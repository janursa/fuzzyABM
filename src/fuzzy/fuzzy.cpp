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
            this->fuzzy_model= MSC_model;
        }
        else {
            std::cerr<<"Error: No controller is defined for the entered key '"<<controller_name<<"'"<<endl;
            std::terminate();
        }
//        cout<<"Successful parameter set definitions for '"<<controller_name<<"'."<<endl;
    }
std::map<std::string,double> fuzzy::predict(std::map<std::string,double> inputs) { // receives a dictionary that inputs are for each cell type are given
        std::map<std::string,double> outputs;
        try{outputs = this->fuzzy_model->predict(inputs);}
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


vector<string> generate_rules(vector<vector<string>> factors, vector<string> levels, string target) {
    /** automatically create the initial parts of fuzzy sets; the number of sets are 2^factors.size() **/


    vector<string> sets; // the initial parts of fuzzy sets (if)
    function<void(unsigned i, string&)> recursive = [&](unsigned i, string& set) {

        for (auto& item : factors[i]) {
            string set_copy(set);
            set_copy += item;
            if (i == (factors.size() - 1)) {
                sets.push_back(set_copy);
            }
            else {
                set_copy += " and ";
                recursive(i + 1, set_copy);
            }
        }
    };
    string set = "";
    recursive(0, set); //recursively combine the factors

    /** calculate the portions of sets based on the levels considered for the controller **/
    unsigned levels_n = levels.size();
    vector<pair<int, int>> shares;
    if (levels_n == 5) {
        int quota = sets.size() / levels_n;
        int left_overs = sets.size() % levels_n;
        for (unsigned i = 0; i < levels_n; i++) {
            pair<int, int> share;
            if (i == 0) share.first = 0;
            else share.first = shares[i - 1].first + shares[i - 1].second;
            if (left_overs == 0) share.second = quota;
            else {
                share.second = quota + 1;
                left_overs--;
            }
            shares.push_back(share);
        }
    }
    else {
        cerr << "Not defined for this number of levels" << endl;
        std::exit(2);
    }

    vector<vector<string>> split_sets; // sets for each level
    for (auto& share : shares) {
        vector<string> holder;
        for (int i = share.first; i < (share.first + share.second); i++) {
            holder.push_back(sets[i]);
        }
        split_sets.push_back(holder);
    }
    unsigned ii = 0;

    /* creating complete rules by adding the THEN part*/

    vector<string> rules;
    for (unsigned i = 0; i < split_sets.size(); i++) {
        string ors;
        for (unsigned j = 0; j < split_sets[i].size(); j++) {
            string oneor = " ( " + split_sets[i][j] + " ) ";
            if (j != split_sets[i].size() - 1) oneor += " or "; // for all but the last one add "or" in between
            ors += oneor;
        }
        string full = "if " + ors + " then " + target + " is " + levels[i];
        //cout << full << endl;
        rules.push_back(full);
    }
    return rules;

}