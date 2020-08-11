#include "abm.h"

#include "applications/common.h"

#include "core/analysis_transient.h"
#include "core/solver_direct.h"
#include "core/solver_newton_raphson.h"
#include "core/timestep_selector_fixed_factor.h"
#include "core/action_matrix_solver.h"
#include "core/action_pipeline.h"
#include "core/triangulation_output.h"
#include "core/convergence_tester_residual.h"
#include "core/linear_soe.h"
#include "core/assembly_strategy_sequential.h"
#include "core/point_data_map.h"

#include "kernels/time_derivative.h"
#include "kernels/diffusion.h"
#include "kernels/functional_reaction.h"
#include "kernels/boundary_diffusion.h"

#include "pde/postprocessor.h"
#include "pde/quantity_variable_value.h"
#include "pde/quantity_variable_time_derivative.h"
#include "pde/sensor_scalar.h"
#include "pde/field_interpolator.h"
#include "pde/qpoints_output.h"
#include "pde/builders.h"

#include <deal.II/base/function_lib.h>
#include <deal.II/base/table.h>
#include <deal.II/base/quadrature_lib.h>

// Exponential growth
template <int dim>
ABM<dim>::ExponentialGrowth::ExponentialGrowth(double D, std::shared_ptr<const CORE::ModelBase> model)
    : _model(model)
    , _D(D)
{}

template <int dim>
double ABM<dim>::ExponentialGrowth::f(const PDE::VariableValues<dim>& /*variablesValues*/, unsigned int /*qp*/) const
{
    double t = _model->getCurrentTime();
    return std::exp(_D*t);
}

template <int dim>
double ABM<dim>::ExponentialGrowth::df(const PDE::VariableValues<dim>& /*variablesValues*/, std::shared_ptr<const PDE::Variable<dim>> /*ivar*/,
    unsigned int /*qp*/) const
{
    return 0;
}

template <int dim>
double ABM<dim>::ExponentialGrowth::d2f(const PDE::VariableValues<dim>& /*variablesValues*/, std::shared_ptr<const PDE::Variable<dim>> /*ivar*/,
    std::shared_ptr<const PDE::Variable<dim>> /*jvar*/, unsigned int /*qp*/) const
{
    return 0;
}

// Diffusivity
template <int dim>
ABM<dim>::Diffusivity::Diffusivity(double D)
    : _D(D)
{}

template <int dim>
double ABM<dim>::Diffusivity::f(const PDE::VariableValues<dim>& /*variablesValues*/, unsigned int /*qp*/) const
{
    return _D;
}

template <int dim>
double ABM<dim>::Diffusivity::df(const PDE::VariableValues<dim>& /*variablesValues*/, std::shared_ptr<const PDE::Variable<dim>> /*ivar*/,
    unsigned int /*qp*/) const
{
    return 0;
}

template <int dim>
double ABM<dim>::Diffusivity::d2f(const PDE::VariableValues<dim>& /*variablesValues*/, std::shared_ptr<const PDE::Variable<dim>> /*ivar*/,
    std::shared_ptr<const PDE::Variable<dim>> /*jvar*/, unsigned int /*qp*/) const
{
    return 0;
}

