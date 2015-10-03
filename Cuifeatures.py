import networkx as nx
import random
import math


def Common_Neighbors(a,b,g):
    neighbor_a=g.edge[a]
    neighbor_b=g.edge[b]

    len_a=len(neighbor_a)
    len_b=len(neighbor_b)
    len_both=len(neighbor_a.update(neighbor_b))

    return len_a+len_b-len_both


def Adar(a,b,g):
    return 0


def Pre_att(a,b,g):
    return 0

