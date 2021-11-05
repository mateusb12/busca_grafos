import os
import imageio
import networkx as nx
import networkx.classes.graph as NxGraph
import matplotlib.pyplot as plt


class GraphCreator:
    def __init__(self):
        self.raw = nx.Graph()

    def handle_graph_creation(self, **kwargs):
        if kwargs["graph_type"] == "random":
            return self.create_random_albert_graph()
        elif kwargs["graph_type"] == "default":
            return self.create_default_graph()

    @staticmethod
    def handle_adjacency(input_graph: NxGraph, color_table: dict):
        for node in input_graph.adjacency():
            index = node[0]
            content = node[1]
            aux = input_graph.nodes[index]
            aux["neighbours"] = list(content.keys())
            aux["degree"] = len(content)
            aux["is_visited"] = False
            aux["color"] = color_table[index]

    def create_random_albert_graph(self) -> NxGraph:
        albert = nx.random_graphs.barabasi_albert_graph(60, 5)
        keys = list(albert.nodes)
        default_color = "mediumblue"
        values = [default_color] * len(keys)
        colors = dict(zip(keys, values))
        self.handle_adjacency(albert, colors)
        return albert

    def create_default_graph(self) -> NxGraph:
        NG = self.raw
        raw_edges = [(0, 9), (0, 7), (0, 11),
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

        nodes = list(range(1, 13))
        NG.add_nodes_from(nodes)
        NG.add_edges_from(raw_edges)

        default_color = "mediumblue"
        colors = {0: default_color, 1: default_color, 2: default_color, 3: default_color,
                  4: default_color, 5: default_color, 6: default_color, 7: default_color,
                  8: default_color, 9: default_color, 10: default_color, 11: default_color,
                  12: default_color}

        self.handle_adjacency(NG, colors)
        return NG

    @staticmethod
    def create_default_colors():
        return {0: "red", 1: "blue", 2: "green", 3: "yellow", 4: "purple",
                5: "orange", 6: "brown", 7: "pink", 8: "cyan", 9: "black",
                10: "grey", 11: "magenta", 12: "lime"}


class GraphSearch:
    def __init__(self, graph: NxGraph):
        self.graph = graph
        self.image_index = 1
        self.folder = "resources"
        self.filenames = []

    def save_graph(self):
        filename = self.folder + "/graph_" + str(self.image_index) + ".png"
        plt.savefig(filename)
        self.filenames.append(filename)
        self.image_index += 1

    def create_gif(self, filename="graph_animation.gif"):
        with imageio.get_writer(self.folder + '/' + filename, mode='I') as writer:
            for filename in self.filenames:
                image = imageio.imread(filename)
                writer.append_data(image)

    def remove_pictures(self):
        for filename in set(self.filenames):
            os.remove(filename)

    def assemble_gif(self, filename="graph_animation.gif"):
        self.create_gif(filename)
        self.remove_pictures()

    def draw_graph(self):
        fig, ax = plt.subplots()
        my_pos = nx.spring_layout(self.graph, seed=100)
        raw_colors = [n[1]['color'] for n in self.graph.nodes(data=True)]
        nx.draw(G, pos=my_pos, with_labels=1, node_size=500,
                node_color=raw_colors, font_color='white', edge_color='black')
        background_color = 'white'
        ax.set_facecolor(background_color)
        ax.axis('off')
        fig.set_facecolor(background_color)
        self.save_graph()
        plt.show()

    def breadth_first_search(self, origin: int, target: int) -> dict:
        stack = [origin]

        while stack:
            current_node = stack.pop(0)
            self.graph.nodes[current_node]["color"] = "red"
            self.draw_graph()
            if current_node == target:
                self.graph.nodes[current_node]["color"] = "green"
                self.draw_graph()
                return self.graph.nodes[current_node]
            self.graph.nodes[current_node]["is_visited"] = True
            for neighbour in self.graph.nodes[current_node]["neighbours"]:
                if not self.graph.nodes[neighbour]["is_visited"] and neighbour not in stack:
                    self.graph.nodes[neighbour]["color"] = "orange"
                    stack.append(neighbour)
                    self.draw_graph()
            self.graph.nodes[current_node]["color"] = "gray"

        return {None: None}


gc = GraphCreator()
G = gc.handle_graph_creation(graph_type="random")
gs = GraphSearch(G)
result = gs.breadth_first_search(0, 12)
gs.assemble_gif("random_albert_gif.gif")
