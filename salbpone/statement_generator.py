"""
Модуль генерації додаткових змінних.
Дозволяє адаптувати умову до потреб математичної моделі.
"""
from typing import Tuple

import numpy as np
import math

from .data_types import OperationsCosts, TimeUnit, PrecedenceDict, EarliestLatestData, GraphDict, DepPairsSet
from .logger_setup import logger


class ExtendStatement:
    """
    Клас формування та збереження додаткових змінних умови задачі.
    """
    def __init__(self, parent):
        self.parent = parent
        self.m_min, self.m_max = self.calculate_m_min_max(n=self.parent.n,
                                                          t=self.parent.t,
                                                          cycle_time=self.parent.T)
        self.ST, self.PT = self.calculate_st_pt(procedure_graph=self.parent.precedence_graph)
        self.E, self.L = self.calculate_e_l(n=self.parent.n,
                                            t=self.parent.t,
                                            cycle_time=self.parent.T,
                                            m_max=self.m_max,
                                            ST=self.ST,
                                            PT=self.PT)
        self.P_matrix = self.create_dependency_matrix(n=self.parent.n,
                                               procedure_graph=self.parent.precedence_graph)
        self.P_pairs = self.create_procede_pairs(dep_matrix=self.P_matrix)

    def calculate_m_min_max(self, n: int, t: OperationsCosts, cycle_time: TimeUnit) -> tuple[int, int]:
        """
        Функція для розрахунку m_min та m_max.

        Parameters:
        n (int): Кількість операцій
        t (list): Масив з тривалістю операцій
        cycle_time (int): Час циклу

        Returns:
        tuple: m_min, m_max
        """
        m_max = n
        total_time = sum(t)
        m_min = math.ceil(total_time / cycle_time)
        if self.parent.verbose:
            logger.debug(f"Мінімальна (теоретична) кількість робочих станції (m_min): {m_min}")
            logger.debug(f"Максимальна (найгірший випадок) кількість робочих станції (m_max): {m_max}")
        return m_min, m_max

    def calculate_st_pt(self, procedure_graph: GraphDict) -> Tuple[PrecedenceDict, PrecedenceDict]:
        """
        Функція для створення словників ST та PT.

        Parameters:
        procedure_graph (dict): Словник з залежностями операцій

        Returns:
        tuple: ST, PT
        """
        n = len(procedure_graph)
        ST = {i: set() for i in range(1, n + 1)}
        PT = {i: set() for i in range(1, n + 1)}

        def find_successors(node):
            successors = set()
            for successor in procedure_graph[node]:
                successors.add(successor)
                successors.update(find_successors(successor))
            return successors

        def find_predecessors(node):
            predecessors = set()
            for pred, successors in procedure_graph.items():
                if node in successors:
                    predecessors.add(pred)
                    predecessors.update(find_predecessors(pred))
            return predecessors

        for i in range(1, n + 1):
            PT[i] = find_predecessors(i)
            ST[i] = find_successors(i)

        # Інвертуємо значення (через зворотню побудову графа)
        ST, PT = PT, ST

        if self.parent.verbose:
            for k, v in ST.items():
                if not len(v):
                    continue
                o_list = [f't{x}' for x in v]
                text = ', '.join(o_list)
                logger.debug(f'Тільки після t{k} можуть розпочатись (ST): {text}')

            for k, v in PT.items():
                if not len(v):
                    continue
                o_list = [f't{x}' for x in v]
                text = ', '.join(o_list)
                logger.debug(f'Перед t{k} мають завершитись (PT): {text}')

        return ST, PT

    def calculate_e_l(self,
                      n: int,
                      t: OperationsCosts,
                      cycle_time: TimeUnit,
                      m_max: int,
                      ST: PrecedenceDict,
                      PT: PrecedenceDict) -> Tuple[EarliestLatestData, EarliestLatestData]:
        """
        Функція для розрахунку масивів E та L.

        Parameters:
        n (int): Кількість операцій
        t (list): Масив з тривалістю операцій
        cycle_time (int): Час циклу
        m_max (int): Максимальна кількість робочих станцій
        ST (dict): Словник з операціями, що мають бути виконані після операції
        PT (dict): Словник з операціями, що мають бути виконані до операції

        Returns:
        tuple: E, L
        """
        E = {}
        L = {}

        for i in range(1, n + 1):
            sum_PT = sum(t[k-1] for k in PT[i])
            sum_ST = sum(t[k-1] for k in ST[i])

            E[i] = math.ceil((t[i-1] + sum_PT) / cycle_time)
            L[i] = m_max + 1 - math.ceil((t[i-1] + sum_ST) / cycle_time)

        if self.parent.verbose:
            for i in range(n):
                logger.debug(f"Операція t{i+1} не може бути за межами станцій "
                             f"[E{i+1},L{i+1}] = [{E[i+1]}...{L[i+1]}]")

        return E, L

    def create_dependency_matrix(self, n: int, procedure_graph: GraphDict) -> np.ndarray:
        """
        Функція для створення матриці залежностей P.

        Parameters:
        n (int): Кількість операцій
        PT (dict): Словник з операціями, що мають бути виконані до операції

        Returns:
        np.array: Матриця залежностей P
        """
        P = np.zeros((n, n), dtype=int)

        for i in range(1, n + 1):
            for k in procedure_graph[i]:
                P[i-1][k-1] = 1
                if self.parent.verbose:
                    logger.debug(f"Додана залежність P_ik: перед t{i} має бути виконана t{k}")
        return P

    def create_procede_pairs(self, dep_matrix: np.ndarray) -> DepPairsSet:
        pairs = set()
        n = self.parent.n
        for k in range(n):
            for i in range(n):
                if dep_matrix[i][k]:
                    pairs.add((k + 1, i + 1))
        return pairs



