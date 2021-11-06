import os
import imageio
import networkx as nx
import networkx.classes.graph as NxGraph
import matplotlib.pyplot as plt

from graph_generator import GraphCreator, GraphType


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

    def is_node_leaf(self, input_node: dict) -> bool:
        return all(
            self.graph.nodes[item]["is_visited"]
            for item in input_node["neighbours"]
        )

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
                backtrack_list = []
                c = current_node
                while self.graph.nodes[c]["parent"] is not None:
                    backtrack_list.append(c)
                    c = self.graph.nodes[c]["parent"]
                backtrack_list.append(origin)
                backtrack_list.reverse()
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

    def depth_first_search(self, origin: int, target: int) -> dict:
        n = len(self.graph.nodes)

        def dfs(at):
            aux = self.graph.nodes[at]
            neighbours = self.graph.nodes[at]["neighbours"]
            if self.graph.nodes[at]["label"] == target:
                return target
            else:
                self.graph.nodes[at]["is_visited"] = True
                for neighbour in neighbours:
                    if self.graph.nodes[neighbour]["is_visited"] is False:
                        return dfs(neighbour)

        dfs_result = dfs(origin)
        return {None: None}


gc = GraphCreator()
G = gc.create_default_graph(GraphType.bfs)
gs = GraphSearch(G)
result = gs.breadth_first_search(0, 4)
gs.assemble_gif("breadth_first_search2.gif")
