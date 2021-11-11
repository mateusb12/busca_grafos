from graph_generator import GraphCreator, GraphType
from nx import GraphSearch


class GraphTest:
    def __init__(self):
        self.gc = GraphCreator()

    def test_bfs(self):
        G = self.gc.create_squared_graph(width=8, height=8, holes=20,
                                         seed=150, color="darkslateblue")
        self.gc.plot_squared_graph(G)
        gs = GraphSearch(G)
        result = gs.breadth_first_search((0, 0), (7, 7))
        gs.assemble_gif("breadth_first_search.gif")
        print(result)

    def test_dfs(self):
        G = self.gc.create_squared_graph(width=8, height=8, holes=20,
                                         seed=150, color="darkslateblue")
        self.gc.plot_squared_graph(G)
        gs = GraphSearch(G)
        result = gs.depth_first_search((0, 0), (7, 7))
        gs.assemble_gif("depth_first_search.gif")
        print(result)

    def test_uniform_cost(self):
        G = self.gc.create_squared_graph(width=8, height=8, holes=20,
                                         seed=150, color="darkslateblue")
        gs = GraphSearch(G)
        self.gc.plot_squared_graph(G)
        result = gs.uniform_cost_search((0, 0), (7, 7))
        gs.assemble_gif("uniform_cost_search.gif")
        print(result)

    def test_best_first_search(self, **kwargs):
        G = self.gc.create_squared_graph(width=12, height=12, holes=30,
                                         seed=150, color="darkslateblue")
        gs = GraphSearch(G)
        self.gc.plot_squared_graph(G)
        result = gs.best_first_search((0, 0), (7, 7))
        gs.assemble_gif("best_first_search.gif")
        print(result)

    def test_a_star(self, **kwargs):
        G = self.gc.create_squared_graph(width=12, height=12, holes=30,
                                         seed=150, color="darkslateblue")
        gs = GraphSearch(G)
        self.gc.plot_squared_graph(G)
        result = gs.a_star_search((0, 0), (7, 7))
        gs.assemble_gif("a_star_search.gif")
        print(result)


gt = GraphTest()
gt.test_a_star()
