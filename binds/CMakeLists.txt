# CMAKE_MINIMUM_REQUIRED(VERSION 3.13.1)
# for testing
set(HEADER_LIST )

SET(MODULE_NAME "myBinds")

set (CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/CMake")

pybind11_add_module(${MODULE_NAME} mybinds.cpp ${HEADER_LIST})
target_link_libraries(${MODULE_NAME} PRIVATE pybind11::module)
target_link_libraries(${MODULE_NAME} PRIVATE "${CMAKE_SOURCE_DIR}/../CPPYABM/build/src/libABM.a")
target_link_libraries(${MODULE_NAME} PRIVATE ${STATICLIBS})
target_include_directories(${MODULE_NAME} PUBLIC ${CMAKE_SOURCE_DIR}/include/ABM)
target_include_directories(${MODULE_NAME} PUBLIC "${CMAKE_SOURCE_DIR}/../CPPYABM/include/")

source_group(TREE "${PROJECT_SOURCE_DIR}/include" PREFIX "Header Files" FILES ${HEADER_LIST})
