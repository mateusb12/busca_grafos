import os
import imageio
import networkx as nx
import networkx.classes.graph as NxGraph
import matplotlib.pyplot as plt

from graph_generator import GraphCreator, GraphType


# noinspection PyAttributeOutsideInit
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

    def reset_graph(self):
        for node in self.graph.nodes:
            self.graph.nodes[node]["color"] = "mediumblue"
            self.graph.nodes[node]["is_visited"] = False

    def generate_backtrack_list(self, origin_node: int, target_node: int) -> list:
        backtrack_list = []
        c = target_node
        while self.graph.nodes[c]["parent"] is not None:
            backtrack_list.append(c)
            c = self.graph.nodes[c]["parent"]
        backtrack_list.append(origin_node)
        backtrack_list.reverse()
        return backtrack_list

    def breadth_first_search(self, origin: int, target: int) -> dict:
        stack = [origin]
        expanded_nodes = []

        while stack:
            current_node = stack.pop(0)
            self.graph.nodes[current_node]["color"] = "red"
            self.draw_graph()
            if current_node == target:
                self.graph.nodes[current_node]["color"] = "green"
                self.draw_graph()
                backtrack_list = self.generate_backtrack_list(origin, target)
                return {"target_node": self.graph.nodes[current_node],
                        "path": backtrack_list,
                        "expanded_nodes": expanded_nodes}
            else:
                self.graph.nodes[current_node]["is_visited"] = True
                for neighbour in self.graph.nodes[current_node]["neighbours"]:
                    if not self.graph.nodes[neighbour]["is_visited"] and neighbour not in stack:
                        self.graph.nodes[neighbour]["color"] = "orange"
                        stack.append(neighbour)
                        expanded_nodes.append(neighbour)
                        self.graph.nodes[neighbour]["parent"] = current_node
                        self.draw_graph()
                self.graph.nodes[current_node]["color"] = "gray"

        return {None: None}

    def is_node_leaf(self, input_node: int) -> bool:
        return bool(
            len(self.graph.nodes[input_node]["neighbours"]) == 1
            and self.graph.nodes[self.graph.nodes[input_node]["neighbours"][0]][
                "is_visited"
            ]
        )

    def depth_first_search(self, origin: int, target: int) -> dict:
        n = len(self.graph.nodes)
        expanded_nodes = []
        self.dfs_target_node = None

        def dfs(at):
            aux = self.graph.nodes[at]
            neighbours = self.graph.nodes[at]["neighbours"]
            is_leaf = self.is_node_leaf(at)
            if self.graph.nodes[at]["label"] == target:
                self.graph.nodes[at]["color"] = "green"
                self.draw_graph()
                self.dfs_target_node = aux
                return None
            else:
                self.graph.nodes[at]["is_visited"] = True
                self.graph.nodes[at]["color"] = "red"
                if is_leaf:
                    self.graph.nodes[at]["color"] = "grey"
                self.draw_graph()
                for neighbour in neighbours:
                    if self.graph.nodes[neighbour]["is_visited"] is False:
                        expanded_nodes.append(neighbour)
                        self.graph.nodes[neighbour]["parent"] = at
                        self.graph.nodes[neighbour]["color"] = "orange"
                        self.draw_graph()
                        dfs(neighbour)
                    else:
                        if self.graph.nodes[neighbour]["color"] != "grey":
                            self.graph.nodes[neighbour]["color"] = "grey"
                            self.draw_graph()

        dfs(origin)
        dfs_result = {"target_node": self.dfs_target_node,
                      "path": self.generate_backtrack_list(origin, target),
                      "expanded_nodes": expanded_nodes}
        return {None: None}


gc = GraphCreator()
# G = gc.create_default_graph(GraphType.dfs)
G = gc.create_random_albert_graph()
gs = GraphSearch(G)
result = gs.depth_first_search(0, 10)
# gs.assemble_gif("depth_first_search.gif")
# apple = 5 + 2
