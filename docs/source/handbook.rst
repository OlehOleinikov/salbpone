Приклад використання
=====================

Формування умови
----------------

Відповідно типової задачі SALBP-1 умова складається з:

- визначених тривалостей операцій
- часу виробничого циклу
- залежностей послідовностей операцій

Наприклад:

``T (час циклу) =10``

.. list-table::
   :header-rows: 1

   * - Номер операції
     - Безпосередньо попередні операції
     - Тривалість операції
   * - 1
     - немає
     - 5
   * - 2
     - немає
     - 6
   * - 3
     - 1
     - 2
   * - 4
     - 2, 3
     - 5
   * - 5
     - 1, 2
     - 4
   * - 6
     - 4
     - 3

Може бути виражена у змінних середовища python:

.. code-block:: python

    t = [5, 6, 2, 5, 4, 3],
    procedure_graph = {1: [],
                      2: [],
                      3: [1],
                      4: [2, 3],
                      5: [1, 2],
                      6: [4]},
    cycle_time = 10

Створення екземпляру вирішення
------------------------------

Перед створенням екземпляру вирішення імпортується створений клас вирішення задачі:

.. code-block:: python

    from salbpone import SolverSALBP

Отримані змінні з умови задачі використовуються для створення екземпляру вирішення задачі:

.. code-block:: python

    s = SolverSALBP(operations_costs=t,
                    cycle_time=cycle_time,
                    precedence_graph=procedure_graph,
                    verbose=True)

Параметр ``verbose=True`` дозволяє відобразити у лог виконання кожен крок. У цьому разі детальні повідомлення
логера будуть містити префікс ``| DEBUG |``

Перевірка умови
---------------

Перед початком вирішення перевіряється умова на допустимість типів даних та можливості вирішення (додатні значення,
час кожної операції в межах часу циклу, відповідність графу обмежень до кількості операцій, тощо.)

.. code-block:: shell

    D:\projects\tpr_salbp\venv\Scripts\python.exe D:\projects\tpr_salbp\main.py
    INFO | Створення екземпляру вирішення SALBP-1...
    INFO | Перевірка умови задачі...
    DEBUG | Тривалість циклу (Т): 10
    DEBUG | Тривалості операцій (t_i): t1 = 5, t2 = 6, t3 = 2, t4 = 5, t5 = 4, t6 = 3
    DEBUG | До початку операції t1 обмежень немає
    DEBUG | До початку операції t2 обмежень немає
    DEBUG | До початку операції t3 мають бути виконані операції: t1
    DEBUG | До початку операції t4 мають бути виконані операції: t2, t3
    DEBUG | До початку операції t5 мають бути виконані операції: t1, t2
    DEBUG | До початку операції t6 мають бути виконані операції: t4
    SUCCESS | Отримано та перевірено умову задачі (n=6, T=10)

Створення додаткових змінних
----------------------------

Зважаючи на те, що моделлю вирішення передбачене використання змінних, які випливають з умови задачі (такі як,
мінімальна теоретична кількість станцій, множини попередніх операцій, пари залежностей операцій), створюються
опопрні змінні для подальших розрахунків:

