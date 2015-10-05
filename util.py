__author__ = 'easycui'
import networkx as nx
import random
import math
import csv
from Cuifeatures import *
def createGraphFromFile(filename):
    f = open(filename, "rb")
    g = nx.read_edgelist(f)
    return g

def sample_extraction(g,pos_num,neg_num):
    pos_sample=[]
    neg_sample=[]

    num_edges = g.number_of_edges()
    num_nodes = g.number_of_nodes()
    #f.close()

    #randomly select pos_num as test edges
    sample_edges = random.sample(list(g.edges()), pos_num)
    sample_g = nx.Graph()
    sample_g.add_edges_from(sample_edges, positive="True")
    nx.write_edgelist(sample_g, "testing_positive.txt", data=['positive'])
    pos_sample=sample_edges


    #adding non-existing edges
    i = 0
    neg_g = nx.Graph()
    while i < neg_num:
        edge = random.sample(list(g.nodes()), 2)
        try:
            shortest_path = nx.shortest_path_length(g,source=edge[0],target=edge[1])
            if shortest_path >= 2:
                neg_g.add_edge(edge[0],edge[1], positive="False")
                neg_sample.append((edge[0],edge[1]))
                i += 1
        except:
            pass

    nx.write_edgelist(neg_g, "sample_negative.txt", data = ["positive"])
    nx.write_edgelist(neg_g.add_edges_from(sample_edges), "sample_combine.txt", data = ["positive"])
    #remove the selected 10% edges, the rest is the training set
    g.remove_edges_from(sample_edges)
    train_g = g
    nx.write_edgelist(train_g, "training.txt", data = False)

    return pos_sample,neg_sample,train_g

def feature_extraction(g,pos_sample,neg_sample,model="single",combine_num=5):

    data=[]
    if model=="single":
        feature_name=common_neighbors
        for i in pos_sample:
            feature = feature_name(i[0],i[1],g)
            data.append([feature,1])
        for i in neg_sample:
            feature = feature_name(i[0],i[1],g)
            data.append([feature,0])
    else:
        feature_set=[common_neighbors,common_neighbors]
        for i in pos_sample:
            features=[]
            for j in feature_set:
                features.append(j(i[0],i[1],g))
            data=features.append(1)
        for i in neg_sample:
            features=[]
            for j in feature_set:
                features.append(j(i[0],i[1],g))
            data=features.append(0)

    return data
def write_feature_to_file(features,filename):
    csvfile = file("filename","wb")
    writer = csv.writer(csvfile)
    for i in features:
        writer.writerow(i)
    csvfile.close()

