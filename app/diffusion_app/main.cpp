#include "diffusion/diffusion.h"
//#include "tools/global.h"

template <int dim>
std::vector<double> getRandomInitialValues(unsigned int sz)
{
    unsigned int nComp = std::pow(sz, dim);
    std::vector<double> vecInitVals(nComp);

    double min = 0.008;
    double max = 0.05;

    double avg = (min + max) / 2;
    double dg = (max - min) / 2;

    std::transform(vecInitVals.begin(), vecInitVals.end(), vecInitVals.begin(), 
        [avg, dg] (const double /*v*/) {
            double r = ((double) rand() / (RAND_MAX));
            double v = avg + dg*2*(0.5 - r);
            return v;
        });

    return vecInitVals;
}

constexpr int p_dim = 2;

int main(int argc, char** argv)
{
    std::string savePath;
    if (argc < 2) {
        std::cout << "NOTICE: no VTK save path has been specified, so the data won't be stored" << std::endl;
        std::cout << "    [path] - a path for saving VTK files as an argument" << std::endl;
    } else {
        savePath = argv[1];
        std::cout << "NOTICE: debug output will be saved to " << savePath << std::endl;
    }
    
    dealii::Utilities::MPI::MPI_InitFinalize mpi_initialization(argc, argv);
    std::cout << "    Number of cores       = " << dealii::MultithreadInfo::n_cores() << std::endl;
    std::cout << "    Number of threads     = " << dealii::MultithreadInfo::n_threads() << std::endl;
    std::cout << "    Is single thread mode = " << (dealii::MultithreadInfo::is_running_single_threaded() ? "yes" : "no") << std::endl;
    
    TOOLS::initGlobals();

    // Model settings
    double length = 1;
    double patch_size = 0.008;//0.5 // for Debug
    double D4 = 1.65 / 24;
    double D1 = 0.22e-2 / 24;
    double timeEnd = 1;
    double timeStepInit = 1e-1;

    ABM<p_dim> problem(length, patch_size, D1, D4, savePath);

    // Initial values - auto generation for debug
    // In reality should be a vector<double>
    auto sz = static_cast<unsigned int>(ceil(length / patch_size)) + 1;
    std::vector<double> vecInitVals = getRandomInitialValues<p_dim>(sz);

    // First call
    // returns a vector<double>
    std::vector<double> results = problem.run(vecInitVals, timeStepInit, timeEnd);

    // Second call just for demonstration
    results = problem.run(vecInitVals, timeStepInit, timeEnd);

    TOOLS::timer::instance().print_summary();
}
