from collections import defaultdict

class Graph(object):

    def __init__(self):
        self.edges = defaultdict(set)

    def __getitem__(self, item):
        return self.edges[item]

    def __iter__(self):
        return self.edge_lists()

    def add_edge(self, a, b):
        self[a].add(b)
        self[b].add(a)

    def vertices(self):
        for vertex in self.edges.keys():
            yield vertex

    def edge_lists(self):
        for vertex, edge_list in self.edges.items():
            yield vertex, edge_list


def print_graph(graph):
    for vertex, edge_list in graph:
        print(vertex, ": ", edge_list, sep="")
