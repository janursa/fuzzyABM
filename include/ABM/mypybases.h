#pragma once
#include "CPPYABM/pybases.h"
#include "model.h"
using namespace std;
template<class derivedEnv>
class PyMyEnv: public PyEnv<derivedEnv>{
	using PyEnv<derivedEnv>::PyEnv;
	
};
template<class derivedAgent>
class PyMSC: public PyAgent<derivedAgent>{
	using PyAgent<derivedAgent>::PyAgent;
	using input_output = std::map<string,double>;
	input_output run_policy(input_output inputs) override {
		PYBIND11_OVERLOAD_PURE(
			input_output,
			derivedAgent,
			run_policy,
			inputs
		);
	}
	void reward() override {
		PYBIND11_OVERLOAD(
			void,
			derivedAgent,
			reward
		);
	}
	void step() override {
		PYBIND11_OVERLOAD(
			void,
			derivedAgent,
			step
		);
	}
};
template<class derivedAgent>
class PyDead: public PyAgent<derivedAgent>{
	using PyAgent<derivedAgent>::PyAgent;
};
template<class derivedPatch>
class PyMyPatch: public PyPatch<derivedPatch>{
	using PyPatch<derivedPatch>::PyPatch;
};
