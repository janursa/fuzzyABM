#include <iostream>
#include "CPPYABM/tools.h"
#include "mypybases.h"
#include "CPPYABM/pybases.h"
#include "model.h"
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

PYBIND11_MODULE(myBinds, m) {
	/** Envs **/
	// data type
	py::bind_vector<AgentsBank>(m,"AgentsBank");
    py::bind_map<PatchesBank>(m,"PatchesBank");
    // class
	expose_base_env(m);
	expose_env<myEnv,PyMyEnv<myEnv>>(m,"myEnv");
	/** Agent **/
    expose_base_agent(m);
    expose_agent<myAgent,PyMyAgent<myAgent>>(m,"myAgent");

    /** Patch **/
    // data types
    auto bb = py::bind_map<map<string,double>>(m,"PatchDataBank"); //TODO: needs to go
    bb.def("keys",[](map<string,double> &v) {
       std::vector<std::string> retval;
       for (auto const& element : v) {
         retval.push_back(element.first);
       }
       return retval;
    });
    // class
    expose_base_patch(m);
    expose_patch<myPatch,PyMyPatch<myPatch>>(m,"myPatch");
    // /** Exceptions **/
    register_exceptions(m);
    /** mesh **/
    register_mesh(m);
}




