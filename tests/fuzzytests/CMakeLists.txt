

# Tests need to be added as executables first
add_executable(${FUZZYTESTS} testfuzzy.cpp)

# I'm using C++17 in the test
target_compile_features(${FUZZYTESTS} PRIVATE cxx_std_17)

# Should be linked to the main library, as well as the Catch2 testing library
target_link_libraries(${FUZZYTESTS} PRIVATE ${FUZZYLIB} Catch2::Catch2 )
target_include_directories(${FUZZYTESTS} PUBLIC ${CMAKE_SOURCE_DIR}/include)

# If you register a test, then ctest and make test will run it.
# You can also run examples and check the output, as well.
add_test(NAME ${FUZZYTESTS}_test COMMAND ${FUZZYTESTS}) # Command can be a target
