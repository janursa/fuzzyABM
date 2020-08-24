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
		auto baseChance = this->params.at("B_Mo");
		auto a_Pr = this->params.at("a_Pr_Mo");
		auto a_pass = this->params.at("a_c_M0"); // passaging effect
		int pass_flag = 0;
		if (this->myenv->get_tick() <= 1) {
			pass_flag = 1;
		}
		auto change =(1+ a_Pr*this->cycled)*(1+Mo* a_Mo) * (1 + pass_flag* a_pass)* baseChance;
		this->cycled = false;
		auto pick = tools::random(0,1);
		if (pick < change)
			return true;
		else
			return false;
	}

bool MSC::proliferation(double Pr){
	
	auto baseChance = this->params.at("B_Pr");
	auto internal_clock = this->data["Pr_clock"] * baseChance;
	if (internal_clock > 1) internal_clock = 1;
	auto adj_coeff = logic_function(internal_clock);
	auto modified_baseChance = baseChance * adj_coeff;
	
	auto chance =Pr *  modified_baseChance;
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
		auto adaptation_rate = this->params.at("B_rec");
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
	/*json jj(policy_inputs);
	cout << setw(4) << jj << endl;*/
	auto predictions = this->run_policy(policy_inputs);

	// functions
	auto die = this->mortality(predictions["Mo"]);
	auto hatch = this->proliferation(predictions["Pr"]);
	auto walk = this->migration(predictions["Mi"]);
	this->differentiation(predictions["earlyDiff"], predictions["lateDiff"]);
	//bone_production(predictions["ECMprod"], predictions[ "HAprod"]);
	
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
	auto base_rate = this->params["B_Diff"];
	double f_diff;
	if (this->data["maturity"] < this->params["maturity_t"]) { // early maturation
		f_diff = earlyDiff;
	}
	else {
		f_diff = lateDiff;
	}
	auto adj_rate = f_diff  * this->params["a_Diff"]* base_rate;
	//if (tools::random(0,1) < 0.001)
	//cout  <<"\n base_rate: " << base_rate  << " f_diff: " << f_diff << " adj_rate: " << adj_rate << " maturity: " << this->data["maturity"] << endl;
	this->data["maturity"] += adj_rate;
}
void MSC::bone_production(double f_ECM, double f_HA) {


}
//void MSC::GF() {
	/* BMP */
	//auto BMP_cont = this->env->patches[0]->get_data("BMP");
	//auto BMP_PROD = [&]() -> double {

	//	double r_prod = params.at("B_BMP");
	//	auto r_prod_adj = r_prod * this->v_p_v;
	//	return r_prod_adj;
	//};
	//
	//auto BMP_r_prod = BMP_PROD();
	//auto BMP_cont_new = BMP_cont + BMP_r_prod ;
	//if (BMP_cont_new < 0) BMP_cont_new = 0;
	//this->env->patches[0]->set_data("BMP", BMP_cont_new); //only add to the patch 0 as the representative of the domain
	///*cout << "BMP_cont: " << BMP_cont << " BMP_r_prod " << BMP_r_prod  << " BMP_cont_new " << BMP_cont_new << endl;
	//cout << " updated " << this->env->patches[0]->get_data("BMP") << endl;
	//exit(2);*/
	///* TGF */
	//auto TGF_cont = this->env->patches[0]->get_data("TGF");
	//auto TGF_PROD = [&]() -> double {

	//	double r_prod = params.at("B_TGF");
	//	auto r_prod_adj = r_prod * this->v_p_v;
	//	return r_prod_adj;
	//};
	//
	//auto TGF_r_prod = TGF_PROD();
	//auto TGF_cont_new = TGF_cont + TGF_r_prod ;
	//if (TGF_cont_new < 0) TGF_cont_new = 0;
	//this->env->patches[0]->set_data("TGF", TGF_cont_new); //only add to the patch 0 as the representative of the domain