// Main model itself
template <int dim>
ABM<dim>::ABM(double length, double patch_size, double D1, double D4, std::string savePath)
{
    _triangulation = createMesh(length, patch_size);

    // Linear solver - common for all problems
    unsigned int maxIter = 1000;
    double absTol = 1e-8;
    double relTol = 1e-8;
    auto linearSolver = std::make_shared<LinearSolverType<VectorType, MatrixType>>(maxIter, absTol, relTol);

    _model = std::make_shared<PDE::ModelWithKernels<dim, VectorType>>();

    auto gVar = _model->getSystem().createVariable("g", true);

    // 1. Growth kernel
    auto growth = std::make_shared<ExponentialGrowth>(D4, _model);
    auto krnlGrowth = std::make_shared<PDE::KernelFunctionalReaction<double, dim>>(gVar, growth);
    _model->getSystem().addKernel(krnlGrowth);

    // 2. Time derivative
    auto krnlTimeDer = std::make_shared<PDE::KernelTimeDerivative<dim>>(gVar, _model);
    _model->getSystem().addKernel(krnlTimeDer);

    // Diffusivity
    auto diffusivity = std::make_shared<Diffusivity>(D1);
    using TypeMobility = std::remove_reference_t<decltype(*diffusivity)>;

    // 3. Domain diffusion
    auto krnlDiffusion = std::make_shared<PDE::KernelDiffusion<typename TypeMobility::ReturnType, dim>>(gVar, diffusivity);
    _model->getSystem().addKernel(krnlDiffusion);

    // 4. Boundary diffusion
    auto bndrDiffusion = std::make_shared<PDE::BoundaryKernelDiffusion<typename TypeMobility::ReturnType, dim>>(gVar, diffusivity);
    _model->getSystem().addKernel(bndrDiffusion);

    // Apply periodic boundary conditions
    setPeriodicBoundaryCondtions(_model, *_triangulation);

    // System assembly strategy - separate for each model
    auto assemblyStrategy
        = std::make_shared<CORE::AssemblyStrategySequential<dim, VectorType, MatrixType, std::remove_reference_t<decltype(*_model)>>>(_model);

    // We create linear SOE explicitly
    auto linearSOE = std::make_shared<CORE::LinearSOE<VectorType, MatrixType>>();

    // Nonlinear solver
    std::shared_ptr<CORE::NonlinearSolver<dim, VectorType, MatrixType>> nonlinearSolver;
    if (_isNonlinear) {
        // Newton solver
        double absTolNewton = 1e-8;
        unsigned int iterMax = 10;
        auto convergenceTester = std::make_shared<CORE::ConvergenceTesterResidual<VectorType, MatrixType>>(linearSOE, absTolNewton);
        nonlinearSolver = std::make_shared<CORE::SolverNewtonRaphson<dim, VectorType, MatrixType>>(iterMax, assemblyStrategy, linearSolver, convergenceTester);
    } else {
        // Linear one-step solver
        nonlinearSolver = std::make_shared<CORE::SolverDirect<dim, VectorType, MatrixType>>(assemblyStrategy, linearSolver);
    }

    // Create problem set
    _problemSet = std::make_shared<CORE::ProblemSet<dim, VectorType>>();
    _manager = std::make_shared<CORE::ActionsManager<dim, VectorType>>();

    // Create problems
    _problem = std::make_shared<CORE::Problem<dim, VectorType>>("ABM", _model, _triangulation, _problemSet);

    // 1. Apply initial conditions
    _fieldInterpolator = std::make_shared<PDE::FieldInterpolator<dim, VectorType>>();
    _manager->appendOpenTimeAction( std::make_shared<CORE::ActionPipeline<dim, VectorType>>(_problem, _fieldInterpolator) );

    // 2. Solve
    _manager->appendAction( std::make_shared<CORE::ActionMatrixSolver<dim, VectorType, MatrixType>>(_problem, nonlinearSolver, linearSOE) );

    // 3. Transfer state
    auto modelTransfer = std::make_shared<PDE::ModelWithVariables<dim, VectorType>>();
    auto tVar = modelTransfer->getSystem().createVariable("t", true);

    auto stateTransfer = std::make_shared<PDE::StateTransfer<dim, VectorType>>(
        std::move(PDE::buildStateTransfer<dim, VectorType>(_problem, {gVar}, {tVar}))
    );

    auto quadCell = std::make_shared<dealii::QTrapez<dim>>();
    auto quadFace = std::make_shared<dealii::QTrapez<dim-1>>();
    auto problemTransfer = std::make_shared<CORE::Problem<dim, VectorType>>("Transfer",
        modelTransfer, quadCell, quadFace, _triangulation, _problemSet);
    _manager->appendAction( std::make_shared<CORE::ActionPipeline<dim, VectorType>>(problemTransfer, stateTransfer) );

    // Output manager
    auto outputManager = std::make_shared<CORE::OutputManager>();

    // Vector with output variables
    _mapOutput = std::make_shared<CORE::PointDataMap<dim>>();

    // Add ouput to quadrature points
    auto qoutput = std::make_shared<PDE::QPointsOutput<dim, VectorType>>(problemTransfer, modelTransfer, _mapOutput);

    // Add t to output
    auto qtyT = std::make_shared<PDE::QuantityVariableValue<dim>>(tVar);
    auto sensT = std::make_shared<PDE::SensorScalar<dim>>(qtyT);
    qoutput->addSensor(sensT);

    outputManager->addOutput(qoutput);

    
    if (!savePath.empty()) {
        // Output objects
        auto output = std::make_shared<CORE::TriangulationOutput<dim, VectorType>>(_triangulation, savePath);

        // Build postprocessor
        auto postprocessor = std::make_shared<PDE::Postprocessor<dim, VectorType>>(_problem, _model);

        // Add g to output
        auto qtyG = std::make_shared<PDE::QuantityVariableValue<dim>>(gVar);
        auto sensG = std::make_shared<PDE::SensorScalar<dim>>(qtyG);
        postprocessor->addSensor(sensG);

        // Add postprocessor
        output->addPostprocessor(postprocessor);
        outputManager->addOutput(output);
    }

    // Timestep selector settings
    double timestepGrowthFactor = 1.0;
    auto timestepSelector = std::make_shared<CORE::TimestepSelectorFixedFactor>(timestepGrowthFactor);

    // Analysis settings
    _analysis = std::make_shared<CORE::AnalysisTransient<dim, VectorType>>(outputManager, timestepSelector);
}

