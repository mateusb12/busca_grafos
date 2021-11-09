import itertools
import random
from collections import OrderedDict
from enum import Enum

import networkx as nx
import networkx.classes.graph as NxGraph
import numpy as np
from matplotlib import pyplot as plt


class GraphType(Enum):
    bfs = 1
    dfs = 2





class GraphCreator:
    def __init__(self):
        self.raw = nx.Graph()

    @staticmethod
    def handle_adjacency(input_graph: NxGraph, color_table: dict):
        weighted = GraphCreator.is_graph_weighted(input_graph)
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

            if weighted:
                aux["connections"] = {}
                for end_node, connection in content.items():
                    aux["connections"][end_node] = connection["weight"]
                aux["distance_to_origin"] = 0

    @staticmethod
    def is_graph_weighted(input_graph: NxGraph) -> bool:
        for edge in input_graph.adjacency():
            aux = random.choice(list(edge[1].values())).keys()
            return "weight" in aux

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

    def create_random_weighted_graph(self, size=10, probability=0.5, seed=None, **kwargs):
        if "size" in kwargs:
            size = kwargs["size"]
        if "probability" in kwargs:
            probability = kwargs["probability"]
        if "seed" in kwargs:
            seed = kwargs["seed"]
        new_G = nx.fast_gnp_random_graph(size, probability, seed)
        for e in new_G.edges():
            new_G[e[0]][e[1]]["weight"] = random.randint(12, 20)
        new_G[1][8]["weight"] = 36
        isolates = list(nx.isolates(new_G))
        if isolates:
            for isolate in isolates:
                new_G.remove_node(isolate)
        keys = list(new_G.nodes)
        default_color = "mediumblue"
        values = [default_color] * len(keys)
        colors = dict(zip(keys, values))
        self.handle_adjacency(new_G, colors)
        return new_G

    @staticmethod
    def get_medium_blue_table(input_g: NxGraph):
        keys = list(input_g.nodes)
        default_color = "mediumblue"
        values = [default_color] * len(keys)
        return dict(zip(keys, values))

    def create_raw_weighted_graph(self) -> NxGraph:
        new_G = nx.Graph()
        new_G.add_edge(0, 1, weight=4)
        new_G.add_edge(0, 2, weight=7)
        new_G.add_edge(1, 3, weight=3)
        new_G.add_edge(1, 4, weight=6)
        new_G.add_edge(3, 6, weight=4)
        new_G.add_edge(3, 7, weight=2)
        new_G.add_edge(7, 10, weight=6)
        new_G.add_edge(0, 2, weight=7)
        new_G.add_edge(2, 5, weight=2)
        new_G.add_edge(5, 8, weight=4)
        new_G.add_edge(5, 9, weight=7)
        new_G.add_edge(9, 11, weight=3)
        self.handle_adjacency(new_G, self.get_medium_blue_table(new_G))
        return new_G

    @staticmethod
    def create_default_colors() -> dict:
        return {0: "red", 1: "blue", 2: "green", 3: "yellow", 4: "purple",
                5: "orange", 6: "brown", 7: "pink", 8: "cyan", 9: "black",
                10: "grey", 11: "magenta", 12: "lime"}

    @staticmethod
    def plot_weighted_graph(input_g: nx.DiGraph):
        fig, ax = plt.subplots()
        labels = nx.get_edge_attributes(input_g, 'weight')
        pos = nx.spring_layout(input_g, k=0.3*1/np.sqrt(len(input_g.nodes())))
        nx.draw(input_g, pos=pos, with_labels=1, node_size=500, font_weight="bold",
                node_color="mediumblue", font_color='white', edge_color='black')
        nx.draw_networkx_edge_labels(input_g, pos=pos, edge_labels=labels,
                                     font_color='indigo', font_size=11,
                                     alpha=0.8, rotate=False)
        plt.show()


if __name__ == "__main__":
    graph_creator = GraphCreator()
    # G = graph_creator.create_default_graph(GraphType.dfs)
    G = graph_creator.create_random_weighted_graph(size=10, probability=0.35, seed=7)
    graph_creator.plot_weighted_graph(G)
    # for node in G.nodes():
    #     print(G[node])
    plt.show()
    apple = 5 + 3
