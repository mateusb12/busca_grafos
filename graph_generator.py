from enum import Enum

import networkx as nx
import networkx.classes.graph as NxGraph


class GraphType(Enum):
    bfs = 1
    dfs = 2


class GraphCreator:
    def __init__(self):
        self.raw = nx.Graph()

    @staticmethod
    def handle_adjacency(input_graph: NxGraph, color_table: dict):
        for node in input_graph.adjacency():
            index = node[0]
            content = node[1]
            aux = input_graph.nodes[index]
            aux["label"] = index
            aux["neighbours"] = list(content.keys())
            aux["parent"] = None
            aux["degree"] = len(content)
            aux["is_visited"] = False
            aux["color"] = color_table[index]

    def create_random_albert_graph(self) -> NxGraph:
        albert = nx.random_graphs.barabasi_albert_graph(20, 2)
        keys = list(albert.nodes)
        default_color = "mediumblue"
        values = [default_color] * len(keys)
        colors = dict(zip(keys, values))
        self.handle_adjacency(albert, colors)
        return albert

    @staticmethod
    def create_bfs_mesh():
        return [(0, 9), (0, 7), (0, 11),
                (1, 8), (1, 10),
                (2, 3), (2, 12),
                (3, 2), (3, 4), (3, 7),
                (4, 3),
                (5, 6),
                (6, 5), (6, 7),
                (7, 0), (7, 3), (7, 11),
                (8, 1), (8, 9), (8, 12),
                (9, 0), (9, 10), (9, 8),
                (10, 1), (10, 9),
                (11, 0), (11, 7),
                (12, 2), (12, 8)]

    @staticmethod
    def create_dfs_mesh():
        return [(0, 1), (0, 9),
                (1, 8), (1, 0),
                (2, 3),
                (3, 2), (3, 4), (3, 5), (3, 7),
                (4, 3),
                (5, 3), (5, 6),
                (6, 5), (6, 7),
                (7, 3), (7, 6), (7, 8), (7, 10), (7, 11),
                (8, 1), (8, 7), (8, 9),
                (9, 0), (9, 8),
                (10, 7), (10, 11),
                (11, 7), (11, 10)]

    def create_default_graph(self, model: GraphType) -> NxGraph:
        NG = self.raw
        raw_edges = None
        if model == GraphType.bfs:
            raw_edges = self.create_bfs_mesh()
        elif model == GraphType.dfs:
            raw_edges = self.create_dfs_mesh()
        nodes_amount = len({x[0] for x in raw_edges})
        nodes = list(range(nodes_amount))

        NG.add_nodes_from(nodes)
        NG.add_edges_from(raw_edges)

        default_color = "mediumblue"
        colors = dict(zip(nodes, [default_color] * nodes_amount))

        self.handle_adjacency(NG, colors)
        return NG

    @staticmethod
    def create_default_colors() -> dict:
        return {0: "red", 1: "blue", 2: "green", 3: "yellow", 4: "purple",
                5: "orange", 6: "brown", 7: "pink", 8: "cyan", 9: "black",
                10: "grey", 11: "magenta", 12: "lime"}


if __name__ == "__main__":
    graph_creator = GraphCreator()
    G = graph_creator.create_default_graph(GraphType.dfs)
    apple = 5 + 3
