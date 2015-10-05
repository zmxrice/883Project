
import networkx as nx
import random
import math

from common_neighbors import common_neighbors
from util import *

"""
This is the entrance of this project
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
"""

if __name__ == "__main__":
    filename="facebook_combined.txt"
    pos_num=20000
    neg_num=20000
    model="single"
    model="combined"
    combine_num=5
    g,sample_g=createGraphFromFile(filename)
    train_pos_sample,train_neg_sample=sample_extraction(g,pos_num,neg_num)
    train_data=feature_extraction(g,train_pos_sample,train_neg_sample,model,combine_num)


