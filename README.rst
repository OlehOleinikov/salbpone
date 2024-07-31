# SALBP-1 solver

SALBP-1 solver
======================

TL;DR
----------------

Solution of a linear programming problem with integer constraints and the sequence of operations according to
the precedence constraint graph for optimizing the number of workstations (a.k.a. Assembly Line Balancing
Problem (SALBP-1)).

.. image:: images/graph.png
   :align: center
   :alt: Procedure graph


The project examines approaches to formulating the mathematical model and constraints, methods for finding the
optimal solution, and the implementation of the proposed algorithms using a personal computer. The program
listing can be used to solve similar problems.
do

Типова умова
--------------
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


Вхідні дані формуються змінними:

.. code-block:: python

    t = [5, 6, 2, 5, 4, 3],
    procedure_graph = {1: [],
                      2: [],
                      3: [1],
                      4: [2, 3],
                      5: [1, 2],
                      6: [4]},
    cycle_time = 10


**SALBP-1 (Simple Assembly Line Balancing Problem Type 1)** є класичним завданням оптимізації у виробничих системах. Основне завдання полягає в тому, щоб розподілити набір операцій на мінімальну кількість робочих станцій при фіксованому часі циклу. Це допомагає зменшити витрати, покращити ефективність та продуктивність виробничого процесу. Програма вирішує цю задачу шляхом побудови математичної моделі, що враховує всі необхідні обмеження і вимоги.


Вирішення задачі
------------------------------


.. code-block:: python

    s = SolverSALBP(operations_costs=t,
                    cycle_time=cycle_time,
                    precedence_graph=procedure_graph,
                    verbose=False)




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