.. code-block:: shell

    INFO | Розширення умови допоміжними змінними...
    DEBUG | Мінімальна (теоретична) кількість робочих станції (m_min): 3
    DEBUG | Максимальна (найгірший випадок) кількість робочих станції (m_max): 6
    DEBUG | Тільки після t1 можуть розпочатись (ST): t3, t4, t5, t6
    DEBUG | Тільки після t2 можуть розпочатись (ST): t4, t5, t6
    DEBUG | Тільки після t3 можуть розпочатись (ST): t4, t6
    DEBUG | Тільки після t4 можуть розпочатись (ST): t6
    DEBUG | Перед t3 мають завершитись (PT): t1
    DEBUG | Перед t4 мають завершитись (PT): t1, t2, t3
    DEBUG | Перед t5 мають завершитись (PT): t1, t2
    DEBUG | Перед t6 мають завершитись (PT): t1, t2, t3, t4
    DEBUG | Операція t1 не може бути за межами станцій [E1,L1] = [1...5]
    DEBUG | Операція t2 не може бути за межами станцій [E2,L2] = [1...5]
    DEBUG | Операція t3 не може бути за межами станцій [E3,L3] = [1...6]
    DEBUG | Операція t4 не може бути за межами станцій [E4,L4] = [2...6]
    DEBUG | Операція t5 не може бути за межами станцій [E5,L5] = [2...6]
    DEBUG | Операція t6 не може бути за межами станцій [E6,L6] = [3...6]
    DEBUG | Додана залежність P_ik: перед t3 має бути виконана t1
    DEBUG | Додана залежність P_ik: перед t4 має бути виконана t2
    DEBUG | Додана залежність P_ik: перед t4 має бути виконана t3
    DEBUG | Додана залежність P_ik: перед t5 має бути виконана t1
    DEBUG | Додана залежність P_ik: перед t5 має бути виконана t2
    DEBUG | Додана залежність P_ik: перед t6 має бути виконана t4
    SUCCESS | Створено допоміжні змінні (m, L, E, P, PT, ST)

Визначення цільової функції
---------------------------

Зважаючи на те, що на цьому кроці відомі основні змінні умови, та проведено розрахунок необхідних допоміжних
змінних - стає можливим визначити цільову функцію, яка підлягає мінімізації (відома кількість мінімально можливих
станцій, кількість операцій та верхня межа):

.. code-block:: shell

    INFO | Цільова функція: min 4 * y[4] + 5 * y[5] + 6 * y[6]

Створення обмежень
------------------

.. code-block:: shell

    INFO | Формування обмежень...
    INFO | Обмеження призначення операції одному й тільки одному робочому місцю...
    DEBUG | x[1][1] + x[1][2] + x[1][3] + x[1][4] + x[1][5] == 1
    DEBUG | x[2][1] + x[2][2] + x[2][3] + x[2][4] + x[2][5] == 1
    DEBUG | x[3][1] + x[3][2] + x[3][3] + x[3][4] + x[3][5] + x[3][6] == 1
    DEBUG | x[4][2] + x[4][3] + x[4][4] + x[4][5] + x[4][6] == 1
    DEBUG | x[5][2] + x[5][3] + x[5][4] + x[5][5] + x[5][6] == 1
    DEBUG | x[6][3] + x[6][4] + x[6][5] + x[6][6] == 1
    DEBUG | Додано обмежень 6
    INFO | Дотримання часу виробничого циклу...
    DEBUG | 5 * x[1][1] + 6 * x[2][1] + 2 * x[3][1] <= 10
    DEBUG | 5 * x[1][2] + 6 * x[2][2] + 2 * x[3][2] + 5 * x[4][2] + 4 * x[5][2] <= 10
    DEBUG | 5 * x[1][3] + 6 * x[2][3] + 2 * x[3][3] + 5 * x[4][3] + 4 * x[5][3] + 3 * x[6][3] <= 10
    DEBUG | 5 * x[1][4] + 6 * x[2][4] + 2 * x[3][4] + 5 * x[4][4] + 4 * x[5][4] + 3 * x[6][4] <= 10 * y[4]
    DEBUG | 5 * x[1][5] + 6 * x[2][5] + 2 * x[3][5] + 5 * x[4][5] + 4 * x[5][5] + 3 * x[6][5] <= 10 * y[5]
    DEBUG | 2 * x[3][6] + 5 * x[4][6] + 4 * x[5][6] + 3 * x[6][6] <= 10 * y[6]
    DEBUG | Додано обмежень 6
    INFO | Дотримання послідовності виробництва...
    DEBUG | 1 * x[2][1] + 2 * x[2][2] + 3 * x[2][3] + 4 * x[2][4] + 5 * x[2][5] <= 2 * x[4][2] + 3 * x[4][3] + 4 * x[4][4] + 5 * x[4][5] + 6 * x[4][6]
    DEBUG | 1 * x[3][1] + 2 * x[3][2] + 3 * x[3][3] + 4 * x[3][4] + 5 * x[3][5] + 6 * x[3][6] <= 2 * x[4][2] + 3 * x[4][3] + 4 * x[4][4] + 5 * x[4][5] + 6 * x[4][6]
    DEBUG | 1 * x[1][1] + 2 * x[1][2] + 3 * x[1][3] + 4 * x[1][4] + 5 * x[1][5] <= 2 * x[5][2] + 3 * x[5][3] + 4 * x[5][4] + 5 * x[5][5] + 6 * x[5][6]
    DEBUG | 2 * x[4][2] + 3 * x[4][3] + 4 * x[4][4] + 5 * x[4][5] + 6 * x[4][6] <= 3 * x[6][3] + 4 * x[6][4] + 5 * x[6][5] + 6 * x[6][6]
    DEBUG | 1 * x[2][1] + 2 * x[2][2] + 3 * x[2][3] + 4 * x[2][4] + 5 * x[2][5] <= 2 * x[5][2] + 3 * x[5][3] + 4 * x[5][4] + 5 * x[5][5] + 6 * x[5][6]
    DEBUG | 1 * x[1][1] + 2 * x[1][2] + 3 * x[1][3] + 4 * x[1][4] + 5 * x[1][5] <= 1 * x[3][1] + 2 * x[3][2] + 3 * x[3][3] + 4 * x[3][4] + 5 * x[3][5] + 6 * x[3][6]
    DEBUG | Додано обмежень 6
    INFO | Обмеження увімкнення тільки задіяних станцій...
    DEBUG | x[1][5] <= y[6]
    DEBUG | x[1][4] <= y[5]
    DEBUG | x[1][3] <= y[4]
    DEBUG | x[2][5] <= y[6]
    DEBUG | x[2][4] <= y[5]
    DEBUG | x[2][3] <= y[4]
    DEBUG | x[3][6] <= y[6]
    DEBUG | x[3][5] <= y[5]
    DEBUG | x[3][4] <= y[4]
    DEBUG | x[4][6] <= y[6]
    DEBUG | x[4][5] <= y[5]
    DEBUG | x[4][4] <= y[4]
    DEBUG | x[5][6] <= y[6]
    DEBUG | x[5][5] <= y[5]
    DEBUG | x[5][4] <= y[4]
    DEBUG | x[6][6] <= y[6]
    DEBUG | x[6][5] <= y[5]
    DEBUG | x[6][4] <= y[4]
    DEBUG | Додано обмежень 18

