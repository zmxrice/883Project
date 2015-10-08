import networkx as nx
import random
import math
from features import *
from util import *

"""

This is the entrance of this project
1.the main method reads from a .txt file and convert the edge list into a graph
  g.nodes() is the list of nodes
  g.edges() is the list of edges //edge is a tuple such as (a,b)

2.Default 10% edges is randomly deleted from the graph, which is the positive sample set, together with 10% randomly
  created non-existing edges(at a distance of 2 or greater than 2)are treated as negative sample set.

3.for each feature calculation subroutine, the graph and a list of samples are passed as argument and the subroutine returns the corresponding
  feature value for each test edges. return is a list of tuple (a,b,v), a and b are the nodes, v is the feature of this edge
  Such as: the_feature_name(g,edges)   ///g is the whole graph, edges is a list of samples.
  write the feature function in "features.py"

4.four files will be created when running the main script:
  sample_positive_num.txt: positive samples
  sample_negative_num.txt: negative samples
  sample_combined_num.txt: all samples in the same file
  features_single_feature_name.csv or features_combined_combine_num.csv

"""


def main(filename="Email-Enron.txt", pos_num=0.1, neg_num=0.1, model="single", combine_num=5,
         feature_name=common_neighbors, neg_mode="hard"):
    """

    :param filename: the graph file
    :param pos_num: the percentage of positive samples in all edges
    :param neg_num: the percentage of negative samples in all edges
    :param model: it can be "single" or "combined"
    :param combine_num: the number of combined features
    :param feature_name: if model is "single", this parameter will be the name of the feature. if model is "combined"
                        this parameter will be the list of features
    :param neg_mode : "easy" means the distance between two nodes in a negative edge is greater than 2. "hard" means
                      it is exactly 2.
    :return:
    """
    g = create_graph_from_file(filename)
    num_edges = g.number_of_edges()
    pos_num = int(num_edges * pos_num)
    neg_num = int(num_edges * neg_num)
    pos_sample, neg_sample = sample_extraction(g, pos_num, neg_num,neg_mode)
    train_data = feature_extraction(g, pos_sample, neg_sample, feature_name, model, combine_num)


if __name__ == "__main__":
    feature_set = [common_neighbors,
                   nx.resource_allocation_index,
                   nx.jaccard_coefficient,
                   nx.adamic_adar_index,
                   nx.preferential_attachment
                   ]
    main(model="combined", combine_num=5, feature_name=feature_set, neg_mode="easy")
