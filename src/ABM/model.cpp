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
	//auto new_lactate = this->lactate();
	this->data["pH"] = pH_new;
	//this->data["lactate"] = new_lactate;
	this->data["agent_density"] = this->find_neighbor_agents(true).size()/9.0;
}

bool MSC::mortality(double Mo){
		auto a_Mo = this->params.at("a_Mo");
		auto baseChance = this->params.at("B_MSC_Mo");
		auto a_Pr = this->params.at("a_Pr_Mo");
		auto change =(1+ a_Pr*this->cycled)*(1+Mo* a_Mo) * baseChance;
		this->cycled = false;
		auto pick = tools::random(0,1);
		if (pick < change)
			return true;
		else
			return false;
	}

bool MSC::proliferation(double Pr){
	
	auto baseChance = this->params.at("B_MSC_Pr");
	auto internal_clock = this->data["Pr_clock"] * baseChance;
	if (internal_clock > 1) internal_clock = 1;
	auto adj_coeff = logic_function(internal_clock);
	auto modified_baseChance = baseChance * adj_coeff;
	
	auto chance =Pr * this->params.at("a_Pr")* modified_baseChance;
	auto pick = tools::random(0,1);
	//cout << "internal_clock:"<< internal_clock <<" adj_coeff: "<< adj_coeff<<" modified:"<< modified_baseChance <<" pr: "<<Pr<<" chance: "<< chance << endl;
	if (pick < chance)
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
			AE = this->params.at("AE_a_coeff") * abs(env_pH - adapted_pH) / adapted_pH;
		if (AE > 1)
			AE = 1;
		// damage
		if (this->patch->get_data("pH") >= this->params.at("pH_t")) {
			this->damage = true;
		}
		return AE;
	}
double MSC::adaptation(){
		auto adapted_pH = this->data.at("pH");
		if (this->damage) return adapted_pH; // not recovery for permanent damage

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
	//json jj(policy_inputs);
	//cout << setw(4) << jj << endl;
	auto predictions = this->run_policy(policy_inputs);
	// functions
	auto die = this->mortality(predictions["Mo"]);
	auto hatch = this->proliferation(predictions["Pr"]);
	auto walk = this->migration(predictions["Mi"]);
	this->differentiation(predictions["earlyDiff"], predictions["lateDiff"]);
	bone_production(predictions["ECMprod"], predictions[ "HAprod"]);
	GF_production();
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
void MSC::differentiation(double earlyDiff, double lateDiff) {
	// TODO: update maturity
	if (this->data["maturity"] >= 1) return;
	auto base_rate = this->params["B_MSC_Diff"];
	double f_diff;
	if (this->data["maturity"] < this->params["maturity_t"]) { // early maturation
		f_diff = earlyDiff;
	}
	else {
		f_diff = lateDiff;
	}
	auto adj_rate = f_diff  * this->params["a_Diff"]* base_rate;
	cout  <<" base_rate: " << base_rate  << " f_diff: " << f_diff << " adj_rate: " << adj_rate << " maturity: " << this->data["maturity"] << endl;
	this->data["maturity"] += adj_rate;
}
void MSC::bone_production(double f_ECM, double f_HA) {


}
void MSC::GF_production() {
	// BMP
	auto a_BMP = 15.0;
	auto a_BMP_0 = 0.01;
	auto b_ECM = 2.0 * 0.000000001 / (24); // TODO: check the training data and possibly modify the rate

	double k = (b_ECM / (a_BMP * this->data["BMP"] + a_BMP_0));
	this->data["BMP"] += k;
	
}
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
		auto maturity = this->data["maturity"] ; // maturity indeex
		auto TGF = this->patch->get_data("TGF");
		double BMP = this->patch->get_data("BMP");
		float damage = this->damage;
		map<string, double> policy_inputs = { {"AE",AE} , {"Mg",Mg} , {"CD", CD} , {"TGF", TGF} ,
			{"maturity", maturity} , {"BMP",BMP},{"damage",damage} };
		return policy_inputs;
	}
void MSC::update(){
	this->data["Pr_clock"] += 1;
}
void myEnv::update(){
	Env::update();
	for (auto &agent:this->agents){
		agent->update();
	}
}
void myPatch::initialize(){
	initial_conditions["BMP"] = 0;
	initial_conditions["TGF"] = 0;
	initial_conditions["agent_density"] = 0;
	initial_conditions["lactate"] = 0;
	initial_conditions["ECM"] = 0;
	initial_conditions["HA"] = 0;
	for (auto const &[key,value]:this->initial_conditions){
		this->data[key] = value;
	}
}
double myPatch::pH(){
		auto mg = this->data.at("Mg");
		auto lactate = this->data.at("lactate");
		// auto pH_new = this->params["w_mg_ph"]*mg -this->params.at("w_lactate_ph")*lactate + 7.8;
		auto pH_new = this->params["w_mg_ph"]*mg + 7.83;
		return pH_new;
	}
void MSC::inherit(shared_ptr<Agent> father){
	this->cycled = true;
		for (auto const&[key,value]:this->data){
			this->data[key] = father->get_data(key);
			if (key == "age") {
				this->data[key] += 1;
				father->set_data(key, this->data[key]);
			}
			else if (key == "Pr_clock") {
				this->data[key] = 0;
				father->set_data(key, 0);
			}
			
		}
		
	}
void MSC::initialize(map<string,double> initial_conditions){
	initial_conditions["pH"] = 7.8;
	initial_conditions["Pr_clock"] = 0;
	initial_conditions["maturity"] = 0;
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