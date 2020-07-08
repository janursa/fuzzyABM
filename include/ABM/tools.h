#include <iostream>
#include <iomanip>
#include <string>
#include <map>
#include <random>
#include <cmath>
#include <type_traits>

namespace tools{

	double random(double min, double max); //!< A random value in the given range

}
inline double tools::random(double min, double max){
	    std::random_device rd;
	    std::mt19937 gen(rd());
	    std::uniform_real_distribution<> dis(min,max);
	    return dis(gen);
}

