#include <deal.II/base/point.h>
#include <deal.II/base/function.h>

#include "pde/functional_object.h"

#include "applications/common.h"

template <int dim>
class InitialValues : public dealii::Function<dim>
{
private:
    double _avg;
    double _dg;
public:
    InitialValues() : dealii::Function<dim>(1)
    {
        double min = 0.008;
        double max = 0.05;

        _avg = (min + max) / 2;
        _dg = (max - min) / 2;
    }

    virtual double value(const dealii::Point<dim>& /*p*/,
                        const unsigned int component = 0) const override
    {
        (void)component;
        Assert(component < 1, dealii::ExcIndexRange(component, 0, 1));

        double r = ((double) rand() / (RAND_MAX));
        double v = _avg + _dg*2*(0.5 - r);
        return v;
    }
};

// Forward declarations

namespace PDE {
    template <int dim, typename VectorType>
    class ModelWithKernels;

    template <int dim, typename VectorType>
    class FieldInterpolator;

    template <int dim>
    class VariableValues;

    template <int dim>
    class Variable;
}

namespace CORE {
    template <int dim, typename VectorType>
    class AnalysisTransient;

    template <int dim, typename VectorType>
    class ProblemSet;

    template <int dim, typename VectorType>
    class Problem;

    template <int dim, typename VectorType>
    class ActionsManager;

    template <int dim, typename VectorType>
    class Model;

    template <int dim>
    class PointDataMap;

    class ModelBase;
}

template <int dim>
class ABM
{
    class ExponentialGrowth : public PDE::FunctionalObject<double, dim>
    {
    private:
        std::shared_ptr<const CORE::ModelBase> _model;
        double _D;

    public:
        ExponentialGrowth(double D, std::shared_ptr<const CORE::ModelBase> model);

        virtual double
        f(const PDE::VariableValues<dim>& /*variablesValues*/, unsigned int /*qp*/) const override;

        virtual double
        df(const PDE::VariableValues<dim>& /*variablesValues*/, std::shared_ptr<const PDE::Variable<dim>> /*ivar*/,
            unsigned int /*qp*/) const override;

        virtual double
        d2f(const PDE::VariableValues<dim>& /*variablesValues*/, std::shared_ptr<const PDE::Variable<dim>> /*ivar*/,
            std::shared_ptr<const PDE::Variable<dim>> /*jvar*/, unsigned int /*qp*/) const override;
    };

    class Diffusivity : public PDE::FunctionalObject<double, dim>
    {
    private:
        double _D;

    public:
        Diffusivity(double D);

        virtual double
        f(const PDE::VariableValues<dim>& /*variablesValues*/, unsigned int /*qp*/) const override;

        virtual double
        df(const PDE::VariableValues<dim>& /*variablesValues*/, std::shared_ptr<const PDE::Variable<dim>> /*ivar*/,
            unsigned int /*qp*/) const override;

        virtual double
        d2f(const PDE::VariableValues<dim>& /*variablesValues*/, std::shared_ptr<const PDE::Variable<dim>> /*ivar*/,
            std::shared_ptr<const PDE::Variable<dim>> /*jvar*/, unsigned int /*qp*/) const override;
    };

    // Is nonlinear solver used
    bool _isNonlinear = false; 

    // Triangulation
    std::shared_ptr<Triangulation<dim>> _triangulation;

    // Model
    std::shared_ptr<PDE::ModelWithKernels<dim, VectorType>> _model;

    // Analysis
    std::shared_ptr<CORE::AnalysisTransient<dim, VectorType>> _analysis;

    // Create problem set
    std::shared_ptr<CORE::ProblemSet<dim, VectorType>> _problemSet;

    // Manager
    std::shared_ptr<CORE::ActionsManager<dim, VectorType>> _manager;

    // Main problem
    std::shared_ptr<CORE::Problem<dim, VectorType>> _problem;

    // Interpolator to apply initial cocnditions
    std::shared_ptr<PDE::FieldInterpolator<dim, VectorType>> _fieldInterpolator;

    // Output container for points values
    std::shared_ptr<CORE::PointDataMap<dim>> _mapOutput;

    // Geometry data
    struct Geometry {
        double length;
        unsigned int div;
    };

    Geometry _geometry;

public:
    ABM(double length, double patch_size, double D1, double D4, std::string savePath = std::string());

    std::vector<double> run(std::vector<double> vecInitVals, double timeStepInit, double timeEnd);

private:
    std::shared_ptr<Triangulation<dim>> createMesh(double length, double patch_size);

    void setPeriodicBoundaryCondtions(std::shared_ptr<CORE::Model<dim, VectorType>> model,
        Triangulation<dim>& triangulation);
};
