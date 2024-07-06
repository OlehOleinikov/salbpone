"""
Модуль перетворень обмежень.
Забезпечує адаптацію існуючого формату обмежень для друку у документах.
"""
from typing import List


class LatexConverter:
    """
    Конвертер обмежень до Latex.
    """
    def __init__(self, constraints: List[str]):
        self.constraints = constraints

    def to_latex(self) -> List[str]:
        """
        Перетворює рядки обмежень у формат LaTeX.

        :return: Список рядків у форматі LaTeX
        """
        latex_constraints = []
        for constraint in self.constraints:
            # Заміна індексів x[i][j] на x_{i,j} для LaTeX
            latex_constraint = constraint
            latex_constraint = latex_constraint.replace('][', ',').replace('[', '_{').replace(']', '}')
            # Заміна знаків нерівності на формат LaTeX
            latex_constraint = latex_constraint.replace("<=", r"\leq").replace(">=", r"\geq")
            # Заміна знаків множення на LaTeX формат
            latex_constraint = latex_constraint.replace("*", r"\cdot")
            latex_constraints.append(f"{latex_constraint}")
        return latex_constraints

    def print_latex(self) -> None:
        """
        Друкує обмеження у форматі LaTeX.
        """
        latex_constraints = self.to_latex()
        for constraint in latex_constraints:
            print(constraint)
