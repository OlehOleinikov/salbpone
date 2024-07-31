"""
Модуль формування візуалізації.
"""
from pyvis.network import Network
import networkx as nx

from .data_types import GraphDict, OperationsCosts


def save_procedure_graph(procedure_graph: GraphDict, t: OperationsCosts, file_name: str) -> None:
    """
    Збереження інтерактивного графа послідовностей операцій.
    Зберігається у форматі html, має можливість переміщення нод.

    :param procedure_graph:
    :param t:
    :param file_name:
    :return:
    """
    # Створення направленого графу
    G = nx.DiGraph()

    # Додавання вузлів і ребер до графа
    for node, dependencies in procedure_graph.items():
        for dep in dependencies:
            G.add_edge(dep, node)

    # Створення об'єкту Network для інтерактивного графу
    net = Network(notebook=True, directed=True, cdn_resources='in_line')

    # Додавання вузлів і ребер до Network
    for node in G.nodes:
        label = f"t{node}={t[node-1]}"
        net.add_node(node, label=label)

    for edge in G.edges:
        net.add_edge(edge[0], edge[1])

    # Налаштування фізичних параметрів для збереження положень нод та прямих ліній
    net.set_options("""
    var options = {
      "physics": {
        "enabled": false
      },
      "edges": {
        "smooth": {
          "type": "continuous",
          "forceDirection": "none",
          "roundness": 0
        }
      }
    }
    """)

    # Запис HTML-файлу з кодуванням utf-8
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(net.generate_html())
