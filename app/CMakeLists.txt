


add_executable(${APP} main.cpp )
target_compile_features(${APP} PRIVATE cxx_std_17)
target_link_libraries(${APP} PRIVATE ${ABMLIB})
target_link_libraries(${APP} PRIVATE pybind11::module)
target_include_directories(${APP}  PUBLIC ${CMAKE_SOURCE_DIR}/include)






