# Travelling Salesman Problem (TSP)
Problema del viajante de comercio (TSP) resuelto con **Pyhton** y **Or-Tools**.
En cada archivo se encuentra un modelo diferente para abordar la eliminación de subtours.
## Modelo con Ui
### tsp.py
Contiene el modelo del TSP solucionando el problema de los subtours con el uso de Ui.
#### Definición de las variables
```
u = {}
for i in range(1,nodes):
    u[i] = solver.IntVar(1.0,solver.infinity(),'u[%i]' % (i))
```
#### Resolución de subtours
```
for i in range(1,nodes):
    for j in range(1,nodes):
        solver.Add(u[j]>=(u[i]+x[i,j]-(nodes-2)*(1-x[i,j])))
```
### tsp1mejorado.py
Mejora el modelo anterior de las Uij reforzando las restricciones
```
for i in range(1,nodes):
    for j in range(1,nodes):
        solver.Add(u[j]>=(u[i]+x[i,j]-(nodes-2)*(1-x[i,j])+(nodes-3)*x[j,i]))
```
## Modelo con Vij
### tsp2.py
Contiene el modelo del TSP solucionando el problema de los subtours con el uso de Vij.
#### Definición de las variables
```
v = {}
for i in range(1, nodes):
    for j in range(1, nodes):
        if i != j:
            v[i, j] = solver.BoolVar('v[%i, %i]' % (i, j))
```
#### Resolución de subtours
```
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
```
## Modelo con flujos (fij)
### tsp_flujo.py
Contiene el modelo del TSP solucionando el problema de los subtours con el uso de fij.
#### Definición de las variables
```
f = {}
for i in range(nodes):
    for j in range(nodes):
        f[i, j] = solver.IntVar(0.0,solver.infinity(),'f[%i, %i]' % (i, j))
```
#### Resolución de subtours
```
for i in range(1,nodes):
    solver.Add((solver.Sum([f[i,j] for j in range(nodes)])-solver.Sum([f[j,i] for j in range(nodes)]))==1)
for i in range(nodes):
    for j in range(nodes):
        solver.Add(0<=f[i,j]<=(nodes-1)*x[i,j])
```
### tsp_flujo_mejorado.py
Mejora el modelo anterior de las fij reforzando las restricciones
```
for i in range(1,nodes):
    solver.Add((solver.Sum([f[i,j] for j in range(nodes)])-solver.Sum([f[j,i] for j in range(nodes)]))==1)
for i in range(1,nodes):
    for j in range(1,nodes):
        solver.Add(x[i,j]<=f[i,j]<=(nodes-2)*x[i,j])
for i in range(1,nodes):
    solver.Add(f[i,0]==(nodes-1)*x[i,0])
for i in range(1,nodes):
    solver.Add(f[0,i]==0)
```
