# Graph search tool
_Visualizing search within graphs_

## nx.py
- File that has the search algorithms

## graph_generator.py
- File that can create random graphs following some rules

## priority_dict.py
- Data structure to prioritize a list of entities

## unit_tests.py
- File to run the searchs

### `GraphTest class`


- Instantiating the graph class

```sh
gt = GraphTest()
```

### `Breadth first search`
```
gt.test_bfs()
```
### `Depth first search`
```
gt.test_dfs()
```

### `Uniform cost search`
```
gt.test_uniform_cost()
```

### `Greedy search`
```
gt.test_best_first_search()
```

### `A* search`
```
gt.test_a_star()
```