template <int dim>
std::vector<double> ABM<dim>::run(std::vector<double> vecInitVals, double timeStepInit, double timeEnd)
{
    // Initial values
    std::array<std::pair<double, double>, dim> interval_endpoints;
    interval_endpoints.fill(std::make_pair(0, _geometry.length));
    
    std::array<unsigned int, dim> n_subintervals;
    n_subintervals.fill(_geometry.div);

    dealii::TableIndices<dim> indices;
    for(unsigned int i=0; i<dim; i++) {
        indices[i] = _geometry.div + 1;
    }
    dealii::Table<dim, double> table;
    table.reinit(indices);

    if(table.n_elements() != vecInitVals.size()) {
        throw std::runtime_error("Wrong number of values in the provided vector, size = "
                + dealii::Utilities::int_to_string(vecInitVals.size()) 
                + ", needed = "
                + dealii::Utilities::int_to_string(table.n_elements()));
    }

    table.fill(&*vecInitVals.begin());

    auto initialValues = std::make_shared<dealii::Functions::InterpolatedUniformGridData<dim>>(interval_endpoints, n_subintervals, table);

    // Debug
    //auto initialValues = std::make_shared<InitialValues<dim>>();

    // Set initial conditions
    _fieldInterpolator->applyInterpolation(initialValues);

    double timeStart = 0;
    //double timeEnd = 1;
    //double timeStepInit = 1e-1;
    double timeStepMin = 1e-1 * timeStepInit;
    double timeStepMax = 1e1 * timeStepInit;

    _analysis->analyze(_manager, timeStart, timeEnd, timeStepInit, timeStepMin, timeStepMax);

    // Convert the results into the vector
    std::vector<double> vecResults;
    for(auto& [pt, qvals] : _mapOutput->data()) {
        (void)pt;
        vecResults.push_back(qvals[0]);
    }

    return vecResults;
}

