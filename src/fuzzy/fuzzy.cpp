#include "fuzzy/fuzzy.h"

using std::cout;
using namespace std;
fuzzy::fuzzy(std::string controller_name, std::map<std::string,double> params) { // params for fuzzy definition taged with each cell type
        myMap params_mymap;
        for (auto &param:params){
            params_mymap.insert(param.first,param.second);
        }
        if (controller_name == "MSC"){ // initialze for MSC
            auto MSC_model = std::make_shared<MSC_FUZZY>(params_mymap);
            base_model::fuzzy_model()= MSC_model;
        }
        else {
            std::cerr<<"Error: No controller is defined for the entered key '"<<controller_name<<"'"<<endl;
            std::terminate();
        }
//        cout<<"Successful parameter set definitions for '"<<controller_name<<"'."<<endl;
    }
std::map<std::string,double> fuzzy::predict(std::map<std::string,double> inputs) { // receives a dictionary that inputs are for each cell type are given
        std::map<std::string,double> outputs;
        try{outputs = base_model::fuzzy_model()->predict(inputs);}
        catch(invalid_fuzzy_input &e){
            cerr<<e.what()<<endl;
            std::terminate();
        }catch(invalid_fuzzy_definition & e){
            cerr<<e.what()<<endl;
            std::terminate();
        }catch(invalid_fuzzy_output &e){
            cerr<<e.what()<<endl;
            std::terminate();
        }catch(invalid_engine& e){
            cerr<<e.what()<<endl;
            std::terminate();
        }
        return outputs;
    }
void fuzzy::tests(){
        /** test validity of the model for the whole range of inputs **/
        vector<string> target_input = {"CD","Mg","AE"};
        vector<string> target_output = {"Mo,Mi,Pr"};
        map<string,double> non_target_inputs = { };
        unsigned steps = 50;
        map<string,double> inputs = {};
        std::function<void(unsigned)> RECURSIVE = [&](unsigned j){
            // cout<<"j "<<j <<endl;
            for (unsigned i = 0; i <= steps; i++) {
                auto input_tag  = target_input[target_input.size()-j];
                auto value = i * 1.0 / steps; // assuming that it starts from 0 and has a range of 1
                inputs[input_tag] = value;
                if (j > 1){        
                    RECURSIVE(j -1); 
                }
                else{
                    // cout<<" CD :" << inputs["CD"]<<" Mg :" << inputs["Mg"]<<" AE :" << inputs["AE"]<< " ";
                    auto results = predict(inputs);
                }
            
            };
        };
        RECURSIVE(target_input.size());   
        cout<<"Successful. Valid model for the whole range of inputs"<<endl;

        /** general tests **/
        auto test_1 = [&](){ // check different Mg
            map<string,double> inputs_1 = {{"Mg",0},{"AE",0},{"CD",0.5}};
            map<string,double> inputs_2 = {{"Mg",0.05},{"AE",0},{"CD",0.5}};
            map<string,double> inputs_3 = {{"Mg",0.5},{"AE",0},{"CD",0.5}};
            auto result_1 = predict(inputs_1);
            auto result_2 = predict(inputs_2);
            auto result_3 = predict(inputs_3);
            // cout<<"Me2 "<<result_2["Me"]<<" Me1 "<<result_1["Me"]<<endl;
            assert(("Low Mg results in higher Pr",result_2["Pr"]>result_1["Pr"]));
            assert(("High Mg results in lower Pr",result_3["Pr"]<result_1["Pr"]));
            assert(("High Mg results in higher mortality",result_3["Mo"]>result_1["Mo"]));

        };
        test_1();
        auto test_2 = [&](){ // check different CD
            map<string,double> inputs_1 = {{"Mg",0},{"AE",0},{"CD",0}};
            map<string,double> inputs_2 = {{"Mg",0},{"AE",0},{"CD",0.5}};
            map<string,double> inputs_3 = {{"Mg",0},{"AE",0},{"CD",1}};
            auto result_1 = predict(inputs_1);
            auto result_2 = predict(inputs_2);
            auto result_3 = predict(inputs_3);
            assert(("High CD results in higher mortality compared to normal",result_3["Mo"]>result_2["Mo"]));
            assert(("Low CD results in higher mortality compared to normal",result_1["Mo"]>result_2["Mo"]));
            assert(("High CD results in higher migration compared to normal",result_3["Mi"]>result_2["Mi"]));
        };
        test_2();
        auto test_3 = [&](){ // check different AE
            map<string,double> inputs_1 = {{"Mg",0},{"AE",0},{"CD",0.5}};
            map<string,double> inputs_2 = {{"Mg",0},{"AE",0.5},{"CD",0.5}};
            auto result_1 = predict(inputs_1);
            auto result_2 = predict(inputs_2);
            assert(("High AE results in higher mortality",result_2["Mo"]>result_1["Mo"]));
            assert(("High AE results in lower Pr",result_2["Pr"]<result_1["Pr"]));
        };
        test_3();
        cout<<"Successful. General tests passed"<<endl;
    }

/*
PYBIND11_MODULE(fuzzy, m) {
    py::class_<fuzzy>(m, "fuzzy")
            .def(py::init<std::string,std::map<std::string,double>>()) //receives NN as input
            .def("predict", &fuzzy::predict)
            .def("tests",&fuzzy::tests);
};
*/


