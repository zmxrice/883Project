__author__ = 'easycui'
import networkx as nx
import random
import math
import csv
from features import *


def create_graph_from_file(filename):
    print("----------------build graph--------------------")
    f = open(filename, "rb")
    g = nx.read_edgelist(f)
    return g


def sample_extraction(g, pos_num, neg_num, neg_mode, neg_distance=2, delete=0):
    """

    :param g:  the graph
    :param pos_num: the number of positive samples
    :param neg_num: the number of negative samples
    :param neg_distance: the distance between two nodes in negative samples
    :param delete: if delete ==0, don't delete positive edges from graph
    :return: pos_sample is a list of positive edges, neg_sample is a list of negative edges
    """

    print("----------------extract positive samples--------------------")
    # randomly select pos_num as test edges
    pos_sample = random.sample(g.edges(), pos_num)
    sample_g = nx.Graph()
    sample_g.add_edges_from(pos_sample, positive="True")
    nx.write_edgelist(sample_g, "sample_positive_" + str(pos_num) + ".txt", data=['positive'])

    # adding non-existing edges
    print("----------------extract negative samples--------------------")
    i = 0
    neg_g = nx.Graph()
    while i < neg_num:
        edge = random.sample(g.nodes(), 2)
        try:
            shortest_path = nx.shortest_path_length(g, source=edge[0], target=edge[1])
            if neg_mode == "hard":
                if shortest_path == neg_distance:
                    neg_g.add_edge(edge[0], edge[1], positive="False")
                    i += 1
            elif neg_mode == "easy":
                if shortest_path >= neg_distance:
                    neg_g.add_edge(edge[0], edge[1], positive="False")
                    i += 1
        except:
            pass

    nx.write_edgelist(neg_g, "sample_negative_" + str(neg_num) + ".txt", data=["positive"])
    neg_sample = neg_g.edges()
    neg_g.add_edges_from(pos_sample)
    nx.write_edgelist(neg_g, "sample_combine_" + str(pos_num + neg_num) + ".txt", data=["positive"])

    # remove the positive sample edges, the rest is the training set
    if delete == 0:
        return pos_sample, neg_sample
    else:
        g.remove_edges_from(pos_sample)
        nx.write_edgelist(g, "training.txt", data=False)

        return pos_sample, neg_sample


def feature_extraction(g, pos_sample, neg_sample, feature_name, model="single", combine_num=5):
    """

    :param g:  the graph
    :param pos_sample : the positive samples, it should be a list of edges, such as [(1,2),(2,3)]
    :param neg_sample : the negative samples
    :param feature_name: name of the feature fucntion
    :param model:
    :return: the extracted feature and the last column is the label, "pos" means positive, "neg" means negative
    """

    data = []
    if model == "single":
        print "-----extract feature:", feature_name.__name__, "----------"
        preds = feature_name(g, pos_sample)
        feature = [feature_name.__name__] + [i[2] for i in preds]
        label = ["label"] + ["Pos" for i in range(len(feature))]
        preds = feature_name(g, neg_sample)
        feature1 = [i[2] for i in preds]
        feature = feature + feature1
        label = label + ["Neg" for i in range(len(feature1))]
        data = [feature, label]
        data = transpose(data)
        print("----------write the feature to file---------------")
        write_data_to_file(data, "features_" + model + "_" + feature_name.__name__ + ".csv")
    else:
        label = ["label"] + ["Pos" for i in range(len(pos_sample))] + ["neg" for i in range(len(neg_sample))]
        for j in feature_name:
            print "-----extract feature:", j.__name__, "----------"
            preds = j(g, pos_sample)

            feature = [j.__name__] + [i[2] for i in preds]
            preds = j(g, neg_sample)
            feature = feature + [i[2] for i in preds]
            data.append(feature)

        data.append(label)
        data = transpose(data)
        print("----------write the features to file---------------")
        write_data_to_file(data, "features_" + model + "_" + str(combine_num) + ".csv")
    return data


def write_data_to_file(data, filename):
    csvfile = file(filename, "wb")
    writer = csv.writer(csvfile)
    for i in data:
        writer.writerow(i)
    csvfile.close()


def transpose(data):
    return [list(i) for i in zip(*data)]
