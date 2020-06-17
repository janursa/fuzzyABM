#pragma once
#include "CPPYABM/bases.h"
#include "tools.h"
using namespace std;
struct Patch;
struct Dead: public Agent{
	Dead(shared_ptr<Env> env , string class_name)
	try: Agent(env,class_name){
		
	}catch(...){
		cerr<<"Error in the construction of my agent";
		exit(2);
	}

};
struct MSC : public Agent{
	MSC(shared_ptr<Env> env , string class_name, 
		std::map<string,double> params_,std::map<string,double> initial_conditions,
		unsigned id_)
	try: Agent(env,class_name){
		this->params = params_;
		this->initial_conditions = initial_conditions;
		this->initialize(initial_conditions);
		this->id = id_;
	}catch(...){
		cerr<<"Error in the construction of my agent";
		exit(2);
	}
	void initialize(map<string,double> initial_conditions);

	std::map<string,double> params;
	std::map<string,double> initial_conditions;
	py::object policy;
	bool proliferation(double Pr);
	bool mortality(double Mo);
	double adaptation();
	double alkalinity();
	bool migration(double Mi);
	virtual std::map<string,double> run_policy(std::map<string,double> ) = 0;
	virtual void step();
	unsigned id;
	virtual double get_data(string tag){
		return this->data[tag];
	}

	map<string,double> collect_policy_inputs();
	virtual void inherit(shared_ptr<Agent> father);
	map<string,double> data;
};
struct myEnv : public Env{
	/** Env data **/
	using param_type = map<string,double>;
   double collect_from_patches(string tag);
   void set_settings(py::dict settings_){
   		this->settings = settings_;
   }
   void set_params(param_type params_){
   		this->params = params_;
   }
   virtual shared_ptr<Patch> generate_patch();
   py::dict settings;
   param_type params;

};
struct myPatch : public Patch{
	myPatch(shared_ptr<Env> env,std::map<string,double> params_,std::map<string,double> initial_conditions)
	try: Patch(env){
		this->params = params_;
		this->initial_conditions = initial_conditions;
		this->initialize(initial_conditions);
	}catch (...){
		cerr<<"Error in the construction of my patch";
		exit(2);
	}
	virtual double get_data(string tag){
		return this->data[tag];
	}
	std::map<string,double> params;
	std::map<string,double> initial_conditions;
	double pH();
	double lactate();
	virtual void initialize(map<string,double> configs);
	virtual void step();
	map<string,double> data;
};
