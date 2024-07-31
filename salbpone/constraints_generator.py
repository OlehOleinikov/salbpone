"""
Модуль формування обмежень задачі лінійного програмування
"""
from .logger_setup import logger
from .data_types import ConstraintsGroup, EarliestLatestData, TimeUnit, OperationsCosts, DepPairsSet


class ConstraintsGenerator:
    """
    Забезпечує генерацію обмежень.
    Формує обмеження рівностей та нерівностей відповідно загальної математичної моделі.
    """
    def __init__(self, parent):
        self.parent = parent
        self.c_single_assignments = self.generate_single_assignment(n=self.parent.n,
                                                                    E=self.parent.E,
                                                                    L=self.parent.L)
        self.c_cycle_time = self.generate_cycle_constraints(n=self.parent.n,
                                                            t=self.parent.t,
                                                            cycle_time=self.parent.T,
                                                            m_min=self.parent.m_min,
                                                            m_max=self.parent.m_max,
                                                            E=self.parent.E,
                                                            L=self.parent.L,
                                                            use_y=True)
        self.c_precedence = self.generate_precedence_constraints(P_ik_pairs=self.parent.P,
                                                                 E=self.parent.E,
                                                                 L=self.parent.L)
        self.c_station_turn_on = self.generate_station_constraints(n=self.parent.n,
                                                                   m_min=self.parent.m_min,
                                                                   m_max=self.parent.m_max,
                                                                   L=self.parent.L)

    @property
    def constraints(self) -> ConstraintsGroup:
        """
        :return: Загальний список згенерованих обмежень.
        """
        return (self.c_single_assignments +
                self.c_cycle_time +
                self.c_precedence +
                self.c_station_turn_on)

    def generate_single_assignment(self,
                                   n: int,
                                   E: EarliestLatestData,
                                   L: EarliestLatestData) -> ConstraintsGroup:
        """
        Функція, яка забезпечує створення обмежень щодо призначення операції до одного й тільки одного робочого місця.
        :param n: Кількість операцій
        :param E: Відомості про найменший (найранішій) індекс робочого місця до якого може бути призначена операція
        :param L: Відомості про найбільший (найпізніший) індекс робочого місця до якого може бути призначена операція

        :return: Список рядків, що представляють обмеження рівності
        """
        constraints = []
        logger.info("Обмеження призначення операції одному й тільки одному робочому місцю...")
        for i in range(1, n + 1):
            constraint = " + ".join([f"x[{i}][{j}]" for j in range(E[i], L[i] + 1)]) + " == 1"
            constraints.append(constraint)
            if self.parent.verbose:
                logger.debug(constraint)
        if self.parent.verbose:
            logger.debug(f"Додано обмежень {len(constraints)}")
        return constraints

    def generate_cycle_constraints(self,
                                   n: int,
                                   t: OperationsCosts,
                                   cycle_time: TimeUnit,
                                   m_min: int,
                                   m_max: int,
                                   E: EarliestLatestData,
                                   L: EarliestLatestData,
                                   use_y: bool = False) -> ConstraintsGroup:
        """
        Генерує обмеження циклу для робочих станцій.

        :param n: Кількість операцій
        :param t: Масив з тривалістю операцій
        :param cycle_time: Час циклу
        :param m_min: Мінімальна (можлива) кількість робочих станцій
        :param m_max: Максимальна (можлива) кількість робочих станцій
        :param E: Відомості про найменший (найранішній) індекс робочого місця до якого може бути призначена операція
        :param L: Відомості про найбільший (найпізніший) індекс робочого місця до якого може бути призначена операція
        :param use_y: Вказує, чи використовувати множник y_j
        :return: Список рядків, що представляють обмеження циклу
        """
        logger.info("Дотримання часу виробничого циклу...")
        constraints = []
        for j in range(1, m_max + 1):
            terms = [f"{t[i - 1]} * x[{i}][{j}]" for i in range(1, n + 1) if E[i] <= j <= L[i]]
            if j <= m_min:
                constraint = " + ".join(terms) + f" <= {cycle_time}"
            else:
                if use_y:
                    constraint = " + ".join(terms) + f" <= {cycle_time} * y[{j}]"
                else:
                    constraint = " + ".join(terms) + f" <= {cycle_time}"
            if self.parent.verbose:
                logger.debug(constraint)
            constraints.append(constraint)
        if self.parent.verbose:
            logger.debug(f"Додано обмежень {len(constraints)}")
        return constraints

    def generate_precedence_constraints(self,
                                        P_ik_pairs: DepPairsSet,
                                        E: EarliestLatestData,
                                        L: EarliestLatestData) -> ConstraintsGroup:
        """
        Генерує обмеження послідовності операцій для задачі балансування збиральної лінії.

        :param P_ik_pairs: Набір пар (i, k), де операція `i` має передувати операції k
        :param E: Відомості про найменший (найранішній) індекс робочого місця до якого може бути призначена операція
        :param L: Відомості про найбільший (найпізніший) індекс робочого місця до якого може бути призначена операція
        :return: Список рядків, що представляють обмеження послідовності
        """
        logger.info("Дотримання послідовності виробництва...")
        constraints = []
        for i, k in P_ik_pairs:
            left_terms = [f"{j} * x[{i}][{j}]" for j in range(E[i], L[i] + 1)]
            right_terms = [f"{j} * x[{k}][{j}]" for j in range(E[k], L[k] + 1)]
            left_constraint = " + ".join(left_terms)
            right_constraint = " + ".join(right_terms)
            constraints.append(f"{left_constraint} <= {right_constraint}")
            if self.parent.verbose:
                logger.debug(f"{left_constraint} <= {right_constraint}")
        if self.parent.verbose:
            logger.debug(f"Додано обмежень {len(constraints)}")
        return constraints

    def generate_station_constraints(self, n: int, m_max: int, m_min: int, L: EarliestLatestData) -> ConstraintsGroup:
        """
        Функція для генерування обмежень на увімкнення станцій

        :param n: Кількість операцій
        :param m_max: Максимальна кількість робочих станцій
        :param m_min: Мінімальна кількість робочих станцій
        :param L: Словник, де ключ - індекс операції, значення - кінцева станція
        :return: Список рядків, що представляють обмеження на увімкнення станцій
        """
        logger.info("Обмеження увімкнення тільки задіяних станцій...")
        constraints = []
        for i in range(1, n + 1):
            for q in range(m_max - m_min):
                # logger.debug(f"i={i} q={q}")
                # if L[i] - q >= m_min:  # Додаємо перевірку, щоб не було негативних або нульових індексів
                constraints.append(f"x[{i}][{L[i] - q}] <= y[{m_max - q}]")
                if self.parent.verbose:
                    logger.debug(f"x[{i}][{L[i] - q}] <= y[{m_max - q}]")
        if self.parent.verbose:
            logger.debug(f"Додано обмежень {len(constraints)}")
        return constraints
