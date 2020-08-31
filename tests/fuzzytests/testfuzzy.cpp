#define CATCH_CONFIG_MAIN
#include <fstream>
#include <catch2/catch.hpp>
#include <nlohmann/json.hpp>
#include "fuzzy/fuzzy.h"
using json = nlohmann::json;


shared_ptr<fuzzy> initialize() {
    string params_dir = "../scripts/params.json";
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
    vector<string> target_input = { "Mg","BMP","TGF", "maturity" ,"AE" };
    vector<string> target_output = {"HAprod"};
    map<string, double> non_target_inputs = { {"damage",0},{"CD",.5 } };

    unsigned steps = 10;
    
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
                
                //json jj2(inputs);
                //cout << "inputs" << setw(4) << jj2 << endl;
                auto results = fuzzy_obj->predict(inputs);
                //json jj(results);
                //cout << "results"<< setw(4) << jj["HAprod"] << endl;
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
*/

TEST_CASE("Effect of different Mg", "[Mgs]") {
    
    auto fuzzy_obj = initialize();
    map<string, double> inputs_1 = { {"maturity", 0}, { "Mg", 0 }, { "AE",0 }, { "CD",0 }, { "damage",0 }, { "TGF",0 }, { "BMP",0 } };
    map<string, double> inputs_2 = { {"maturity", 0}, { "Mg", .05 }, { "AE",0 }, { "CD",0 }, { "damage",0 }, { "TGF",0 }, { "BMP",0 } };
    map<string, double> inputs_3 = { {"maturity", 0}, { "Mg", .5 }, { "AE",0 }, { "CD",0 }, { "damage",0 }, { "TGF",0 }, { "BMP",0 } };
    map<string, double> inputs_01 = { {"maturity", 0 }, { "Mg", .017 }, { "AE",0 }, { "CD",0.5 }, { "damage",0 }, { "TGF",0 }, { "BMP",0 } };
    map<string, double> inputs_02 = { {"maturity", .5 }, { "Mg", .083 }, { "AE",0 }, { "CD",0.5 }, { "damage",0 }, { "TGF",0 }, { "BMP",0 } };
    map<string, double> inputs_03 = { {"maturity", .9 }, { "Mg", .083 }, { "AE",0 }, { "CD",0.5 }, { "damage",0 }, { "TGF",0 }, { "BMP",0 } };

    auto result_01 = fuzzy_obj->predict(inputs_01);
    auto result_02 = fuzzy_obj->predict(inputs_02);
    auto result_03 = fuzzy_obj->predict(inputs_03);
    cout<<"Mg 1mM late diff: "<<result_01["lateDiff"]<<"  Mg 5mM late diff: "<< result_02["lateDiff"]<<endl;
    cout<<"Mg 5mM maturity 0.5 late diff: "<<result_02["lateDiff"]<<"  Mg 5mM maturity 0.9 late diff: "<<result_03["lateDiff"]<<endl;
    REQUIRE(result_01["lateDiff"] > result_02["lateDiff"]);
    REQUIRE(result_02["lateDiff"] == result_03["lateDiff"]);

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
TEST_CASE("Checking HA produnction", "[HAprod]") {
    auto fuzzy_obj = initialize();
    map<string, double> inputs_11 = { {"maturity",0 } ,{"Mg",0},{"AE",0},{"CD",0},{"damage",0},{"TGF",0},{"BMP",1} }; // all good other than maturity
    map<string, double> inputs_12 = { {"maturity",1} ,{"Mg",1},{"AE",1},{"CD",0},{"damage",0},{"TGF",1},{"BMP",1} }; // all bad other than maturity
    REQUIRE(fuzzy_obj->predict(inputs_11)["HAprod"] < fuzzy_obj->predict(inputs_12)["HAprod"]); // check that maturity is the prime factor

    // check the levels
    map<string, double> inputs_vh = { {"maturity",1} ,{"Mg",0},{"AE",0},{"CD",0},{"damage",0},{"TGF",0},{"BMP",1} }; // very high
    REQUIRE(fuzzy_obj->predict(inputs_vh)["HAprod"] == 1);
    map<string, double> inputs_h1 = { {"maturity",1} ,{"Mg",0},{"AE",0},{"CD",0},{"damage",0},{"TGF",0},{"BMP",0} }; // high
    REQUIRE(fuzzy_obj->predict(inputs_h1)["HAprod"] == 0.75);
    map<string, double> inputs_h2 = { {"maturity",1} ,{"Mg",0},{"AE",0},{"CD",0},{"damage",0},{"TGF",1},{"BMP",1} }; // high
    REQUIRE(fuzzy_obj->predict(inputs_h2)["HAprod"] == 0.75);
    map<string, double> inputs_h3 = { {"maturity",1} ,{"Mg",1},{"AE",0},{"CD",0},{"damage",0},{"TGF",0},{"BMP",1} }; // high
    REQUIRE(fuzzy_obj->predict(inputs_h3)["HAprod"] == 0.75);
    map<string, double> inputs_m1 = { {"maturity",1} ,{"Mg",1},{"AE",0},{"CD",0},{"damage",0},{"TGF",0},{"BMP",0} }; // medium
    REQUIRE(fuzzy_obj->predict(inputs_m1)["HAprod"] == 0.5);
    map<string, double> inputs_m2 = { {"maturity",1} ,{"Mg",0},{"AE",1},{"CD",0},{"damage",0},{"TGF",0},{"BMP",0} }; // medium
    REQUIRE(fuzzy_obj->predict(inputs_m2)["HAprod"] == 0.5);
    map<string, double> inputs_l1 = { {"maturity",1} ,{"Mg",1},{"AE",1},{"CD",0},{"damage",0},{"TGF",0},{"BMP",0} }; // low
    REQUIRE(fuzzy_obj->predict(inputs_l1)["HAprod"] == 0.25);
    map<string, double> inputs_l2 = { {"maturity",1} ,{"Mg",0},{"AE",1},{"CD",0},{"damage",0},{"TGF",1},{"BMP",0} }; // low
    REQUIRE(fuzzy_obj->predict(inputs_l2)["HAprod"] == 0.25);
    map<string, double> inputs_vr1 = { {"maturity",1} ,{"Mg",1},{"AE",1},{"CD",0},{"damage",0},{"TGF",1},{"BMP",0} }; // verylow
    REQUIRE(fuzzy_obj->predict(inputs_vr1)["HAprod"] == 0);
    map<string, double> inputs_vr2 = { {"maturity",0} ,{"Mg",1},{"AE",0},{"CD",0},{"damage",0},{"TGF",1},{"BMP",0} }; // verylow
    REQUIRE(fuzzy_obj->predict(inputs_vr2)["HAprod"] == 0);
    map<string, double> inputs_vr3 = { {"maturity",1} ,{"Mg",1},{"AE",0},{"CD",0},{"damage",1},{"TGF",1},{"BMP",1} }; // verylow
    REQUIRE(fuzzy_obj->predict(inputs_vr3)["HAprod"] == 0);

    // check random
    map<string, double> inputs1 = { {"maturity",0.5} ,{"Mg",0},{"AE",0.2},{"CD",0},{"damage",0},{"TGF",.2},{"BMP",.6} }; // middle
    map<string, double> inputs2 = { {"maturity",0.7} ,{"Mg",0.5},{"AE",0.2},{"CD",0},{"damage",0},{"TGF",0.2},{"BMP",0.6} }; // better
    map<string, double> inputs3 = { {"maturity",0.5} ,{"Mg",1},{"AE",0},{"CD",0},{"damage",0},{"TGF",1},{"BMP",.6} }; // worse
    REQUIRE(fuzzy_obj->predict(inputs1)["HAprod"] < fuzzy_obj->predict(inputs2)["HAprod"]);
    REQUIRE(fuzzy_obj->predict(inputs3)["HAprod"] < fuzzy_obj->predict(inputs1)["HAprod"]);
}