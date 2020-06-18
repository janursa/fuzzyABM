# CMAKE_MINIMUM_REQUIRED(VERSION 3.13.1)
# for testing
set(HEADER_LIST )

set(SOURCE_FILES "model.cpp"
				 "mypybases.cpp")

set (CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/CMake")

add_library(${STATICLIBS} STATIC ${SOURCE_FILES})
target_link_libraries(${STATICLIBS} PRIVATE pybind11::module)
target_link_libraries(${STATICLIBS} PRIVATE "${CMAKE_SOURCE_DIR}/../CPPYABM/build/src/libABM.a")
# target_link_libraries(${STATICLIBS} PRIVATE CPPYABM.a)
target_include_directories(${STATICLIBS} PUBLIC ${CMAKE_SOURCE_DIR}/include/ABM)
set_target_properties(${STATICLIBS} PROPERTIES POSITION_INDEPENDENT_CODE ON)
target_include_directories(${STATICLIBS} PUBLIC "${CMAKE_SOURCE_DIR}/../CPPYABM/include/")
source_group(TREE "${PROJECT_SOURCE_DIR}/include" PREFIX "Header Files" FILES ${HEADER_LIST})
