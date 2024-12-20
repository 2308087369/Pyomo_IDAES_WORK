import pyomo.environ as pyo
W = ['Harlingen', 'Memphis', 'Ashland']  
C = ['NYC', 'LA', 'Chicago', 'Houston']
model = pyo.ConcreteModel()
model.x = pyo.Var( W, C, bounds=(0,1) )
model.y = pyo.Var( W, within=pyo.Binary )
def one_per_cust_rule(m, c):  
    return sum( m.x[w,c] for w in W ) == 1
model.one_per_cust = pyo.Constraint( C, rule=one_per_cust_rule )
@model.Constraint(W, C) 
def warehouse_active (m, w, c): 
    return m.x[w,c] <= m.y[w]
pyo.SolverFactory('glpk').solve(model)
model.display()