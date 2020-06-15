#include <iostream>
#include "tools.h"
#include "myPyBases.h"
#include "pybases.h"
#include "model.h"
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

PYBIND11_MODULE(myBinds, m) {
	/** Envs **/
	py::bind_vector<AgentsBank>(m,"AgentsBank");
    py::bind_map<PatchesBank>(m,"PatchesBank");
	// link_env<Env,PyEnv<Env>>(m,"Env");
    // link_env<myEnv,PyMyEnv<myEnv>>(m,"myEnv");
	py::class_<Env,PyEnv<Env>,std::shared_ptr<Env>> (m,"Env",py::dynamic_attr())
        .def(py::init<>())
        .def("check",&Env::check)
        .def("place_agent_randomly",&Env::place_agent_randomly)
        .def("setup_domain",&Env::setup_domain)
        .def("step_agents",&Env::step_agents)
        .def("step_patches",&Env::step_patches)
        .def("place_agent",&Env::place_agent)
        .def("update",&Env::update)
        .def("setup_agents",&Env::setup_agents)
        .def("count_agents",&Env::count_agents)
        .def("collect_from_patches",&Env::collect_from_patches)
        .def_readwrite("patches",&Env::patches)
        .def_readwrite("agents",&Env::agents);

    py::class_<myEnv,Env,PyMyEnv<myEnv>,std::shared_ptr<myEnv>> (m,"myEnv",py::dynamic_attr())
        .def(py::init<>())
        .def("check",&myEnv::check)
        .def("place_agent_randomly",&myEnv::place_agent_randomly)
        .def("setup_domain",&myEnv::setup_domain)
        .def("step_agents",&myEnv::step_agents)
        .def("step_patches",&myEnv::step_patches)
        .def("place_agent",&myEnv::place_agent)
        .def("update",&myEnv::update)
        .def("setup_agents",&myEnv::setup_agents)
        .def("count_agents",&myEnv::count_agents)
        .def("collect_from_patches",&myEnv::collect_from_patches)
        .def_readwrite("patches",&myEnv::patches)
        .def_readwrite("agents",&myEnv::agents);
	/** Agent **/
    // link_agent<myAgent,PyMyAgent<myAgent>>(m,"myAgent");
    py::class_<Agent,PyAgent<Agent>,std::shared_ptr<Agent>>(m,"Agent",py::dynamic_attr())
        .def(py::init<shared_ptr<Env>,string>(),"Initialize",py::arg("env"),py::arg("class_name"))
        .def("move",&Agent::move,"Move the agent to a new patch")
        .def("order_hatch",&Agent::order_hatch,"Hatch request",
            py::arg("patch")=nullptr, py::arg("inherit")=false,
            py::arg("quiet")=false, py::arg("reset")=false)
        .def("order_move",&Agent::order_move,"Move request",
            py::arg("patch")=nullptr, 
            py::arg("quiet")=false, py::arg("reset")=false)
        .def("order_switch",&Agent::order_switch,"Switch request",
            py::arg("to"))
        .def_readwrite("disappear",&Agent::disappear)
        .def_readwrite("env",&Agent::env)
        .def_readwrite("data",&Agent::data)
        .def_readwrite("patch",&Agent::patch)
        .def_readwrite("class_name",&Agent::class_name);
    py::class_<myAgent,Agent,PyMyAgent<myAgent>,std::shared_ptr<myAgent>>(m,"myAgent",py::dynamic_attr())
        .def(py::init<shared_ptr<Env>,string>(),"Initialize",py::arg("env"),py::arg("class_name"))
        .def("move",&myAgent::move,"Move the agent to a new patch")
        .def("order_hatch",&myAgent::order_hatch,"Hatch request",
            py::arg("patch")=nullptr, py::arg("inherit")=false,
            py::arg("quiet")=false, py::arg("reset")=false)
        .def("order_move",&myAgent::order_move,"Move request",
            py::arg("patch")=nullptr, 
            py::arg("quiet")=false, py::arg("reset")=false)
        .def("order_switch",&myAgent::order_switch,"Switch request",
            py::arg("to"))
        .def_readwrite("disappear",&myAgent::disappear)
        .def_readwrite("env",&myAgent::env)
        .def_readwrite("data",&myAgent::data)
        .def_readwrite("patch",&myAgent::patch)
        .def_readwrite("class_name",&myAgent::class_name);
    // /** Patch **/
    // // data types
    auto bb = py::bind_map<map<string,double>>(m,"PatchDataBank"); //TODO: needs to go
    bb.def("keys",[](map<string,double> &v) {
       std::vector<std::string> retval;
       for (auto const& element : v) {
         retval.push_back(element.first);
       }
       return retval;
    });
    // link_patch<myPatch,PyMyPatch<myPatch>>(m,"myPatch");
    py::class_<Patch,PyPatch<Patch>,std::shared_ptr<Patch>>(m,"Patch",py::dynamic_attr())
        .def(py::init<shared_ptr<Env>>())
        .def("empty_neighbor", &Patch::empty_neighbor,"Return an empty patch around the patch",
            py::arg("quiet")=false)
        .def("find_neighbor_agents",&Patch::find_neighbor_agents,"Returns a vector of agents in one patch neighborhood",
            py::arg("include_self")=true)
        .def_readwrite("coords",&Patch::coords)
        .def_readwrite("agent",&Patch::agent)
        .def_readwrite("empty",&Patch::empty)
        .def_readwrite("disappear",&Patch::disappear)
        .def_readwrite("data",&Patch::data)
        .def_readwrite("neighbors",&Patch::neighbors);
    py::class_<myPatch,Patch,PyMyPatch<myPatch>,std::shared_ptr<myPatch>>(m,"myPatch",py::dynamic_attr())
        .def(py::init<shared_ptr<Env>>())
        .def("empty_neighbor", &myPatch::empty_neighbor,"Return an empty patch around the patch",
            py::arg("quiet")=false)
        .def("find_neighbor_agents",&myPatch::find_neighbor_agents,"Returns a vector of agents in one patch neighborhood",
            py::arg("include_self")=true)
        .def_readwrite("coords",&myPatch::coords)
        .def_readwrite("agent",&myPatch::agent)
        .def_readwrite("empty",&myPatch::empty)
        .def_readwrite("disappear",&myPatch::disappear)
        .def_readwrite("data",&myPatch::data)
        .def_readwrite("neighbors",&myPatch::neighbors);
    // /** Exceptions **/
    register_exceptions(m);
    /** mesh **/
    register_mesh(m);

}




