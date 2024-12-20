import pyomo.environ as pyo 
import dcopf_decl as dcopf 
from uc_example_data import data

model = pyo.ConcreteModel()
model.T = pyo.Set(initialize=range(2), ordered=True)
model.G = pyo.Set(initialize=sorted(data['gens'].keys()), ordered=True)

def period_rule(b, t):
    return dcopf.create_dcopf_model(data[t])

model.period = pyo.Block(model.T, rule=period_rule)

def ramp_con_rule(m, t, g):
    if t == m.T.first():
        return pyo.Constraint.Skip
    return (-15.0, m.period[t-1].pg[g] - m.period[t].pg[g], 15.0)

model.ramp_con = pyo.Constraint(model.T, model.G, rule=ramp_con_rule)

model.period[:].objective.deactivate()
model.obj = pyo.Objective(expr=sum(model.period[:].objective.expr))

solver = pyo.SolverFactory('ipopt')
solver.solve(model, tee=True)

model.period[:].pg.display()
