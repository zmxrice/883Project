'''
1.The training graph is amazon0312.txt
2.This script will get the newly added edges in amazon0601.txt, while ignoring
those edges which end nodes is not in amazon0312.txt
3.We will use unsupervised learning to predict which edges will be added from
0312 to 0601
'''
import networkx as nx
import time

if __name__ == "__main__":
    start_time = time.clock()
    f1 = open("amazon0312.txt", "rb")
    f2 = open("amazon0601.txt", "rb")
    g1 = nx.read_edgelist(f1)
    g2 = nx.read_edgelist(f2)
    edges2 = g2.edges()
    f1.close(); f2.close()

    temp_graph = nx.Graph()
    for edge in edges2:
        if not g1.has_edge(edge[0],edge[1]) and g1.has_node(edge[0]) and g1.has_node(edge[1]):
            temp_graph.add_edge(edge[0],edge[1])

    nx.write_edgelist(temp_graph, "testing.txt", data = False)
    elapsed_time = time.clock() - start_time
    print "time used", elapsed_time
