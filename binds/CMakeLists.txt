# CMAKE_MINIMUM_REQUIRED(VERSION 3.13.1)
# for testing
set(HEADER_LIST )


pybind11_add_module(${BINDSMODULE} mybinds.cpp ${HEADER_LIST})
target_link_libraries(${BINDSMODULE} PRIVATE pybind11::module)
target_link_libraries(${BINDSMODULE} PRIVATE ${ABMLIB})

target_include_directories(${BINDSMODULE} PUBLIC ${CMAKE_SOURCE_DIR}/include/ABM)

source_group(TREE "${PROJECT_SOURCE_DIR}/include" PREFIX "Header Files" FILES ${HEADER_LIST})
