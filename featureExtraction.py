__author__ = 'easycui'
from Cuifeatures import *
import networkx as nx
import numpy as np
def featureExtraction(G):
    for edge in G.edges():
        node_one, node_two = edge[0], edge[1]
        common_neighbors(node_one,node_two,G)
