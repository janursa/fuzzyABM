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


/*
PYBIND11_MODULE(fuzzy, m) {
    py::class_<fuzzy>(m, "fuzzy")
            .def(py::init<std::string,std::map<std::string,double>>()) //receives NN as input
            .def("predict", &fuzzy::predict)
            .def("tests",&fuzzy::tests);
};
*/


