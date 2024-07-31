"""
Модуль перевірки вхідних даних задачі
"""

from typing import Any

from .data_types import OperationsCosts, TimeUnit, GraphDict
from .logger_setup import logger


class InputChecker:
    """
    Забезпечує перевірку вхідних значень задачі.
    Здійснюється звірка очікуваних типів та структур даних.
    """
    def __init__(self, parent):
        self.parent = parent

    def check_costs(self, value: Any) -> OperationsCosts:
        """
        Перевіряє допустимість значень вартості операцій.

        :param value: Змінна для перевірки
        :return: повертається вхідна змінна, якщо відповідає вимогам допустимості (інакше - помилка з описом)
        """
        assert isinstance(value, list), "Вартість (тривалість) операцій мають бути передані списком t"
        assert all([isinstance(x, (int, float)) for x in value]), "Тривалості всіх операцій (t_i) мають бути числом"
        if self.parent.verbose:
            labels = []
            for ti in range(len(value)):
                labels.append(f't{ti + 1} = {value[ti]}')
            message = ', '.join(labels)
            logger.debug(f'Тривалості операцій (t_i): {message}')
        return value

    def check_cycletime(self, value: Any) -> TimeUnit:
        """
        Перевіряє допустимість значень тривалості виробничого циклу.

        :param value: Змінна для перевірки
        :return: повертається вхідна змінна, якщо відповідає вимогам допустимості (інакше - помилка з описом)
        """
        assert isinstance(value, TimeUnit), "Час (Т) виробничого циклу має бути числом "
        if self.parent.verbose:
            logger.debug(f'Тривалість циклу (Т): {value}')
        return value

    def check_graph(self, value: Any) -> GraphDict:
        """
        Перевіряє допустимість наданого графу обмежень.

        :param value: Змінна для перевірки
        :return: повертається вхідна змінна, якщо відповідає вимогам допустимості (інакше - помилка з описом)
        """
        assert isinstance(value, dict), "Граф попередніх обов'язкових операцій має бути словником"
        assert all([isinstance(x, int) for x in value.keys()]), "Всі ключі графу залежностей мають бути цілими числами"
        assert all([x > 0 for x in value.keys()]), "Всі ключі графу залежностей мають бути додатніми числами"
        assert all(isinstance(item, int)
                   for sublist in value.values()
                   for item in sublist), "Всі обов'язкові операції графу залежностей мають бути цілими числами"
        if self.parent.verbose:
            for k, v in value.items():
                if len(v):
                    o_list = []
                    for o in v:
                        o_list.append(f't{o}')
                    operations = ", ".join(o_list)
                    logger.debug(f'До початку операції t{k} мають бути виконані операції: {operations}')
                else:
                    logger.debug(f'До початку операції t{k} обмежень немає')
        return value
