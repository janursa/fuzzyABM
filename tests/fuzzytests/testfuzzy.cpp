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

/*
TEST_CASE("Validity for the whole range of inputs", "[main]") {
    auto fuzzy_obj = initialize();
    cout << "results" << setw(4) << results["earlyDiff"] << endl;
    vector<string> target_input = { "Mg","BMP","TGF","CD","damage" ,"AE" };
    vector<string> target_output = {"Mo"};
    map<string, double> non_target_inputs = { {"maturity",0} };
    unsigned steps = 2;
    
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
                //cout << " CD :" << inputs["CD"] << " Mg :" << inputs["Mg"] << " TGF :" << inputs["TGF"] << " BMP :" << inputs["BMP"] <<
                //    " damage :" << inputs["damage"]<< " maturity :" << inputs["maturity"] << " AE :" << inputs["AE"] <<endl;
                //
                //json jj2(inputs);
                //cout << "inputs" << setw(4) << jj2 << endl;
                auto results = fuzzy_obj->predict(inputs);
                //json jj(results);
                //cout << "results"<< setw(4) << jj["Mo"] << endl;
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
}*/
TEST_CASE("Effect of different Mg", "[Mgs]") {
    
    auto fuzzy_obj = initialize();
    map<string, double> inputs_1 = { {"maturity", 0}, { "Mg", 0 }, { "AE",0 }, { "CD",0 }, { "damage",0 }, { "TGF",0 }, { "BMP",0 } };
    map<string, double> inputs_2 = { {"maturity", 0}, { "Mg", .05 }, { "AE",0 }, { "CD",0 }, { "damage",0 }, { "TGF",0 }, { "BMP",0 } };
    map<string, double> inputs_3 = { {"maturity", 0}, { "Mg", .5 }, { "AE",0 }, { "CD",0 }, { "damage",0 }, { "TGF",0 }, { "BMP",0 } };
    auto result_1 = fuzzy_obj->predict(inputs_1);
    auto result_2 = fuzzy_obj->predict(inputs_2);
    auto result_3 = fuzzy_obj->predict(inputs_3);
        
    REQUIRE(result_2["Pr"] > result_1["Pr"]);
            
    //REQUIRE(result_2["Diff"] > result_1["Diff"]);
          
        
    REQUIRE(result_3["Pr"] < result_2["Pr"]);
            
    REQUIRE(result_3["Mo"] > result_1["Mo"]);
            
}
TEST_CASE("Checking early diff", "[earlyDiff]") {
    auto fuzzy_obj = initialize();
    map<string, double> inputs_1 = { {"maturity",0} ,{"Mg",.05},{"AE",0},{"CD",1},{"damage",0},{"TGF",.5},{"BMP",.5} }; // very high
    map<string, double> inputs_21 = { {"maturity",0} ,{"Mg", 0},{"AE",0},{"CD",1},{"damage",0},{"TGF",.5},{"BMP",.5} }; // high
    map<string, double> inputs_22 = { {"maturity",0} ,{"Mg",.05},{"AE",0},{"CD",1},{"damage",0},{"TGF",0},{"BMP",.5} }; // high
    map<string, double> inputs_31 = { {"maturity",0} ,{"Mg", 0},{"AE",0},{"CD",1},{"damage",0},{"TGF",0},{"BMP",.5} }; // medium
    map<string, double> inputs_32 = { {"maturity",0} ,{"Mg", 0},{"AE",0},{"CD",0},{"damage",0},{"TGF",1},{"BMP",1} }; // medium
    map<string, double> inputs_41 = { {"maturity",0} ,{"Mg", .05},{"AE",0},{"CD",0},{"damage",0},{"TGF",0},{"BMP",0} }; // low
    map<string, double> inputs_42 = { {"maturity",0} , {"Mg", 0},{"AE",0},{"CD",0},{"damage",0},{"TGF",0},{"BMP",1} }; // low
    map<string, double> inputs_5 = { {"maturity",0} ,{"Mg", 0},{"AE",0},{"CD",0},{"damage",0},{"TGF",0},{"BMP",0} }; // verylow

    auto result_1 = fuzzy_obj->predict(inputs_1);
    auto result_21 = fuzzy_obj->predict(inputs_21);
    auto result_22 = fuzzy_obj->predict(inputs_22);
    auto result_31 = fuzzy_obj->predict(inputs_31);
    auto result_32 = fuzzy_obj->predict(inputs_32);
    auto result_41 = fuzzy_obj->predict(inputs_41);
    auto result_42 = fuzzy_obj->predict(inputs_42);
    auto result_5 = fuzzy_obj->predict(inputs_5);
    REQUIRE(result_1["earlyDiff"] > result_21["earlyDiff"]);
    REQUIRE(result_1["earlyDiff"] > result_22["earlyDiff"]);
    REQUIRE(result_21["earlyDiff"] > result_32["earlyDiff"]);
    REQUIRE(result_22["earlyDiff"] > result_31["earlyDiff"]);
    REQUIRE(result_32["earlyDiff"] > result_41["earlyDiff"]);
    REQUIRE(result_31["earlyDiff"] > result_42["earlyDiff"]);
    REQUIRE(result_5["earlyDiff"] < result_42["earlyDiff"]);
    REQUIRE(result_5["earlyDiff"] < result_41["earlyDiff"]);
    
    map<string, double> inputs_6 = { {"maturity",0} ,{"Mg", .05},{"AE",0},{"CD",0.8},{"damage",0},{"TGF",0},{"BMP",0} }; // half medium
    auto result_6 = fuzzy_obj->predict(inputs_6);
    cout << result_6["earlyDiff"] << endl;
    REQUIRE(result_6["earlyDiff"] > 0.25);
}
TEST_CASE("Checking mortality", "[Mo]") {
    auto fuzzy_obj = initialize();
    map<string, double> inputs_1 = { {"maturity",0} ,{"Mg",1},{"AE",0},{"CD",1},{"damage",0},{"TGF",0},{"BMP",0} }; // high
    map<string, double> inputs_2 = { {"maturity",0} ,{"Mg",1},{"AE",0},{"CD",1},{"damage",0},{"TGF",1},{"BMP",1} }; // another high
    map<string, double> inputs_3 = { {"maturity",0} , {"Mg",0},{"AE",0},{"CD",1},{"damage",0},{"TGF",0},{"BMP",1} }; // another high
    map<string, double> inputs_4 = { {"maturity",0} ,{"Mg",0},{"AE",1},{"CD",1},{"damage",0},{"TGF",0},{"BMP",1} }; // very high
    map<string, double> inputs_5 = { {"maturity",0} , {"Mg",1},{"AE",0},{"CD",1},{"damage",0},{"TGF",1},{"BMP",0} }; // medium
    map<string, double> inputs_6 = { {"maturity",0} ,{"Mg",0},{"AE",0},{"CD",1},{"damage",0},{"TGF",0},{"BMP",0} }; // another medium
    auto result_1 = fuzzy_obj->predict(inputs_1);
    auto result_2 = fuzzy_obj->predict(inputs_2);
    auto result_3 = fuzzy_obj->predict(inputs_3);
    auto result_4 = fuzzy_obj->predict(inputs_4);
    auto result_5 = fuzzy_obj->predict(inputs_5);
    auto result_6 = fuzzy_obj->predict(inputs_6);
    REQUIRE(result_2["Mo"] == result_1["Mo"]);
    REQUIRE(result_3["Mo"] == result_1["Mo"]);
    REQUIRE(result_4["Mo"] > result_1["Mo"]);
    REQUIRE(result_2["Mo"] > result_5["Mo"]); // high against medium
    REQUIRE(result_5["Mo"] == result_6["Mo"]); // medium against medium
        
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