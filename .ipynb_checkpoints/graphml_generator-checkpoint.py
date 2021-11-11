import networkx as nx
import osmnx as ox
import random


# Create a random unequal nx graph using random labels
def create_random_graph(n: int, m: int, labels: bool = True) -> nx.Graph:
    print("Creating graph!")
    g = nx.gnm_random_graph(n, m)
    print("g")
    if labels:
        for node in g.nodes:
            g.nodes[node]['value'] = random.randint(0, 100)
    return g


def create_city_graphml(city_name: str):
    G = ox.graph_from_place(city_name, network_type='drive')
    ox.plot_graph(G)
    ox.save_graphml(G, filepath=f'{city_name}.graphml')


# Convert a nx graph to graphml
def convert_to_graphml(g: nx.Graph, filename: str) -> None:
    nx.write_graphml(g, filename)


# gr = create_random_graph(10, 20, labels=True)
# convert_to_graphml(gr, 'example.graphml')


# create_city_graphml("Fortaleza, Brazil")