Вирішення задачі цілочисленого програмування
----------------------------------------------

.. code-block:: shell

    INFO | Вирішення задачі...
    Welcome to the CBC MILP Solver
    Version: 2.10.3
    Build Date: Dec 15 2019

    command line - D:\projects\tpr_salbp\venv\lib\site-packages\pulp\solverdir\cbc\win\64\cbc.exe C:\Users\O3425~1.OLE\AppData\Local\Temp\a865a1a57c204b0f8d72cc3ace2fc2a8-pulp.mps -timeMode elapsed -branch -printingOptions all -solution C:\Users\O3425~1.OLE\AppData\Local\Temp\a865a1a57c204b0f8d72cc3ace2fc2a8-pulp.sol (default strategy 1)
    At line 2 NAME          MODEL
    At line 3 ROWS
    At line 41 COLUMNS
    At line 271 RHS
    At line 308 BOUNDS
    At line 342 ENDATA
    Problem MODEL has 36 rows, 33 columns and 160 elements
    Coin0008I MODEL read with 0 errors
    Option for timeMode changed from cpu to elapsed
    Continuous objective value is 0 - 0.00 seconds
    Cgl0003I 0 fixed, 0 tightened bounds, 8 strengthened rows, 0 substitutions
    Cgl0003I 0 fixed, 0 tightened bounds, 2 strengthened rows, 0 substitutions
    Cgl0003I 0 fixed, 0 tightened bounds, 1 strengthened rows, 0 substitutions
    Cgl0003I 0 fixed, 0 tightened bounds, 1 strengthened rows, 0 substitutions
    Cgl0003I 0 fixed, 0 tightened bounds, 1 strengthened rows, 0 substitutions
    Cgl0004I processed model has 35 rows, 33 columns (33 integer (33 of which binary)) and 170 elements
    Cutoff increment increased from 1e-05 to 0.9999
    Cbc0038I Initial state - 2 integers unsatisfied sum - 1
    Cbc0038I Pass   1: suminf.    0.60000 (3) obj. 1.2 iterations 7
    Cbc0038I Pass   2: suminf.    0.40000 (2) obj. 6 iterations 6
    Cbc0038I Pass   3: suminf.    0.40000 (2) obj. 6 iterations 4
    Cbc0038I Pass   4: suminf.    1.14286 (4) obj. 6 iterations 9
    Cbc0038I Pass   5: suminf.    0.80000 (2) obj. 6 iterations 5
    Cbc0038I Pass   6: suminf.    0.80000 (2) obj. 6 iterations 2
    Cbc0038I Pass   7: suminf.    2.00000 (5) obj. 8.5 iterations 9
    Cbc0038I Pass   8: suminf.    1.28859 (6) obj. 7.12752 iterations 5
    Cbc0038I Pass   9: suminf.    1.11111 (4) obj. 6 iterations 1
    Cbc0038I Pass  10: suminf.    0.40000 (2) obj. 6 iterations 5
    Cbc0038I Solution found of 6
    Cbc0038I Before mini branch and bound, 16 integers at bound fixed and 0 continuous
    Cbc0038I Full problem 35 rows 33 columns, reduced to 15 rows 12 columns
    Cbc0038I Mini branch and bound did not improve solution (0.00 seconds)
    Cbc0038I Round again with cutoff of 4.50009
    Cbc0038I Reduced cost fixing fixed 2 variables on major pass 2
    Cbc0038I Pass  11: suminf.    1.00000 (3) obj. 1.33333 iterations 7
    Cbc0038I Pass  12: suminf.    0.66667 (2) obj. 4 iterations 5
    Cbc0038I Pass  13: suminf.    0.66667 (2) obj. 4 iterations 4
    Cbc0038I Pass  14: suminf.    1.60000 (4) obj. 4 iterations 4
    Cbc0038I Pass  15: suminf.    0.66667 (2) obj. 4 iterations 5
    Cbc0038I Pass  16: suminf.    0.66667 (2) obj. 4 iterations 5
    Cbc0038I Pass  17: suminf.    1.14286 (4) obj. 4 iterations 3
    Cbc0038I Pass  18: suminf.    0.80000 (2) obj. 4 iterations 5
    Cbc0038I Pass  19: suminf.    1.20000 (4) obj. 4 iterations 6
    Cbc0038I Pass  20: suminf.    2.00000 (4) obj. 4 iterations 8
    Cbc0038I Pass  21: suminf.    1.00000 (2) obj. 4 iterations 10
    Cbc0038I Pass  22: suminf.    1.00000 (2) obj. 4 iterations 3
    Cbc0038I Pass  23: suminf.    1.00000 (2) obj. 4 iterations 2
    Cbc0038I Pass  24: suminf.    2.15686 (6) obj. 4 iterations 7
    Cbc0038I Pass  25: suminf.    1.66667 (4) obj. 4 iterations 9
    Cbc0038I Pass  26: suminf.    1.66667 (4) obj. 4 iterations 5
    Cbc0038I Pass  27: suminf.    1.66667 (4) obj. 4 iterations 7
    Cbc0038I Pass  28: suminf.    1.66667 (4) obj. 4 iterations 4
    Cbc0038I Pass  29: suminf.    1.66667 (4) obj. 4 iterations 3
    Cbc0038I Pass  30: suminf.    2.97143 (9) obj. 1.14286 iterations 16
    Cbc0038I Pass  31: suminf.    2.61176 (8) obj. 1.36471 iterations 12
    Cbc0038I Pass  32: suminf.    2.56000 (10) obj. 1.33333 iterations 8
    Cbc0038I Pass  33: suminf.    2.66667 (6) obj. 4 iterations 16
    Cbc0038I Pass  34: suminf.    2.66667 (7) obj. 4 iterations 2
    Cbc0038I Pass  35: suminf.    1.66667 (4) obj. 4 iterations 8
    Cbc0038I Pass  36: suminf.    1.66667 (4) obj. 4 iterations 2
    Cbc0038I Pass  37: suminf.    1.66667 (4) obj. 4 iterations 3
    Cbc0038I Pass  38: suminf.    1.66667 (4) obj. 4 iterations 0
    Cbc0038I Pass  39: suminf.    1.66667 (4) obj. 4 iterations 4
    Cbc0038I Pass  40: suminf.    1.66667 (4) obj. 4 iterations 11
    Cbc0038I No solution found this major pass
    Cbc0038I Before mini branch and bound, 15 integers at bound fixed and 0 continuous
    Cbc0038I Full problem 35 rows 33 columns, reduced to 20 rows 16 columns
    Cbc0038I Mini branch and bound improved solution from 6 to 4 (0.02 seconds)
    Cbc0038I Round again with cutoff of 2.40008
    Cbc0038I Reduced cost fixing fixed 3 variables on major pass 3
    Cbc0038I Pass  40: suminf.    1.00000 (2) obj. 0 iterations 1
    Cbc0038I Pass  41: suminf.    1.00000 (2) obj. 0 iterations 5
    Cbc0038I Pass  42: suminf.    2.04762 (6) obj. 0 iterations 6
    Cbc0038I Pass  43: suminf.    0.80000 (2) obj. 0 iterations 9
    Cbc0038I Pass  44: suminf.    0.80000 (2) obj. 0 iterations 3
    Cbc0038I Pass  45: suminf.    0.80000 (2) obj. 0 iterations 2
    Cbc0038I Pass  46: suminf.    1.40000 (4) obj. 0 iterations 8
    Cbc0038I Pass  47: suminf.    0.40000 (2) obj. 0 iterations 5
    Cbc0038I Pass  48: suminf.    0.40000 (2) obj. 0 iterations 3
    Cbc0038I Pass  49: suminf.    1.33333 (4) obj. 0 iterations 10
    Cbc0038I Pass  50: suminf.    1.00000 (2) obj. 0 iterations 2
    Cbc0038I Solution found of 0
    Cbc0038I Before mini branch and bound, 22 integers at bound fixed and 0 continuous
    Cbc0038I Mini branch and bound did not improve solution (0.02 seconds)
    Cbc0038I After 0.02 seconds - Feasibility pump exiting with objective of 0 - took 0.01 seconds
    Cbc0012I Integer solution of 0 found by feasibility pump after 0 iterations and 0 nodes (0.02 seconds)
    Cbc0001I Search completed - best objective 0, took 0 iterations and 0 nodes (0.02 seconds)
    Cbc0035I Maximum depth 0, 0 variables fixed on reduced cost
    Cuts at root node changed objective from 0 to 0
    Probing was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    Gomory was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    Knapsack was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    Clique was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    MixedIntegerRounding2 was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    FlowCover was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    TwoMirCuts was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    ZeroHalf was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)

    Result - Optimal solution found

    Objective value:                0.00000000
    Enumerated nodes:               0
    Total iterations:               0
    Time (CPU seconds):             0.02
    Time (Wallclock seconds):       0.02

    Option for printingOptions changed from normal to all
    Total time (CPU seconds):       0.02   (Wallclock seconds):       0.02

Отримання рішення
-----------------

.. code-block:: shell

    SUCCESS | Знайдено оптимальне рішення

    SUCCESS | Матриця призначення:
    SUCCESS | t01: |   | + |   |   |   |
    SUCCESS | t02: | + |   |   |   |   |
    SUCCESS | t03: |   |   | + |   |   |
    SUCCESS | t04: |   |   | + |   |   |
    SUCCESS | t05: |   | + |   |   |   |
    SUCCESS | t06: |   |   | + |   |   |

    SUCCESS | Завантаження станцій:
    SUCCESS | Станція J1: 6
    SUCCESS | Станція J2: 9
    SUCCESS | Станція J3: 10
    SUCCESS | Станція J4: 0
    SUCCESS | Станція J5: 0
    SUCCESS | Станція J6: 0

    SUCCESS | Увімкнені станції: 3