template <int dim>
std::shared_ptr<Triangulation<dim>> ABM<dim>::createMesh(double length, double patch_size)
{
    TOOLS::cout::instance() << "Generating initial mesh ..." << std::endl;

    auto div = static_cast<unsigned int>(ceil(length / patch_size));

    // Save geometry info
    _geometry = {length, div};

    std::vector<unsigned int> subdivisions(dim, div);

    const dealii::Point< dim > bottom_left;
    const dealii::Point< dim > top_right = (dim == 2 ?
        dealii::Point<dim>(length, length) :
        dealii::Point<dim>(length, length, length));

    auto triangulation = createTriaPtr<dim>();

    dealii::GridGenerator::subdivided_hyper_rectangle(*triangulation,
        subdivisions,
        bottom_left,
        top_right);

    /* Mark boundaries
                  3
            ------------
            |          |
          0 |          | 1
            |          |
            ------------ x
                  2
        3D:
        4 - Z bottom
        5 - Z top
    */
    for (const auto &cell : triangulation->active_cell_iterators()) {
        for (unsigned int face = 0; face < dealii::GeometryInfo<dim>::faces_per_cell; ++face) {

            if (std::fabs(cell->face(face)->center()(0) - 0) < 1e-8) {
                // left face
                cell->face(face)->set_boundary_id(0);
            } else if (std::fabs(cell->face(face)->center()(0) - length) < 1e-8) {
                // right face
                cell->face(face)->set_boundary_id(1);
            } else if (std::fabs(cell->face(face)->center()(1) - 0) < 1e-8) {
                // bottom face
                cell->face(face)->set_boundary_id(2);
            } else if (std::fabs(cell->face(face)->center()(1) - length) < 1e-8) {
                // top face
                cell->face(face)->set_boundary_id(3);
            } else {
                if (dim == 3) {
                    if (std::fabs(cell->face(face)->center()(2) - 0) < 1e-8) {
                        // Z bottom face
                        cell->face(face)->set_boundary_id(4);
                    } else if (std::fabs(cell->face(face)->center()(2) - length) < 1e-8) {
                        // Z top face
                        cell->face(face)->set_boundary_id(5);
                    }
                }
            }
        }
    }

    return triangulation;
}

template <int dim>
void ABM<dim>::setPeriodicBoundaryCondtions(std::shared_ptr<CORE::Model<dim, VectorType>> model,
    Triangulation<dim>& triangulation)
{
    // Need to work with triangulation here
    std::vector<dealii::GridTools::PeriodicFacePair<typename Triangulation<dim>::cell_iterator> >
    periodicity_vector;

    // 1. Periodicity left-right
    dealii::types::boundary_id bLeft = 0;
    dealii::types::boundary_id bRight = 1;
    unsigned int direction = 0;
    dealii::GridTools::collect_periodic_faces(
        triangulation,
        bLeft, bRight, direction,
        periodicity_vector);

    triangulation.add_periodicity(periodicity_vector);

    model->addPeriodicBoundary(bLeft, bRight, direction, dealii::ComponentMask());

    periodicity_vector.clear();

    // 2. Periodicity bottom-top
    dealii::types::boundary_id bBottom = 2;
    dealii::types::boundary_id bTop = 3;
    direction = 1;
    dealii::GridTools::collect_periodic_faces(
        triangulation,
        bBottom, bTop, direction,
        periodicity_vector);

    triangulation.add_periodicity(periodicity_vector);

    model->addPeriodicBoundary(bBottom, bTop, direction, dealii::ComponentMask());

    if (dim == 3) {
        periodicity_vector.clear();

        // 3. Periodicity Z bottom - Z top
        dealii::types::boundary_id bZBottom = 4;
        dealii::types::boundary_id bZTop = 5;
        direction = 2;
        dealii::GridTools::collect_periodic_faces(
            triangulation,
            bZBottom, bZTop, direction,
            periodicity_vector);

        triangulation.add_periodicity(periodicity_vector);

        model->addPeriodicBoundary(bZBottom, bZTop, direction, dealii::ComponentMask());
    }
}

template class ABM<2>;
template class ABM<3>;