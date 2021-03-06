from ortools.linear_solver import pywraplp
import random as rand

solver = pywraplp.Solver('MiPrimerProblemaEntero', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# x and y are integer non-negative variables.
nodes = 10
rand.seed(42)
cost = { (i,j): rand.randint(10,100) for i in range(nodes) for j in range(nodes) if i!=j}
x = {}
for i in range(nodes):
    for j in range(nodes):
        if i!=j:
            x[i, j] = solver.BoolVar('x[%i, %i]' % (i, j))
v = {}
for i in range(1, nodes):
    for j in range(1, nodes):
        if i != j:
            v[i, j] = solver.BoolVar('v[%i, %i]' % (i, j))

# Aqui se almacenarán las precedencias que se deseen
precedencias = [[3,2],[1,2]]

solver.Minimize(solver.Sum([cost[i,j]*x[i,j] for i in range(nodes) for j in range(nodes) if i!=j]))

for i in range(nodes):
    solver.Add(solver.Sum([x[i,j] for j in range(nodes) if i!=j]) == 1)

for j in range(nodes):
    solver.Add(solver.Sum([x[i,j] for i in range(nodes) if i!=j]) == 1)

for i in range(1,nodes):
    for j in range(1,nodes):
        if i != j:
            solver.Add((v[i,j]+v[j,i]) == 1)

for i in range(1,nodes):
    for j in range(1,nodes):
        if i != j:
            for k in range(1, nodes):
                if (k != i) & (k != j):
                    solver.Add( v[i,j]+v[j,k] <= v[i,k]+1 )

for i in range(1,nodes):
    for j in range(1,nodes):
        if i != j:
            solver.Add(x[i,j] <= v[i,j])

for p in precedencias:
    solver.Add(v[p[0],p[1]] == 1)

sol = solver.Solve()
if sol == solver.OPTIMAL:
    print('Wall time = ' + str(solver.WallTime()) + ' ms')
    print('Número de variables =', solver.NumVariables())
    print('Número de restricciones =', solver.NumConstraints())
    print('Costo total =', solver.Objective().Value())
    recorrido = '0'
    i=0
    while i != -1:
        for j in range(nodes):
            if i!=j:
                if x[i, j].solution_value() > 0:
                    recorrido += ' -c(' + str(cost[i,j]) +')-> ' + str(j)
                    aux = j
        if aux != 0:
            i = aux
        else:
            i = -1
    print(recorrido)      
