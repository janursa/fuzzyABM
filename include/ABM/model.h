#pragma once
#include "CPPYABM/bases.h"
using namespace std;
struct Patch;
struct myAgent : public Agent{
	myAgent(shared_ptr<Env> env , string class_name)
	try: Agent(env,class_name){
		
	}catch(...){
		cerr<<"Error in the construction of my agent";
		exit(2);
	}
};
struct myEnv : public Env{
};
struct myPatch : public Patch{
	myPatch(shared_ptr<Env> env)
	try: Patch(env){
	}catch (...){
		cerr<<"Error in the construction of my patch";
		exit(2);
	}
};
