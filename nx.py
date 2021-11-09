import collections
import os
import random
from collections import OrderedDict

import imageio
import networkx as nx
import networkx.classes.graph as NxGraph
import matplotlib.pyplot as plt
import numpy as np

from graph_generator import GraphCreator
from priority_dict import PriorityList


class GraphSearch:
    def __init__(self, graph: NxGraph):
        self.G = graph
        self.image_index = 1
        self.folder = "resources"
        self.filenames = []
        self.priority_queue: PriorityList = PriorityList()

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
        my_pos = nx.spring_layout(self.G, seed=100)
        raw_colors = [n[1]['color'] for n in self.G.nodes(data=True)]
        nx.draw(self.G, pos=my_pos, with_labels=1, node_size=500,
                node_color=raw_colors, font_color='white', edge_color='black')
        background_color = 'white'
        ax.set_facecolor(background_color)
        ax.axis('off')
        fig.set_facecolor(background_color)
        self.save_graph()
        plt.show()

    def draw_weighted_graph(self):
        fig, ax = plt.subplots()
        labels = nx.get_edge_attributes(self.G, 'weight')
        pos = nx.spring_layout(self.G, seed=100, k=0.3 * 1 / np.sqrt(len(self.G.nodes())))
        raw_colors = [n[1]['color'] for n in self.G.nodes(data=True)]
        nx.draw(self.G, pos=pos, with_labels=1, node_size=300, font_weight="bold",
                node_color=raw_colors, font_color='white', edge_color='black')
        nx.draw_networkx_edge_labels(self.G, pos=pos, edge_labels=labels,
                                     font_color='indigo', font_size=11,
                                     alpha=0.8, rotate=False)
        self.save_graph()
        plt.show()

    def reset_graph(self):
        for nd in self.G.nodes:
            self.G.nodes[nd]["color"] = "mediumblue"
            self.G.nodes[nd]["is_visited"] = False

    def get_node(self, node_id: int) -> dict:
        return self.G.nodes[node_id]

    def generate_backtrack_list(self, origin_node: int, target_node: int) -> list:
        backtrack_list = []
        c = target_node
        while self.G.nodes[c]["parent"] is not None:
            backtrack_list.append(c)
            aux = self.G.nodes[c]
            if type(aux["parent"]) is not dict:
                c = aux["parent"]
            else:
                c = aux["parent"]["label"]
        backtrack_list.append(origin_node)
        backtrack_list.reverse()
        return backtrack_list

    def breadth_first_search(self, origin: int, target: int) -> dict:
        stack = [origin]
        expanded_nodes = []

        while stack:
            current_node = stack.pop(0)
            self.G.nodes[current_node]["color"] = "red"
            self.draw_graph()
            if current_node == target:
                self.G.nodes[current_node]["color"] = "green"
                self.draw_graph()
                backtrack_list = self.generate_backtrack_list(origin, target)
                return {"target_node": self.G.nodes[current_node],
                        "path": backtrack_list,
                        "expanded_nodes": expanded_nodes}
            else:
                self.G.nodes[current_node]["is_visited"] = True
                for neighbour in self.G.nodes[current_node]["neighbours"]:
                    if not self.G.nodes[neighbour]["is_visited"] and neighbour not in stack:
                        self.G.nodes[neighbour]["color"] = "orange"
                        stack.append(neighbour)
                        expanded_nodes.append(neighbour)
                        self.G.nodes[neighbour]["parent"] = current_node
                        self.draw_graph()
                self.G.nodes[current_node]["color"] = "gray"

        return {None: None}

    def is_node_leaf(self, input_node: int) -> bool:
        return bool(
            len(self.G.nodes[input_node]["neighbours"]) == 1
            and self.G.nodes[self.G.nodes[input_node]["neighbours"][0]][
                "is_visited"
            ]
        )

    def depth_first_search(self, origin: int, target: int) -> dict:
        n = len(self.G.nodes)
        expanded_nodes = []
        self.dfs_target_node = None

        def dfs(at):
            aux = self.G.nodes[at]
            neighbours = self.G.nodes[at]["neighbours"]
            is_leaf = self.is_node_leaf(at)
            if self.G.nodes[at]["label"] == target:
                self.G.nodes[at]["color"] = "green"
                self.draw_graph()
                self.dfs_target_node = aux
                return None
            else:
                self.G.nodes[at]["is_visited"] = True
                self.G.nodes[at]["color"] = "red"
                if is_leaf:
                    self.G.nodes[at]["color"] = "grey"
                self.draw_graph()
                for neighbour in neighbours:
                    if self.G.nodes[neighbour]["is_visited"] is False:
                        expanded_nodes.append(neighbour)
                        self.G.nodes[neighbour]["parent"] = at
                        self.G.nodes[neighbour]["color"] = "orange"
                        self.draw_graph()
                        dfs(neighbour)
                    else:
                        if self.G.nodes[neighbour]["color"] != "grey":
                            self.G.nodes[neighbour]["color"] = "grey"
                            self.draw_graph()

        dfs(origin)
        dfs_result = {"target_node": self.dfs_target_node,
                      "path": self.generate_backtrack_list(origin, target),
                      "expanded_nodes": expanded_nodes}
        return {None: None}

    def backtrack_distance(self, input_node_index: int) -> int:
        total_distance = 0
        current_node_index = input_node_index
        current_node = self.get_node(input_node_index)
        parent = current_node["parent"]
        while parent is not None:
            parent_cost = parent["connections"][current_node_index]
            total_distance += parent_cost
            current_node = parent
            parent = current_node["parent"]
        return total_distance

    def has_connections(self, node_a: int, node_b: int) -> bool:
        return node_a in self.G.nodes[node_b]["neighbours"]

    def get_father(self, input_node: int) -> list:
        neighbours = self.G.nodes[input_node]["neighbours"]
        for neighbour in neighbours:
            aux = self.G.nodes[neighbour]
            if aux["is_visited"] is True and aux["parent"]:
                return aux

    def change_color(self, node_index: int, new_color: str):
        self.G.nodes[node_index]["color"] = new_color
        self.draw_weighted_graph()

    def uniform_cost_search(self, origin: int, target: int) -> dict:
        current_index = origin
        origin_node = self.G.nodes[origin]
        origin_node["is_visited"] = True
        for children in origin_node["neighbours"]:
            children_node = self.get_node(children)
            distance = origin_node["connections"][children]
            children_node["parent"] = origin_node
            children_node["distance_to_origin"] = distance
        # self.change_color(origin, "red")

        expanded_nodes = []

        for _ in range(10):
            current_node = self.G.nodes[current_index]
            if current_node["label"] == target:
                current_node["parent"] = self.get_father(current_index)
                ucs_result = {"target_node": current_node,
                              "path": self.generate_backtrack_list(origin, target),
                              "expanded_nodes": []}
                self.change_color(current_node["label"], "green")
                return current_node
            parent = current_node["parent"]
            if not parent:
                current_node["parent"] = self.get_father(current_index)

            current_node["is_visited"] = True
            current_neighbours = current_node["neighbours"]
            current_connections = current_node["connections"]
            self.change_color(current_node["label"], "red")
            for neighbour in current_neighbours:
                neighbour_node = self.G.nodes[neighbour]
                if neighbour_node["is_visited"] is False:
                    raw_distance = current_connections[neighbour]
                    full_distance = raw_distance + current_node["distance_to_origin"]
                    neighbour_node["distance_to_origin"] = full_distance
                    expanded_nodes.append(neighbour)
                    self.change_color(neighbour, "orange")
                    self.priority_queue.add(neighbour, full_distance)

            self.change_color(current_index, "gray")
            new_index = self.priority_queue.pop(0)[0]
            current_index = new_index

        return {None: None}


if __name__ == "__main__":
    gc = GraphCreator()
    # G = gc.create_default_graph(GraphType.dfs)
    # gs = GraphSearch(G)
    # G = gc.create_random_weighted_graph(size=10, probability=0.35, seed=7)
    # gc.plot_weighted_graph(G)
    # result = gs.depth_first_search(0, 4)
    # # result = gs.uniform_cost_search(9, 8)
    # gs.assemble_gif("depth_first_search.gif")
    # # apple = 5 + 2
