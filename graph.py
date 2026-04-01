class Graph:
    """
    Representation of a graph (directed or undirected, with positive edge weights).
    You may choose the internal representation, e.g., adjacency list (with weights) or
    adjacency/distance matrix.
    """

    def __init__(self, number_of_nodes, directed=True):
        """Initialize the graph with a given number of nodes and orientation.

        Args:
            number_of_nodes (int): Number of nodes in the graph.
            directed (bool): True for a directed graph, False for undirected.

        Exception handling:
            Check that number_of_nodes is a non-negative integer. Raise ValueError if invalid.
        """
        ...

    def add_or_change_edge(self, u, v, weight=1):
        """Add a new edge or change the weight of an existing edge from node u to node v.

        To remove an edge, set weight = None.
        Behavior may differ depending on whether the graph is directed or not.

        Exception handling:
           Check that 0 <= u, v < number_of_nodes.
           Check that weight is positive number or None (for removal).
           Raise ValueError or IndexError if invalid.

        """
        ...

    def get_edge_weight(self, u, v):
        """Return the weight of the edge from u to v.

        Returns None if the edge does not exist.

        Exception handling:
            Check valid node indices. Raise ValueError or IndexError if invalid.
        """
        ...

    def get_number_of_nodes(self):
        """Return the total number of nodes in the graph."""
        ...

    def get_neighbors(self, u):
        """Return a list of all neighbors (reachable nodes) from node u.

        Example: [1, 3, 8]

        Exception handling:
            Raise ValueError or IndexError if u is out of range.
            Return empty list if u has no neighbors.
        """
        ...

    def __str__(self):
        """Return a string representation of the graph 
        based on the internal structure (e.g., adjacency matrix or list).
        """
        ...

    def get_edges(self):
        """Return a list of all edges in the graph.

        Each edge is represented as a tuple: ((u, v), weight)

        Example output:
        [((0, 1), 1), ((1, 2), 1)]         # directed
        or
        [((0, 1), 1), ((1, 2), 1)]         # undirected (only one per pair, u <= v)
        """
        ...

    def find_connected_components(self):
        """Return a list of connected components in the undirected graph.

        Each component is represented as a list or set of nodes.

        Example:
            [[0, 2], [1, 3, 7], [4], [5, 6]]
            or
            [{0, 2}, {1, 3, 7}, {4}, {5, 6}]

        Exception handling:
            Raise ValueError if the graph is directed.
        """
        ...
        
    def shortest_paths(self, start):
        """Compute the shortest paths from a start node to all other nodes using the Dijksra algorithm.

        Returns:
            tuple:
                distances (list): distances[i] is the shortest distance from start to node i (or float('inf')).
                previous (list): previous[i] == j means j is the predecessor of i on the shortest path.

        Example:
            ([0, 1, inf, 2], [0, 0, -1, 1])
            for start node 0 and edges (0, 1), (1, 3).

        Exception handling:
            Raise IndexError or ValueError if start is invalid.
            Check for negative weights (if using Dijkstra, weights must be non-negative). Raise ValueError if invalid.

        """
        ...

    def reconstruct_the_shortest_path(self, destination, previous):
        """Return the list of nodes forming the shortest path to node destination.

        'previous' is the list returned by self.shortest_paths(start).

        Example:
            [0, 1, 3] for node 3,
            [] for unreachable node 2
            in a graph with edges (0, 1), (1, 3) and start node 0.

        Exception handling:
            Raise ValueError or IndexError if destination is out of range.
            Check that previous is a list of valid indices or -1. Raise ValueError if invalid.
            Return [] if node is unreachable.
        """
        ...