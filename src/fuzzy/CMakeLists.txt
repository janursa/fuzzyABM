

add_library(${FUZZYLIB} STATIC fuzzy.cpp)
target_include_directories(${FUZZYLIB} PUBLIC ${CMAKE_SOURCE_DIR}/include/)
target_link_libraries(${FUZZYLIB} ${FUZZYLITE})
