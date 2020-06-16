#pragma once
#include "CPPYABM/pybases.h"
#include "model.h"
using namespace std;
template<class derivedEnv>
class PyMyEnv: public PyEnv<derivedEnv>{
	using PyEnv<derivedEnv>::PyEnv;
	
};
template<class derivedAgent>
class PyMyAgent: public PyAgent<derivedAgent>{
	using PyAgent<derivedAgent>::PyAgent;
};
template<class derivedPatch>
class PyMyPatch: public PyPatch<derivedPatch>{
	using PyPatch<derivedPatch>::PyPatch;
};
