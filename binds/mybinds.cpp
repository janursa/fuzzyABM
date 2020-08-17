#include <iostream>
#include "CPPYABM/include/ABM/bind_tools.h"
#include "mypybases.h"
#include "CPPYABM/include/ABM/pybases.h"
#include "model.h"
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>

PYBIND11_MODULE(myBinds, m) {
	/** Envs **/
    expose_defaults(m);
	// data type
    // expose_containers(m);   
    // class
	// expose_base_env(m);
	auto myEnv_binds = expose_env<myEnv,PyMyEnv<myEnv>>(m,"myEnv");
    myEnv_binds.def(py::init<>());
    myEnv_binds.def("collect_from_patches",&myEnv::collect_from_patches);
    myEnv_binds.def("collect_from_agents", &myEnv::collect_from_agents);
    // myEnv_binds.def("set_settings",&myEnv::set_settings);
    myEnv_binds.def("set_params",&myEnv::set_params);
    myEnv_binds.def("set_settings", &myEnv::set_settings);
    myEnv_binds.def("construct_policy", &myEnv::construct_policy);
    myEnv_binds.def("get_tick", &myEnv::get_tick);
    myEnv_binds.def("set_tick", &myEnv::set_tick);
    myEnv_binds.def("increment_tick", &myEnv::increment_tick);
	/** Agent **/
    // MSC
    // expose_base_agent(m);
    auto MSC_binds = expose_agent<MSC,PyMSC<MSC>>(m,"MSC");
    MSC_binds.def("mortality",&MSC::mortality);
    MSC_binds.def(py::init<shared_ptr<myEnv>,
                    string,
                    std::map<string,double>,
                    std::map<string,double>>(),
                    "Initialize",py::arg("env"),py::arg("class_name"),
                    py::arg("params"),py::arg("initial_conditions")
                    );
    MSC_binds.def("alkalinity",&MSC::alkalinity);
    MSC_binds.def("adaptation",&MSC::adaptation);
    MSC_binds.def("proliferation",&MSC::proliferation);
    MSC_binds.def("migration",&MSC::migration);
    MSC_binds.def("collect_policy_inputs",&MSC::collect_policy_inputs);
    // Dead
    auto Dead_binds = expose_agent<Dead,PyDead<Dead>>(m,"Dead");
    Dead_binds.def(py::init<shared_ptr<Env>,string>(),"Initialize",py::arg("env"),py::arg("class_name"));
    /** Patch **/
    // expose_base_patch(m);
    auto myPatch_binds = expose_patch<myPatch,PyMyPatch<myPatch>>(m,"myPatch");
    myPatch_binds.def(py::init<shared_ptr<Env>,
                    std::map<string,double>,
                    std::map<string,double>>(),
                    "Initialize",py::arg("env"),
                    py::arg("params"),py::arg("initial_conditions"));
    myPatch_binds.def("initialize",&myPatch::initialize);
    // /** Exceptions **/
    // expose_exceptions(m);
    /** mesh **/
    // expose_mesh(m);
}




