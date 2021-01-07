#pragma once
#include "CppyABM/include/ABM/bases.h"
#include "tools.h"
#include "fuzzy/fuzzy.h"

using namespace std;
struct myPatch;
struct Cell;
struct myEnv : public  Env<myEnv,Cell,myPatch> {
	/** Env data **/
	
	void construct_policy() {
		try {
			this->policy = make_shared<fuzzy>("MSC", this->params);
		}
		catch (invalid_fuzzy_definition& e) {
		    cout<<"cool up to here"<<endl;
			throw e;

		}
	}
	
	using param_type = map<string, double>;
	double collect_from_patches(string tag);
	double collect_from_agents(string tag);
	virtual void setup_agents(map<string, unsigned> config);
	void set_settings(map<string, double> grid_settings) {
		this->grid_settings = grid_settings;
		
	}
	void set_params(param_type params_) {
		this->params = params_;
	}
	
	//virtual shared_ptr<Patch> generate_patch();
	virtual void update();
	param_type params;
	shared_ptr<fuzzy> policy;
	map<string,double> grid_settings;
	map<string, double> GFs;
	void set_GFs(string tag, double value) {
		GFs[tag] = value;
	}
	double get_GFs(string tag) {
		return GFs[tag];
	}
	unsigned tick;
	void increment_tick() {
		tick++;
	}
	unsigned get_tick() {
		return tick;
	}
	void  set_tick(unsigned value) {
		tick = value;
	}
};
// struct Dead: public Agent{
// 	Dead(shared_ptr< Env> env , string class_name)
// 	try: Agent(env,class_name){
		
// 	}catch(...){
// 		cerr<<"Error in the construction of my agent";
// 		exit(2);
// 	}

// };
struct Cell : public  Agent<myEnv,Cell,myPatch> {
	using  Agent<myEnv,Cell,myPatch>:: Agent;
	Cell(shared_ptr<myEnv> env , string class_name, 
		std::map<string,double> params_,std::map<string,double> initial_conditions)
	try:  Agent(env,class_name){
		myenv = env;
		this->params = params_;
		this->initial_conditions = initial_conditions;
		this->initialize(initial_conditions);
	}catch(...){
		cerr<<"Error in the construction of Cell";
		exit(2);
	}
	void initialize(map<string,double> initial_conditions);

	std::map<string,double> params;
	std::map<string,double> initial_conditions;
	bool proliferation(double Pr);
	bool mortality(double Mo);
	double adaptation();
	double alkalinity();
	void differentiation(double , double);
	void bone_production(double, double); // for ECM and minerals

	bool migration(double Mi);
	virtual void step();
	virtual double get_data(string tag){
		return this->data[tag];
	}
	virtual void set_data(string tag, double value) {
		this->data[tag] = value;
	}

	map<string,double> collect_policy_inputs();
	virtual void inherit(shared_ptr<Cell> father);
	map<string,double> data;
	virtual void reward() {};
	virtual void update();
	
	virtual std::map<string, double> run_policy(std::map<string, double> inputs) {
		auto predictions = this->myenv->policy->predict(inputs);
		return predictions;
	}
	double logic_function(double x) {
		return (2.0 / (1.0 + exp(-8.0 * (x - 0.5))));
	};
	shared_ptr<myEnv> myenv;
	bool damage = false;
	bool cycled = false; // is true if cell just did mitosis
	//double v_p_v; //v_patch/v_domain
};

struct myPatch : public  Patch<myEnv,Cell,myPatch> {
	using  Patch<myEnv,Cell,myPatch>:: Patch;
	myPatch(shared_ptr<myEnv> env,std::map<string,double> params_,std::map<string,double> initial_conditions, std::map<string, bool> flags)
	try:  Patch(env){
		this->params = params_;
		this->initial_conditions = initial_conditions;
		this->flags = flags;
		this->initialize();
	}catch (...){
		cerr<<"Error in the construction of my patch";
		exit(2);
	}
	virtual double get_data(string tag){
		return this->data[tag];
	}
	virtual void set_data(string tag, double value) {
		this->data[tag] = value;
	}
	std::map<string,double> params;
	std::map<string,double> initial_conditions;
	std::map<string, bool> flags;
	double pH();
	double lactate();
	virtual void initialize();
	virtual void step();
	map<string,double> data;
};
