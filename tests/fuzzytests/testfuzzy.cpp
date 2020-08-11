#define CATCH_CONFIG_MAIN
#include <fstream>
#include <catch2/catch.hpp>
#include <nlohmann/json.hpp>
#include "fuzzy/fuzzy.h"
using json = nlohmann::json;


shared_ptr<fuzzy> initialize() {
    string params_dir = "D:/projects/ABM/scripts/params.json";
    std::ifstream  params_file(params_dir);
    json params_json = json::parse(params_file);
    map<string, double> params = params_json;
    auto fuzzy_ptr = make_shared<fuzzy>("MSC", params);
    std::string status;
    auto flag = fuzzy_ptr->fuzzy_model->engine->isReady(&status);
    return fuzzy_ptr;
}


TEST_CASE("Validity for the whole range of inputs", "[main]") {
    auto fuzzy_obj = initialize();
    /*map<string, double> inputs = { {"Mg", 0}, { "BMP", 1}, { "TGF",1 }, { "CD",0 }, 
        
        { "damage", 0 }, { "maturity",0 }, { "AE",0 } };

    auto results = fuzzy_obj->predict(inputs);
    cout << "results" << setw(4) << results["earlyDiff"] << endl;*/
    vector<string> target_input = { "Mg","BMP","TGF","CD","damage","maturity" ,"AE" };
    vector<string> target_output = {"earlyDiff"};
    map<string, double> non_target_inputs = {};
    unsigned steps = 5;
    
    map<string, double> inputs = {};
    for (auto& [key, value] : non_target_inputs) {
        inputs[key] = value;
    }
    std::function<void(unsigned)> RECURSIVE = [&](unsigned j) {
        for (unsigned i = 0; i <= steps; i++) {
            auto input_tag = target_input[target_input.size() - j];
            auto value = i * 1.0 / steps; // assuming that it starts from 0 and has a range of 1
            inputs[input_tag] = value;
            if (j > 1) {
                RECURSIVE(j - 1);
            }
            else {
                /*cout << " CD :" << inputs["CD"] << " Mg :" << inputs["Mg"] << " TGF :" << inputs["TGF"] << " BMP :" << inputs["BMP"] <<
                    " damage :" << inputs["damage"]<< " maturity :" << inputs["maturity"] << " AE :" << inputs["AE"] <<endl;
                */
                //json jj2(inputs);
                //cout << "inputs" << setw(4) << jj2 << endl;
                auto results = fuzzy_obj->predict(inputs);
/*                json jj(results);
                cout << "results"<< setw(4) << jj["earlyDiff"] << endl;*/
            }
        };
    };
    auto flag = true;
    try {
        RECURSIVE(target_input.size());
    }
    catch (...){
        flag = false;
    }
    REQUIRE(flag);
}
SCENARIO("Effect of different Mg", "[Mgs]") {
    GIVEN("A set of inputs") {
        auto fuzzy_obj = initialize();
        map<string, double> inputs_1 = { {"Mg",0},{"AE",0},{"CD",0.5},{"maturity",0},{"damage",0},{"TGF",0},{"BMP",0} };
        map<string, double> inputs_2 = { {"Mg",.05},{"AE",0},{"CD",0.5},{"maturity",0},{"damage",0},{"TGF",0},{"BMP",0} };
        map<string, double> inputs_3 = { {"Mg",.5},{"AE",0},{"CD",0.5},{"maturity",0},{"damage",0},{"TGF",0},{"BMP",0} };
        auto result_1 = fuzzy_obj.predict(inputs_1);
        auto result_2 = fuzzy_obj.predict(inputs_2);
        auto result_3 = fuzzy_obj.predict(inputs_3);
        WHEN("Low Mg conc.") {
            THEN("Higher proliferation") {
                REQUIRE(result_2["Pr"] > result_1["Pr"]);
            }
            THEN("Higher diff") {
                REQUIRE(result_2["Diff"] > result_1["Diff"]);
            }
        };
        WHEN("High Mg conc.") {
            THEN("Lower proliferation") {
                REQUIRE(result_3["Pr"] < result_2["Pr"]);
            };
            THEN("Higher mortality") {
                REQUIRE(result_3["Mo"] > result_1["Mo"]);
            }
        };
    }
}
 /*   
SCENARIO("Validity for different Mg values", "[Mgs]") {
    GIVEN("A set of inputs") {
        auto fuzzy_obj = initialize();
        map<string, double> inputs_1 = { {"Mg",0},{"AE",0},{"CD",0.5},{"age",0} };
        map<string, double> inputs_2 = { {"Mg",0.05},{"AE",0},{"CD",0.5},{"age",0} };
        map<string, double> inputs_3 = { {"Mg",0.5},{"AE",0},{"CD",0.5},{"age",0} };
        auto result_1 = fuzzy_obj.predict(inputs_1);
        auto result_2 = fuzzy_obj.predict(inputs_2);
        auto result_3 = fuzzy_obj.predict(inputs_3);
        WHEN("Low Mg conc.") {
            THEN("Higher proliferation") {
                REQUIRE(result_2["Pr"] > result_1["Pr"]);
            }
        };
        WHEN("High Mg conc.") {
            THEN("Lower proliferation") {
                REQUIRE(result_3["Pr"] < result_1["Pr"]);
            };
            THEN("Higher mortality") {
                REQUIRE(result_3["Mo"] > result_1["Mo"]);
            }
        };
    }
}
SCENARIO("Validity for different CD values", "[CDs]") {
    GIVEN("A set of inputs") {
        auto fuzzy_obj = initialize();
        map<string, double> inputs_1 = { {"Mg",0},{"AE",0},{"CD",0},{"age",0} };
        map<string, double> inputs_2 = { {"Mg",0},{"AE",0},{"CD",0.5} ,{"age",0} };
        map<string, double> inputs_3 = { {"Mg",0},{"AE",0},{"CD",1} ,{"age",0} };
        auto result_1 = fuzzy_obj.predict(inputs_1);
        auto result_2 = fuzzy_obj.predict(inputs_2);
        auto result_3 = fuzzy_obj.predict(inputs_3);
        WHEN("High CD") {
            THEN("Higher mortality compared to medium") {
                REQUIRE(result_3["Mo"] > result_2["Mo"]);
            }
            THEN("Higher migration compared to medium") {
                REQUIRE(result_3["Mi"] > result_2["Mi"]);
            }
        };
        WHEN("Low CD") {
            THEN("higher mortality compared to medium") {
                REQUIRE(result_1["Mo"] > result_2["Mo"]);
            };

        };
    }
}

SCENARIO("Validity for different AE values", "[AEs]") {
    GIVEN("A set of inputs") {
        auto fuzzy_obj = initialize();
        map<string, double> inputs_1 = { {"Mg",0},{"AE",0},{"CD",0.5},{"age",0} };
        map<string, double> inputs_2 = { {"Mg",0},{"AE",0.5},{"CD",0.5},{"age",0} };
        auto result_1 = fuzzy_obj.predict(inputs_1);
        auto result_2 = fuzzy_obj.predict(inputs_2);
        json jj(result_2);
        cout << setw(4) << jj << endl;
        WHEN("High AE") {
            THEN("Higher mortality compared to medium") {
                REQUIRE(result_2["Mo"] > result_1["Mo"]);
            }
            THEN("Lower Pr compared to medium") {
                REQUIRE(result_2["Pr"] < result_1["Pr"]);
            }
        };
    }
}
SCENARIO("Validity for different age values", "[ages]") {
    GIVEN("A set of inputs") {
        auto fuzzy_obj = initialize();
        map<string, double> inputs_1 = { {"Mg",0},{"AE",0},{"CD",0.5},{"age",0} };
        map<string, double> inputs_2 = { {"Mg",0},{"AE",0},{"CD",0.5},{"age",.5} };
        auto result_1 = fuzzy_obj.predict(inputs_1);
        auto result_2 = fuzzy_obj.predict(inputs_2);
        WHEN("High age") {
            THEN("lower Pr compared to medium") {
                REQUIRE(result_2["Pr"] < result_1["Pr"]);
            }
        };
    }
}
SCENARIO("Validity for synergic effect of age and mg", "[age_mg]") {
    GIVEN("A set of inputs") {
        auto fuzzy_obj = initialize();
        map<string, double> inputs_1 = { {"Mg",0.05},{"AE",0},{"CD",0.5},{"age",0} };
        map<string, double> inputs_2 = { {"Mg",0},{"AE",0},{"CD",0.5},{"age",0} };
        map<string, double> inputs_3 = { {"Mg",0},{"AE",0},{"CD",0.5},{"age",.5} };
        auto result_1 = fuzzy_obj.predict(inputs_1);
        auto result_2 = fuzzy_obj.predict(inputs_2);
        auto result_3 = fuzzy_obj.predict(inputs_3);
        WHEN("Low age and low Mg produces highest Pr") {
            REQUIRE(result_1["Pr"] > result_2["Pr"]);
            REQUIRE(result_2["Pr"] > result_3["Pr"]);
        };
    }
}*/