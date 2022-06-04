#include "ABM/model.h"
#include <math.h>  
// #include <nlohmann/json.hpp>
// using json = nlohmann::json;
// #define DIFFUSION 
double myPatch::lactate(){
		double MI = 0;
		if (this->empty()) {
			MI = 0;
		}
		else if (this->get_agents()[0]->class_name == "Dead"){
			MI = 0;
		}
		else {
			MI = this->get_agents()[0]->get_data("MI");
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
	float max_cell_count = 9.0;
	if (this->flags.at("D3")) {
		max_cell_count = 27.0;
	}
	this->data["agent_density"] = this->find_neighbor_agents(true).size()/ max_cell_count;
}

bool Cell::mortality(double Mo){
	auto a_Mo = this->params.at("a_Mo");
	auto baseChance = this->params.at("B_Mo");
	auto a_Pr = this->params.at("a_Pr_Mo");
	auto a_pass = this->params.at("a_c_Mo"); // passaging effect
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

bool Cell::proliferation(double Pr){
	auto baseChance = this->params.at("B_Pr");
	auto internal_clock = this->data["Pr_clock"] * baseChance;
	if (internal_clock > 1) internal_clock = 1;
	auto adj_coeff = logic_function(internal_clock);
	auto modified_baseChance = baseChance * adj_coeff;
	
	auto chance = Pr * this->params["a_P"]* modified_baseChance;
	auto pick = tools::random(0,1);
	//cout << "internal_clock:"<< internal_clock <<" adj_coeff: "<< adj_coeff<<" modified:"<< modified_baseChance <<" pr: "<<Pr<<" chance: "<< chance << endl;
	if (pick < chance)
		return true;
	else
		return false;
}
double Cell::alkalinity(){
	auto adapted_pH = this->data.at("pH");
	auto env_pH = this->get_patch()->get_data("pH");
	double AE;
	if (adapted_pH == 0)
		AE = 1;
	else
		AE = this->params.at("AE_a_coeff") * abs(env_pH - adapted_pH) / adapted_pH;
	if (AE > 1)
		AE = 1;
	// damage
	if (this->get_patch()->get_data("pH") >= this->params.at("pH_t")) {
		this->damage = true;
	}
	return AE;
	}
double Cell::adaptation(){
	auto adapted_pH = this->data.at("pH");
	if (this->damage) return adapted_pH; // not recovery for permanent damage

	auto env_pH = this->get_patch()->get_data("pH");
	double new_adapted_pH = 0;
	auto adaptation_rate = this->params.at("B_rec");
	if (env_pH > adapted_pH)
		new_adapted_pH = adapted_pH + adaptation_rate;
	else
		new_adapted_pH = adapted_pH - adaptation_rate;
	return new_adapted_pH;
	}
bool Cell::migration(double Mi){
		auto chance = Mi;
		auto pick = tools::random(0,1);
		if (pick < chance)
			return true;
		else
			return false;
	}
void myEnv::setup_agents(map<string, unsigned> config) {
	auto FIND_PATCH = [&]() {
		vector<unsigned> patches_indices;
		for(auto const& patch: this->patches)
    		patches_indices.push_back(patch.first);
		auto patches_indices_copy = patches_indices;
		auto patch_count = patches_indices.size();
		auto g = tools::randomly_seeded_MT();

		std::shuffle(patches_indices_copy.begin(), patches_indices_copy.end(), g);

		for (auto const& i : patches_indices_copy) {
			auto potential_patch = this->patches.at(i);
			if (potential_patch->layer_index != 0) continue;
			if (potential_patch->empty()) {
				return potential_patch;
			}
		}
		throw patch_availibility("All patches are occupied.");
	};

	for (auto const [agent_type, count] : config) {
		for (unsigned i = 0; i < count; i++) {
			auto patch = FIND_PATCH();
			auto agent = this->generate_agent(agent_type);
			this->place_agent(patch, agent);
		}
		this->agent_classes.insert(agent_type);
	}
}
void Cell::step(){
	if (class_name == "Dead"){
		return;
	}
	// policy's inputs
	auto policy_inputs = this->collect_policy_inputs();
	/*json jj(policy_inputs);
	cout << setw(4) << jj << endl;*/
	auto predictions = this->run_policy(policy_inputs);

	// functions
	auto die = this->mortality(predictions["Mo"]);
	auto hatch = this->proliferation(predictions["Pr"]);
	// auto walk = this->migration(predictions["Mi"]);
	this->differentiation(predictions["earlyDiff"], predictions["lateDiff"]);
	
	//bone_production(predictions["ECMprod"], predictions[ "HAprod"]);
	
	// if (walk)
	// 	this->order_move(/**patch**/nullptr, /* quiet */ true,/** reset**/ true);
	if (hatch)
		this->order_hatch(/**patch**/nullptr, /**inherit**/true,/** quiet **/ true);
	if (die)
		this->order_switch(/** to **/ "Dead");
	
	auto adapted_ph = this->adaptation();
	auto MI = predictions["Pr"];
	this->data["MI"] = MI;
	this->data["pH"] = adapted_ph;
};
void Cell::differentiation(double earlyDiff, double lateDiff) {
	if (class_name == "Dead"){
		return;
	}
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
//	cout  <<"\n base_rate: " << base_rate  << " f_diff: " << f_diff << " adj_rate: " << adj_rate << " maturity: " << this->data["maturity"] << endl;
	this->data["maturity"] += adj_rate;
	this->data["diff_rate"] = adj_rate;
}
void Cell::bone_production(double f_ECM, double f_HA) {


}

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
map<string,double> Cell::collect_policy_inputs(){

		auto AE = this->alkalinity();
		auto CD = this->get_patch()->get_data("agent_density");
		auto Mg = this->get_patch()->get_data("Mg")/this->params.at("Mg_max");
		auto maturity = this->data["maturity"] ; // maturity indeex
		auto TGF = this->myenv->get_GFs("TGF")/ this->params.at("TGF_max");
		double BMP = this->myenv->get_GFs("BMP")/ this->params.at("BMP_max");
		float damage = this->damage;
		map<string, double> policy_inputs = { {"AE",AE} , {"Mg",Mg} , {"CD", CD} , {"TGF", TGF} ,
			{"maturity", maturity} , {"BMP",BMP},{"damage",damage} };
		return policy_inputs;
	}
void Cell::update(){
	if (class_name == "Dead"){
			return;
		}
	this->data["Pr_clock"] += 1;
}
void myEnv::GFs_diffusion_model(){

}
void myEnv::GFs_static_model(){
	unsigned live_cell_count = 0;
	for (auto& agent : this->agents) {
		if (agent->class_name != "Dead") live_cell_count++;
	}
	auto c_cell = live_cell_count / this->grid_settings["volume"]/pow(10,6);
	// normalized maturity
	auto maturity_t = this->collect_from_agents("maturity");
	double maturity_n = 0;
	if (live_cell_count == 0) maturity_n = 0;
    else   maturity_n = maturity_t/live_cell_count;
    // normalized differentiation rate
    auto diff_rate = this->collect_from_agents("diff_rate");
	double diff_rate_n = 0;
	if (live_cell_count == 0) diff_rate_n = 0;
    else   diff_rate_n = diff_rate/live_cell_count;
    // normalized proliferation indicator function
    int p_count = 0;
    for (auto & cell:this->agents){
    	if (cell->_hatch._flag){
    		p_count++;
    	};
    }
    // auto p_rate = this->collect_from_agents("diff_rate");
	double p_rate = 0;
	if (live_cell_count == 0) p_rate = 0;
    else   p_rate = p_rate/live_cell_count;

	auto TGF = [&]() {
		auto c_TGF = this->get_GFs("TGF");
		auto DEG = [&]() ->double {
			auto deg =  c_TGF* (1 - this->params["deg_rate_TGF"]);
			return deg;
		};
		auto PROD = [&]()->double {
			auto b = this->params["b_TGF"];
			auto coeff = (b)*c_TGF/ (this->params["K_p_g2"] + c_TGF);
			auto rate_prod = coeff * c_cell ;
			return rate_prod;
		};
		auto CONSUMED = [&]()->double {
			auto c_min = 14;
			auto consumed = p_rate *(c_TGF - c_min);
			return consumed;
		};
		auto BACKGROUND = [&]()->double {
			auto V_max = c_cell*this->params["V_max_base"];
			auto K = this->params["K_b"]; 
			auto background = (V_max*c_TGF)/(K*c_TGF);
			return background;

		};
		auto prod = PROD();
		auto deg = DEG();
		auto consumed = CONSUMED();
		auto background = BACKGROUND();
		auto c_TGF_updated = c_TGF + prod - deg-consumed-background;
		this->set_GFs("TGF", c_TGF_updated);
	};
	TGF();
	
	auto BMP = [&]() {
		auto c_BMP = this->get_GFs("BMP");
		auto DEG = [&]() ->double {
			auto deg_rate = (1-this->params["deg_rate_BMP"])*c_BMP ;
			return deg_rate;
		};
		auto PROD = [&]()->double {
			auto b = this->params["b_BMP"];
			auto coeff = (b*c_BMP) / (this->params["K_p_g1"] + c_BMP);
			auto rate_prod = coeff * c_cell ;
			return rate_prod;
		};
		auto CONSUMED = [&]()->double {
			auto c_min = 0.008;
			auto consumed = diff_rate_n *(c_BMP - c_min);
			return consumed;
		};
		auto BACKGROUND = [&]()->double {
			auto V_max = c_cell*this->params["V_max_base"];
			auto K = this->params["K_b"]; 
			auto background = (V_max*c_BMP)/(K*c_BMP);
			// cout<<" c_c "<<c_cell<<" c_BMP "<<c_BMP<<" background "<<background<<endl;
			return background;

		};
		auto prod = PROD();
		auto deg = DEG();
		auto consumed = CONSUMED();
		auto background = BACKGROUND();
		auto c_updated = c_BMP + prod - deg;
		this->set_GFs("BMP", c_updated);
	};
	BMP();
}
void myEnv::execute_GFs(){
#ifdef DIFFUSION
	this->GFs_diffusion_model();
#else 
	this->GFs_static_model();
#endif // DIFFUSION
	// productions
}
void myEnv::update(){
	Env<myEnv,Cell,myPatch>::update();
	for (auto &[index,patch]:this->patches){
		if (patch->agent_count>1){
			throw patch_availibility("Patch holds more than one agent");
		}
	}
	for (auto &agent:this->agents){
		agent->update();
	}
	this->execute_GFs();
	
}
void myPatch::initialize(){
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
void Cell::inherit(shared_ptr<Cell> father){
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
void Cell::initialize(map<string,double> initial_conditions){
	if (class_name == "Dead"){
		return;
	}
	initial_conditions["pH"] = 7.8;
	initial_conditions["Pr_clock"] = 0;
	initial_conditions["maturity"] = 0;
	initial_conditions["diff_rate"] = 0;
	for (auto const &[key,value]:initial_conditions){
		this->data[key] = value;
	}
	double patch_size = this->myenv->grid_settings["patch_size"];
	double v_patch = patch_size * patch_size;
	
}
