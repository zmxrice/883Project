import networkx as nx
import math


def common_neighbors(a, b, g):
    neighbor_a = g.edge[a]
    neighbor_b = g.edge[b]

    len_a = len(neighbor_a)
    len_b = len(neighbor_b)
    union = neighbor_a.copy()
    union.update(neighbor_b)
    len_both = len(union)

    return len_a + len_b - len_both


def adar(a, b, g):
    intersection = dict()
    ans = 0.0
    neighbor_a = g.edge[a]
    neighbor_b = g.edge[b]

    for i in neighbor_a:
        if neighbor_b.has_key(i):
            intersection[i] = {}
    for i in intersection:
        ans += 1.0 / math.log(len(g.edge[i]), 2)
    return ans


def pre_att(a, b, g):
    neighbor_a = g.edge[a]
    neighbor_b = g.edge[b]
    len_a = len(neighbor_a)
    len_b = len(neighbor_b)
    return len_a * len_b


if __name__ == "__main__":
    g = nx.Graph()
    g.add_nodes_from([1, 2, 3, 4])
    g.add_edges_from([(1, 2), (2, 4), (3, 4), (2, 3)])
