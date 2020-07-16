#include "ABM/model.h"
#include <math.h>  
#include <nlohmann/json.hpp>
using json = nlohmann::json;
double myPatch::lactate(){
		double MI = 0;
		if (this->empty) {
			MI = 0;
		}
		else if (this->agent->class_name == "Dead"){
			MI = 0;
		}
		else {
			MI = this->agent->get_data("MI");
		}
		// auto w = this->params["w_MI_lactate"];
		// auto lactate = this->data["lactate"] + w * MI;
		auto lactate = this->data["lactate"] + MI;
		return lactate;
	}
void myPatch::step(){
	auto pH_new = this->pH();
	auto new_lactate = this->lactate();
	this->data["pH"] = pH_new;
	this->data["lactate"] = new_lactate;
	this->data["agent_density"] = this->find_neighbor_agents(true).size()/9.0;
}

bool MSC::mortality(double Mo){
		auto maxOrder = this->params.at("Mo_H_v");
		auto baseChance = this->params.at("B_MSC_Mo");
		auto change =(1+Mo*maxOrder) * baseChance;
		auto pick = tools::random(0,1);
		if (pick < change)
			return true;
		else
			return false;
	}
bool MSC::proliferation(double Pr){
	auto logic_function = [](double x) {
		return (1.0 / (1.0 + exp(-8.0 * (x - 0.5))));
	};
	auto normOrder = this->params.at("Pr_N_v");
	auto baseChance = this->params.at("B_MSC_Pr");
	auto modified_baseChance = 2*baseChance * logic_function(this->data["clock"]);
	//cout << modified_baseChance << endl;
	auto change =(Pr / normOrder) * modified_baseChance;
	auto pick = tools::random(0,1);
	if (pick < change)
		return true;
	else
		return false;
}
double MSC::alkalinity(){
		auto adapted_pH = this->data.at("pH");
		auto env_pH = this->patch->get_data("pH");
		double AE;
		if (adapted_pH == 0)
			AE = 1;
		else
			AE = abs(env_pH - adapted_pH) / adapted_pH;
		if (AE > 1)
			AE = 1;

		return AE;
	}
double MSC::adaptation(){
		auto adapted_pH = this->data.at("pH");
		auto env_pH = this->patch->get_data("pH");
		double new_adapted_pH = 0;
		auto adaptation_rate = this->params.at("B_MSC_rec");
		if (env_pH > adapted_pH)
			new_adapted_pH = adapted_pH + adaptation_rate;
		else
			new_adapted_pH = adapted_pH - adaptation_rate;
		return new_adapted_pH;
	}
bool MSC::migration(double Mi){
		auto chance = Mi;
		auto pick = tools::random(0,1);
		if (pick < chance)
			return true;
		else
			return false;
	}
void MSC::step(){
	// policy's inputs
	auto policy_inputs = this->collect_policy_inputs();
	json jj(policy_inputs);
	cout << setw(4) << jj << endl;
	auto predictions = this->run_policy(policy_inputs);
	// functions
	auto die = this->mortality(predictions["Mo"]);
	auto hatch = this->proliferation(predictions["Pr"]);
	auto walk = this->migration(predictions["Mi"]);

	if (walk)
		this->order_move(/**patch**/nullptr, /* quiet */ true,/** reset**/ true);
	if (hatch)
		this->order_hatch(/**patch**/nullptr, /**inherit**/true,/** quiet **/ true);
	if (die)
		this->order_switch(/** to **/ "Dead");
	
	auto adapted_ph = this->adaptation();
	auto MI = predictions["Pr"];
	this->data["MI"] = MI;
	this->data["pH"] = adapted_ph;
};
double myEnv::collect_from_patches(string tag){
    double result = 0;
    for (auto const &[index,patch]: this->patches){
        result += patch->get_data(tag);
    }
    return result;
}
map<string,double> MSC::collect_policy_inputs(){
		auto AE = this->alkalinity();
		auto CD = this->patch->get_data("agent_density");
		auto Mg = this->patch->get_data("Mg")/this->params.at("Mg_max");
		auto age = this->data["age"] / this->params.at("AGE_H_t");
		auto maturity = this->data["maturity"] ; // maturity indeex
		auto DM = this->patch->get_data("DM") / this->params.at("DM_max");
		auto BMP = this->patch->get_data("BMP") / this->params.at("BMP_max");
		map<string, double> policy_inputs = { {"AE",AE} , {"Mg",Mg} , {"CD", CD} , {"age", age} , {"maturity", maturity} , {"BMP", BMP} , {"DM",DM} };
		return policy_inputs;
	}
void MSC::update(){
	this->data["clock"] += 1;
}
void myEnv::update(){
	Env::update();
	for (auto &agent:this->agents){
		agent->update();
	}
}
void myPatch::initialize(){
		for (auto const &[key,value]:this->initial_conditions){
			this->data[key] = value;
		}
	}
double myPatch::pH(){
		auto mg = this->data.at("Mg");
		auto lactate = this->data.at("lactate");
		// auto pH_new = this->params["w_mg_ph"]*mg -this->params.at("w_lactate_ph")*lactate + 7.8;
		auto pH_new = this->params["w_mg_ph"]*mg + 7.8;
		return pH_new;
	}
void MSC::inherit(shared_ptr<Agent> father){
		for (auto const&[key,value]:this->data){
			this->data[key] = father->get_data(key);
			if (key == "age") {
				this->data[key] += 1;
				father->set_data(key, this->data[key]);
			}
			else if (key == "clock") {
				this->data[key] = 0;
				father->set_data(key, 0);
			}
			
		}
		
	}
void MSC::initialize(map<string,double> initial_conditions){
		for (auto const &[key,value]:initial_conditions){
			this->data[key] = value;
		}
	}
shared_ptr<Patch> myEnv::generate_patch(){
		map<string,double> initial_conditions = py::cast<map<string,double>>(this->settings["setup"]["patch"]["attrs"]);
		auto patch_obj = make_shared<myPatch>(this->get_ptr(), this->params,
			initial_conditions);
		return patch_obj;
}