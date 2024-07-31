from salbpone import SolverSALBP, LatexConverter, save_procedure_graph
from problems import task1, task2, task3, task4

current_task: dict = task4

# Масив з тривалістю операцій
t = current_task['t']

# Словник з залежностями операцій
procedure_graph = current_task['procedure_graph']

# Час циклу Т
cycle_time = current_task['T']

# Вирішення задачі
s = SolverSALBP(operations_costs=t,
                cycle_time=cycle_time,
                precedence_graph=procedure_graph,
                verbose=True)

# Адаптація обмежень у формат Latex
print('\nДрук адаптованих LaTex формул:')
LatexConverter(constraints=s.constraints).print_latex()
LatexConverter(constraints=[s.objective_function]).print_latex()

# Збереження візуалізації графу операцій
print('\nЗбереження інтерактивного графу HTML...')
save_procedure_graph(procedure_graph=procedure_graph,
                     t=t,
                     file_name=current_task['title']+'.html')

print('\nРобота програми завершена.')
