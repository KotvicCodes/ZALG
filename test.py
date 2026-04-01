from Graph import Graph

# Directed graph:
graph = Graph(6)
graph.add_or_change_edge(0, 4, 1)
graph.add_or_change_edge(0, 2, 5)
graph.add_or_change_edge(0, 3, 7)
graph.add_or_change_edge(4, 2, 2)
graph.add_or_change_edge(2, 3, 1)
graph.add_or_change_edge(1, 4, 2)
graph.add_or_change_edge(1, 0, 7)
graph.add_or_change_edge(5, 3, 4)
graph.add_or_change_edge(4, 0, 1)

#print("Print the directed graph:")
#print(graph) # depends on your graph representation

print("Directed graph:")
print("Number of nodes:", graph.get_number_of_nodes())
print("Weight from 4 to 0:", graph.get_edge_weight(4,0))
print("Neighbors (descendants) of 0:", list(graph.get_neighbors(0)))
print("List of edges:", graph.get_edges())

# Undirected graph:
print("\nUndirected graph:")
graph1 = Graph(3, False)
graph1.add_or_change_edge(0, 1, 1)
graph1.add_or_change_edge(0, 2, 5)
graph1.add_or_change_edge(1, 0, 4)
assert graph1.get_edge_weight(0, 2) == graph1.get_edge_weight(2, 0) == 5
print("List of edges:", graph1.get_edges())


print("\nTest for components:")
graph2 = Graph(6, directed=False)
graph2.add_or_change_edge(0, 4, 1)
graph2.add_or_change_edge(1, 2, 5)
graph2.add_or_change_edge(1, 3, 7)
graph2.add_or_change_edge(4, 0, 2)
graph2.add_or_change_edge(3, 3, 1)
graph2.add_or_change_edge(4, 0, 3)

print("List of edges:", graph2.get_edges())
print("Components:", graph2.find_connected_components())


print("\nTest for shortest paths:")
start = 0
i = 3
print(f"Shortest paths from {start}:")
distances, previous = graph.shortest_paths(start)
print(f"distances: {distances}, previous: {previous}")
path = graph.reconstruct_the_shortest_path(i, previous)
print(f"from {start} to {i}: ", path)

start = 1
print(f"\nShortest paths from {start}:")
distances, previous = graph.shortest_paths(start)
print(f"distances: {distances}, previous: {previous}")
for i in range(6):
    print(f"from {start} to {i}: ", graph.reconstruct_the_shortest_path(i, previous))