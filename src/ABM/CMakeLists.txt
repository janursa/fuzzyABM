
set(HEADER_LIST )

set(SOURCE_FILES "model.cpp")
add_library(${ABMLIB} STATIC ${SOURCE_FILES})
target_link_libraries(${ABMLIB} PRIVATE pybind11::module nlohmann_json::nlohmann_json)
target_link_libraries(${ABMLIB} PRIVATE ${FUZZYLIB})
# target_link_libraries(${ABMLIB} PRIVATE ABMBASE)
target_include_directories(${ABMLIB} PUBLIC ${CMAKE_SOURCE_DIR}/include)
target_include_directories(${ABMLIB} PUBLIC ${CMAKE_SOURCE_DIR}/../)
set_target_properties(${ABMLIB} PROPERTIES POSITION_INDEPENDENT_CODE ON)
source_group(TREE "${ABMLIB}/include" PREFIX "Header Files" FILES ${HEADER_LIST})
