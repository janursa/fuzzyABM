#define CATCH_CONFIG_MAIN
#include <fstream>
#include <catch2/catch.hpp>
#include <nlohmann/json.hpp>
#include "fuzzy/fuzzy.h"
using json = nlohmann::json;


fuzzy initialize() {
    string params_dir = "D:/projects/ABM/scripts/params.json";
    std::ifstream  params_file(params_dir);
    json params_json = json::parse(params_file);
    map<string, double> params = params_json;
    auto fuzzy_obj = fuzzy("MSC", params);
    return fuzzy_obj;
}


TEST_CASE("Validity for the whole range of inputs", "[main]") {
    auto fuzzy_obj = initialize();
    vector<string> target_input = { "CD","Mg","AE","age" };
    vector<string> target_output = { "Mo","Mi","Pr" };
    map<string, double> non_target_inputs = { };
    unsigned steps = 20;
    map<string, double> inputs = {};

    std::function<void(unsigned)> RECURSIVE = [&](unsigned j) {
        // cout<<"j "<<j <<endl;
        for (unsigned i = 0; i <= steps; i++) {
            auto input_tag = target_input[target_input.size() - j];
            auto value = i * 1.0 / steps; // assuming that it starts from 0 and has a range of 1
            inputs[input_tag] = value;
            if (j > 1) {
                RECURSIVE(j - 1);
            }
            else {
                // cout<<" CD :" << inputs["CD"]<<" Mg :" << inputs["Mg"]<<" AE :" << inputs["AE"]<< " ";
                fuzzy_obj.predict(inputs);
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
            THEN("Higher mortality compared to normal") {
                REQUIRE(result_3["Mo"] > result_2["Mo"]);
            }
            THEN("Higher migration compared to normal") {
                REQUIRE(result_3["Mi"] > result_2["Mi"]);
            }
        };
        WHEN("Low CD") {
            THEN("higher mortality compared to normal") {
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
        WHEN("High AE") {
            THEN("Higher mortality compared to normal") {
                REQUIRE(result_2["Mo"] > result_1["Mo"]);
            }
            THEN("Lower Pr compared to normal") {
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
            THEN("lower Pr compared to normal") {
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
}