//}
double myEnv::collect_from_patches(string tag){

    double result = 0;
    for (auto const &[index,patch]: this->patches){
        result += patch->get_data(tag);
    }
    return result;
}
double myEnv::collect_from_agents(string tag) {

	double result = 0;
	for (auto const& agent: this->agents) {
		if (agent->class_name == "Dead") continue;
		result += agent->get_data(tag);
	}
	return result;
}
map<string,double> MSC::collect_policy_inputs(){
	
		auto AE = this->alkalinity();
		auto CD = this->patch->get_data("agent_density");
		auto Mg = this->patch->get_data("Mg")/this->params.at("Mg_max");
		auto maturity = this->data["maturity"] ; // maturity indeex
		auto TGF = this->myenv->get_GFs("TGF")/ this->params.at("TGF_max");
		double BMP = this->myenv->get_GFs("BMP")/ this->params.at("BMP_max");
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
	// productions
	unsigned live_cell_count = 0;
	for (auto& agent : this->agents) {
		if (agent->class_name != "Dead") live_cell_count++;
	}
	auto c_cell = live_cell_count / this->grid_settings["volume"];
	auto TGF = [&]() {
		auto c_TGF = this->get_GFs("TGF");

		auto DEG = [&]() ->double {
			double half_life = 1.0 / 6;
			auto half_life_rate = log(2) / half_life;
			auto coeff = exp(-half_life_rate);
			auto deg_rate = c_TGF * (1 - coeff);
			return deg_rate;
		};
		auto PROD = [&]()->double {
			auto b = this->params["b_TGF"];
			auto TGF_max = this->params["TGF_max"];
			auto coeff = (b) / (TGF_max + c_TGF);
			auto rate_prod = coeff * c_cell ;
			//cout << "\n c_TGF "<< c_TGF<<" b " << b << " TGF_max :" << TGF_max << " c_cell:" << c_cell << " coeff " << coeff <<" rate_prod "<< rate_prod<< endl;
			return rate_prod;
		};
		auto prod = PROD();
		auto deg = DEG();
		auto c_TGF_updated = c_TGF + prod - deg;
		this->set_GFs("TGF", c_TGF_updated);
		//cout << "\n agents_c " << this->agents.size() << " volume " << this->grid_settings["volume"] << " c_cell " << c_cell << " rate " << rate << " c "<<c_TGF<< endl;
		//cout << " c0 " << c_TGF << " prod " << prod << " deg " << deg << " c " << c_TGF_updated << endl;
	};
	TGF();
	
	// BMP degrades
	
	auto BMP = [&]() {
		auto c_BMP = this->get_GFs("BMP");
		auto DEG = [&]() ->double {
			auto half_life = 10.08;
			auto half_life_rate = log(2) / half_life;
			auto coeff = exp(-half_life_rate);
			auto deg_rate = c_BMP * (1 - coeff);
			/*cout << "coeff "<< coeff <<" BMP_cont :"<< BMP_cont<<" deg_rate:"<< deg_rate<< endl;
			exit(2);*/
			return deg_rate;
		};
		auto PROD = [&]()->double {
			auto b = this->params["b_BMP"];
			auto BMP_max = this->params["BMP_max"];
			auto coeff = (b) / (BMP_max + c_BMP);
			auto rate_prod = coeff * c_cell ;
			//cout << "b " << b << " BMP_max :" << BMP_max << " c_cell:" << c_cell <<" coeff "<< coeff<< endl;
			return rate_prod;

		};
		auto prod = PROD();
		auto deg = DEG();
		auto c_updated = c_BMP + prod - deg;
		this->set_GFs("BMP", c_updated);
		//cout << " c0 " << c_BMP << " prod " << prod << " deg " << deg << " c " << c_updated << endl;
		//exit(2);
	};
	BMP();
	
}
void myPatch::initialize(){
	initial_conditions["agent_density"] = 0;
	initial_conditions["lactate"] = 0;
	initial_conditions["ECM"] = 0;
	initial_conditions["HA"] = 0;
	/*if (index == 0) {
		initial_conditions["TGF"] = params.at("TGF_0");
		initial_conditions["BMP"] = params.at("BMP_0");
	}
	else {
		initial_conditions["TGF"] = 0;
		initial_conditions["BMP"] = 0;
	}*/
	
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
	double patch_size = this->myenv->grid_settings["patch_size"];
	double v_patch = patch_size * patch_size;
	
}
//shared_ptr<Patch> myEnv::generate_patch(){
//	map<string,double> initial_conditions = py::cast<map<string,double>>(this->settings["setup"]["patch"]["attrs"]);
//	auto patch_obj = make_shared<myPatch>(this->get_ptr(), this->params,
//		initial_conditions);
//	return patch_obj;
//}