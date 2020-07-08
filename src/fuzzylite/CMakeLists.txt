
file(GLOB_RECURSE source_list "src/*.cpp" )
add_library(${FUZZYLITE} STATIC ${source_list})
target_include_directories(${FUZZYLITE} PUBLIC ${CMAKE_SOURCE_DIR}/include)
