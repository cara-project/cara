from fastapi import FastAPI
from pyomo.environ import (
    ConcreteModel,
    Var,
    Objective,
    Constraint,
    SolverFactory,
    NonNegativeReals,
    value,
)
from pyomo.opt import TerminationCondition

app = FastAPI()


def solve_model():
    model = ConcreteModel()

    model.x = Var(domain=NonNegativeReals, initialize=2.0)

    model.con = Constraint(expr=model.x >= 1)

    model.obj = Objective(expr=model.x)

    solver = SolverFactory("appsi_highs")

    if not solver.available(exception_flag=False):
        return {"error": "Solver 'appsi_highs' ist nicht verfügbar."}

    result = solver.solve(model)

    term = result.solver.termination_condition
    if term != TerminationCondition.optimal:
        return {"error": f'Optimierung nicht optimal beendet: {term}'}

    return {
        "x_value": float(value(model.x)),
        "objective": float(value(model.obj)),
        "termination": str(term),
    }


@app.get("/")
async def root():
    return solve_model()
