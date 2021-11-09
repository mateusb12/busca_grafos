from graph_generator import GraphCreator, GraphType
from nx import GraphSearch


class GraphTest:
    def __init__(self):
        self.gc = GraphCreator()

    def test_bfs(self):
        # G = self.gc.create_default_graph(GraphType.bfs)
        G = self.gc.create_random_albert_graph(34)
        gs = GraphSearch(G)
        result = gs.breadth_first_search(1, 5)
        gs.assemble_gif("breadth_first_search.gif")

    def test_dfs(self):
        G = self.gc.create_random_albert_graph(34)
        # G = self.gc.create_default_graph(GraphType.dfs)
        gs = GraphSearch(G)
        result = gs.depth_first_search(0, 4)
        gs.assemble_gif("depth_first_search.gif")

    def test_uniform_cost(self):
        G = self.gc.create_random_weighted_graph(size=20, probability=0.35, seed=7)
        # G = self.gc.create_raw_weighted_graph()
        gs = GraphSearch(G)
        # self.gc.plot_weighted_graph(G)
        result = gs.uniform_cost_search(0, 5)
        gs.assemble_gif("uniform_cost_search.gif")


gt = GraphTest()
gt.test_dfs()
