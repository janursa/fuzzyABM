#include "model.h"

double myPatch::lactate(){
		double MI = 0;
		if (!this->empty and this->agent->class_name != "Dead")
			MI = this->agent->get_data("MI");
		else
			MI = 0;
		auto w = this->params["w_MI_lactate"];
		auto lactate = this->data["lactate"] + w * MI;
		return lactate;
	}
void myPatch::step(){

	auto pH_new = this->pH();
	// auto new_lactate = this->lactate();
	this->data["pH"] = pH_new;
	// this->data["lactate"] = new_lactate;
	this->data["agent_density"] = this->find_neighbor_agents(true).size()/9.0;
}

bool MSC::mortality(double Mo){
		auto maxOrder = this->params["Mo_H_v"];
		auto baseChance = this->params["B_MSC_Mo"];
		auto change =(1+Mo*maxOrder) * baseChance;
		auto pick = tools::random(0,1);
		if (pick < change)
			return true;
		else
			return false;
	}
bool MSC::proliferation(double Pr){
		auto normOrder = this->params["Pr_N_v"];
		auto baseChance = this->params["B_MSC_Pr"];
		auto change =(Pr / normOrder) * baseChance;
		auto pick = tools::random(0,1);
		if (pick < change)
			return true;
		else
			return false;
	}
double MSC::alkalinity(){
		auto adapted_pH = this->data["pH"];
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
		auto adapted_pH = this->data["pH"];
		auto env_pH = this->patch->get_data("pH");
		double new_adapted_pH = 0;
		auto adaptation_rate = this->params["B_MSC_rec"];
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
	auto predictions = this->run_policy(policy_inputs);
	// functions
	auto die = this->mortality(predictions["Mo"]);
	auto hatch = this->proliferation(predictions["Pr"]);
	auto walk = this->migration(predictions["Mi"]);
	auto adapted_ph = this->adaptation();
	auto MI = predictions["Pr"];
	if (walk)
		this->order_move(/**patch**/nullptr, /* quiet */ true,/** reset**/ true);
	if (hatch)
		this->order_hatch(/**patch**/nullptr, /**inherit**/true,/** quiet **/ true, /**silent**/ true);
	if (die)
		this->order_switch(/** to **/ "Dead");
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
		auto Mg = this->patch->get_data("Mg")/this->params["Mg_max"];
		map<string,double> policy_inputs = {{"AE",AE}, {"Mg",Mg}, {"CD", CD}};

		return policy_inputs;
	}
void myPatch::initialize(map<string,double> configs){
		for (auto const &[key,value]:configs){
			this->data[key] = value;
		}
	}
double myPatch::pH(){
		auto mg = this->data["Mg"];
		// auto lactate = this->data["lactate"];
		// auto pH_new = this->params["w_mg_ph"]*mg -this->params["w_lactate_ph"]*lactate + 7.8;
		auto pH_new = this->params["w_mg_ph"]*mg + 7.8;
		return pH_new;
	}
void MSC::inherit(shared_ptr<Agent> father){
		for (auto const&[key,value]:this->data){
			this->data[key] = father->get_data(key);
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