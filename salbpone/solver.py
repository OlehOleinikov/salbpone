"""
Модуль головного класу солвера SALBP-1.
"""
import re
import pulp

from .data_types import (OperationsCosts, TimeUnit, GraphDict, ConstraintsGroup, EarliestLatestData,
                         DepPairsSet, PrecedenceDict)
from .logger_setup import logger
from .checkers import InputChecker
from .statement_generator import ExtendStatement
from .constraints_generator import ConstraintsGenerator


class SolverSALBP:
    """
    Вирішувач SALBP-1.

    Забезпечує перетворення умови, формування обмежень, вирішення задачі.
    Для вирішення задачі лінійного програмування виконується код, який генерує змінні,
    що підлягають оптимізації та цільову функцію, що підлягає мінімізації:

    .. code-block:: python

        # Ініціалізація задачі
        self.problem = pulp.LpProblem("Binary_Linear_Programming", pulp.LpMinimize)

        # Змінні
        x = [[pulp.LpVariable(f"x_{i + 1}_{j + 1}", cat="Binary") for j in range(self.n)] for i in range(self.n)]
        y = [pulp.LpVariable(f"y_{j + 1}", cat="Binary") for j in range(self.n)]

        # Цільова функція
        self.problem += eval(self.adjust_indices(self.objective_function))

        # Обмеження
        for constraint in self.constraints:
            self.problem += eval(self.adjust_indices(constraint))

        # Запуск оптимізації
        self.problem.solve()


    За результатами роботи може бути:

    - "Знайдено оптимальне рішення" (з відображенням матриці призначення та навантаження станцій)
    - повідомлення "Задачу не вирішено" (з описом причин помилки)
    - "Рішення не існує"
    - "Лише рішення поза обмеженнями!" (з описом похибки та критеріїв, які не вдалось досягнути)
    - "Задача не формалізована, перевірте умову" (в разі порушення формулювання задачі, є непередбаченої помилкою)

    :param operations_costs: Тривалість операцій
    :type operations_costs: OperationsCosts

    :param precedence_graph: Граф залежностей операцій
    :type precedence_graph: GraphDict

    :param cycle_time: Тривалість виробничого циклу
    :type cycle_time: TimeUnit

    :param verbose: Режим деталізованого логування
    :type verbose: bool


    """
    def __init__(self,
                 operations_costs: OperationsCosts,
                 precedence_graph: GraphDict,
                 cycle_time: TimeUnit,
                 verbose: bool = False):
        logger.info("Створення екземпляру вирішення SALBP-1...")

        # Умова задачі
        logger.info("Перевірка умови задачі...")
        self.verbose = verbose
        self.input_checker = InputChecker(parent=self)
        self.T = self.input_checker.check_cycletime(cycle_time)
        self.t = self.input_checker.check_costs(operations_costs)
        assert all([x <= self.T for x in self.t]), "Тривалість жодної операції не може бути більше циклу Т"
        self.n = len(self.t)
        self.precedence_graph = self.input_checker.check_graph(precedence_graph)
        logger.success(f'Отримано та перевірено умову задачі (n={self.n}, T={self.T})')

        # Допоміжні змінні
        logger.info('Розширення умови допоміжними змінними...')
        self.extend_statement = ExtendStatement(parent=self)
        logger.success("Створено допоміжні змінні (m, L, E, P, PT, ST)")

        # Цільова функція
        self.objective_function = self.generate_objective_function(m_min=self.m_min, m_max=self.m_max)
        logger.info(f"Цільова функція: min {self.objective_function}")

        # Обмеження
        logger.info("Формування обмежень...")
        self.constraints_generator = ConstraintsGenerator(parent=self)

        # Оптимізатор
        # Ініціалізація задачі
        self.problem = pulp.LpProblem("Binary_Linear_Programming", pulp.LpMinimize)

        # Змінні
        x = [[pulp.LpVariable(f"x_{i + 1}_{j + 1}", cat="Binary") for j in range(self.n)] for i in range(self.n)]
        y = [pulp.LpVariable(f"y_{j + 1}", cat="Binary") for j in range(self.n)]

        # Цільова функція
        self.problem += eval(self.adjust_indices(self.objective_function))

        # Обмеження
        for constraint in self.constraints:
            self.problem += eval(self.adjust_indices(constraint))

        # Запуск пошуку рішення
        logger.info('Вирішення задачі...')
        self.problem.solve()
        if self.problem.status == pulp.LpStatusOptimal:
            logger.success("Знайдено оптимальне рішення")
        elif self.problem.status == pulp.LpStatusNotSolved:
            logger.error("Задачу не вирішено")
        elif self.problem.status == pulp.LpStatusInfeasible:
            logger.error("Рішення не існує")
        elif self.problem.status == pulp.LpStatusUnbounded:
            logger.error("Лише рішення поза обмеженнями!")
        elif self.problem.status == pulp.LpStatusUndefined:
            logger.error("Задача не формалізована, перевірте умову")

        # Друк матриці призначення відповідно знайденого рішення
        print('')
        logger.success('Матриця призначення:')
        x_matrix = [[int(pulp.value(x[i][j])) if pulp.value(x[i][j]) is not None else 0 for j in range(self.n)] for i in
                    range(self.n)]
        for pos, row in enumerate(x_matrix):
            vals = []
            for v in row:
                if v == 1:
                    vals.append('+')
                else:
                    vals.append(' ')
            text = ' | '.join(vals)
            logger.success(f"t{pos+1:02d}: | {text}")

        # Виведення сум значень по кожній колонці з врахуванням масиву t
        print('')
        stations_on = 0
        logger.success("Завантаження станцій:")
        column_sums = [sum(self.t[i] * x_matrix[i][j] for i in range(self.n)) for j in range(self.n)]
        for idx, col_sum in enumerate(column_sums):
            logger.success(f"Станція J{idx + 1}: {col_sum}")
            if col_sum > 0:
                stations_on += 1

        # Кількість увімкнених станцій
        print('')
        logger.success(f"Увімкнені станції: {stations_on}\n", )

    @property
    def E(self) -> EarliestLatestData:
        """
        Масив найранішніх станцій (для кожної операції)
        """
        return self.extend_statement.E

    @property
    def L(self) -> EarliestLatestData:
        """
        Масив найпізніших станцій (для кожної операції)
        """
        return self.extend_statement.L

    @property
    def P(self) -> DepPairsSet:
        """
        Пари залежностей (перевіряєма операція та операція, яка має передувати)
        """
        return self.extend_statement.P_pairs

    @property
    def ST(self) -> PrecedenceDict:
        """
        Множина операцій, яка має передувати перевіряємій (по всьому графу)
        """
        return self.extend_statement.ST

    @property
    def PT(self) -> PrecedenceDict:
        """
        Множина операцій, яка залежить від перевіряємої (по всьому графу)
        """
        return self.extend_statement.PT

    @property
    def m_min(self) -> int:
        """
        Теоретична мінімальна кількість станцій, яка забезпечить виконання задачі
        """
        return self.extend_statement.m_min

    @property
    def m_max(self) -> int:
        """
        Теоретична максимальна кількість станцій, яка може бути у гіршому випадку
        """
        return self.extend_statement.m_max

    @property
    def constraints(self) -> ConstraintsGroup:
        """
        Список з виразами обмежень (рівності та нерівності)
        """
        return self.constraints_generator.constraints

    @staticmethod
    def generate_objective_function(m_min: int, m_max: int) -> str:
        """
        Допоміжна статична функція.
        Генерує цільову функцію для задачі балансування збиральної лінії.

        :param m_min: Мінімальна (теоретична) кількість робочих станцій
        :param m_max: Максимальна кількість робочих станцій (гірший випадок)
        :return: Рядок, що представляє цільову функцію
        """
        terms = [f"{j} * y[{j}]" for j in range(m_min + 1, m_max + 1)]
        objective_function = " + ".join(terms)
        return f"{objective_function}"

    # Функція для заміни індексів
    @staticmethod
    def adjust_indices(expression):
        """
        Допоміжна статична функція.
        Отримує рядок, який описує обмеження чи функцію, які містять індекси змінних.
        Зменшує індекс на 1, щоб досягти перетворення з людського відображення індексів на індекси списків Python.
        :param expression: рядок з формулюванням обмеження чи функції
        :return: рядок з формулюванням обмеження (чи функції) зі зменшеними індексами змінних
        """
        def replacer(match):
            # Заміна x[i][j] і y[j] індексів
            var, i, j = match.groups()
            return f"{var}[{int(i) - 1}][{int(j) - 1}]" if j else f"{var}[{int(i) - 1}]"

        return re.sub(r'([xy])\[(\d+)\](?:\[(\d+)\])?', replacer, expression)
