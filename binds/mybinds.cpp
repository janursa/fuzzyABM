#include <iostream>
#include "CppyABM/include/ABM/bind_tools.h"
#include "model.h"
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
class PyCell: public Cell{
    using Cell::Cell;
    using input_output = std::map<string,double>;
    input_output run_policy(input_output inputs) override {
        PYBIND11_OVERLOAD(
            input_output,
            Cell,
            run_policy,
            inputs
        );
    }
    void reward() override {
        PYBIND11_OVERLOAD(
            void,
            Cell,
            reward
        );
    }
    void step() override {
        PYBIND11_OVERLOAD(
            void,
            Cell,
            step
        );
    }
};
/** data types **/
EXPOSE_AGENT_CONTAINER(Cell);
EXPOSE_PATCH_CONTAINER(myPatch);
PYBIND11_MODULE(myBinds, m) {
	/** defaults **/
    bind_tools::expose_defaults<myEnv,Cell,myPatch>(m);
    /** Envs **/
	auto myEnv_binds = bind_tools::expose_env<myEnv,Cell,myPatch, bind_tools::tramEnv<myEnv,Cell,myPatch>>(m,"myEnv");
    myEnv_binds.def("collect_from_patches",&myEnv::collect_from_patches);
    myEnv_binds.def("collect_from_agents", &myEnv::collect_from_agents);
    myEnv_binds.def("set_GFs", &myEnv::set_GFs);

    myEnv_binds.def("get_GFs", &myEnv::get_GFs);
    // myEnv_binds.def("set_settings",&myEnv::set_settings);
    myEnv_binds.def("set_params",&myEnv::set_params);
    myEnv_binds.def("set_settings", &myEnv::set_settings);
    myEnv_binds.def("construct_policy", &myEnv::construct_policy);
    myEnv_binds.def("get_tick", &myEnv::get_tick);
    myEnv_binds.def("set_tick", &myEnv::set_tick);
    myEnv_binds.def("increment_tick", &myEnv::increment_tick);
    myEnv_binds.def("setup_agents", &myEnv::setup_agents);
	/** Agent **/
    auto Cell_binds = bind_tools::expose_agent<myEnv,Cell,myPatch,PyCell>(m,"Cell");
    Cell_binds.def(py::init<shared_ptr<myEnv>,
                    string,
                    std::map<string,double>,
                    std::map<string,double>>(),
                    "Initialize",py::arg("env"),py::arg("class_name"),
                    py::arg("params"),py::arg("initial_conditions")
                    );
    Cell_binds.def("mortality",&Cell::mortality);
    Cell_binds.def("alkalinity",&Cell::alkalinity);
    Cell_binds.def("adaptation",&Cell::adaptation);
    Cell_binds.def("proliferation",&Cell::proliferation);
    Cell_binds.def("migration",&Cell::migration);
    Cell_binds.def("collect_policy_inputs",&Cell::collect_policy_inputs);
    /** Patch **/
    auto myPatch_binds = bind_tools::expose_patch<myEnv,Cell,myPatch>(m,"myPatch");
    myPatch_binds.def(py::init<shared_ptr<myEnv>,
                    MESH_ITEM,
                    std::map<string,double>,
                    std::map<string,double>,
                    std::map<string, bool>>(),
                    "Initialize",py::arg("env"),py::arg("mesh"),
                    py::arg("params"),py::arg("initial_conditions"), py::arg("flags"));
    myPatch_binds.def("initialize",&myPatch::initialize);

}




