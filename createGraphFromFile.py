import networkx as nx
import random
import math

from common_neighbors import common_neighbors

'''
1.the main method reads from a .txt file and convert the edge list into a graph
  g.nodes() is the list of nodes
  g.edges() is the list of edges

2.10% edges is randomly deleted from the graph, together with 10% randomly
  created non-existing edges(at a distance of 2) using nodes from the deleted
  subgraph are treated as test set,the rest is the training set.

3.for each feature calculation subroutine, training graph train_g and test
  graph test_g passed as argument and the subroutine returns the corresponding
  feature value for each test edges.

4.four files will be created when running the main script:
  testing_positive.txt: postive test examples
  testing_negative.txt: negative test examples
  testing_combined.txt: combine postive and negative examples in the same file
  training.txt: training examples

5.keep in mind that test nodes may not be in the training set.
'''
if __name__ == "__main__":
    f = open("facebook_combined.txt", "rb")
    g = nx.read_edgelist(f)
    num_edges = g.number_of_edges()
    num_nodes = g.number_of_nodes()
    f.close()

    #randomly select 10% edges as test edges
    num_test_edges = int(math.floor(0.1 * num_edges))
    test_edges = random.sample(g.edges(), num_test_edges)
    test_g = nx.Graph()
    test_g.add_edges_from(test_edges, positive="True")
    nx.write_edgelist(test_g, "testing_positive.txt", data=['positive'])

    #adding non-existing edges
    f_negative = open("testing_negative.txt","wb")
    i = 0
    while i < num_test_edges:
        edge = random.sample(test_g.nodes(), 2)
        try:
            shortest_path = nx.shortest_path_length(g,source=edge[0],target=edge[1])
            if shortest_path == 2:
                test_g.add_edge(edge[0],edge[1], positive="False")
                f_negative.write(str(edge[0])+" "+str(edge[1])+" False\n")
                i += 1
        except:
            pass
    f_negative.close()

    nx.write_edgelist(test_g, "testing_combined.txt", data = ["positive"])

    #remove the selected 10% edges, the rest is the training set
    g.remove_edges_from(test_edges)
    train_g = g
    nx.write_edgelist(train_g, "training.txt", data = False)
    '''
	call subroutines down here, all subroutines should have train_g, test_g as the arguments.
	calculate the feature for each edge in the test graph test_g, and output the corresponding file
	for the corresponding feature using training graph train_g. (e.g. "common_neighbors.txt")
    '''
    common_neighbors(test_g, train_g)
