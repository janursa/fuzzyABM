#include <iostream>
#include <iomanip>
#include <string>
#include <map>
#include <random>
#include <cmath>

namespace tools{

	float random(float min, float max); //!< A random value in the given range
}
inline float tools::random(float min, float max){
	    std::random_device rd;
	    std::mt19937 gen(rd());
	    std::uniform_real_distribution<> dis(min,max);
	    return dis(gen);
}