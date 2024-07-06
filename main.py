from salbpone import SolverSALBP, LatexConverter

# Масив з тривалістю операцій
t = [5, 6, 2, 5, 4, 3]

# Словник з залежностями операцій
procedure_graph = {
    1: [],
    2: [],
    3: [1],
    4: [2, 3],
    5: [1, 2],
    6: [4]
}

# Час циклу Т
cycle_time = 10

s = SolverSALBP(operations_costs=t,
                cycle_time=cycle_time,
                precedence_graph=procedure_graph,
                verbose=True)
lat = LatexConverter(constraints=s.constraints)

print('end')




