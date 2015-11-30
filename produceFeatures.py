import networkx as nx
import random
import multiprocessing as mp
from getSequenceFeatures import AllFeatures

def getAll(start, end):
    for i in xrange(start, end):
        path = "data"
        f1 = open(path+"/graph"+str(i-1)+".txt", "rb")
        f2 = open(path+"/graph"+str(i)+".txt", "rb")
        n_f = open(path+"/neg"+str(i)+".txt", "rb")
        p_f = open(path+"/pos"+str(i)+".txt", "rb")

        g1 = nx.read_edgelist(f1, nodetype=int, data=(('timestamp', int),))
        g2 = nx.read_edgelist(f2, nodetype=int, data=(('timestamp', int),))

        neg = nx.read_edgelist(n_f, nodetype=int, data=(('timestamp', int),))
        pos = nx.read_edgelist(p_f, nodetype=int, data=(('timestamp', int),))

        f1.close(); f2.close(); n_f.close(); p_f.close()

        neg_edges, pos_edges = neg.edges(), pos.edges()
        #some bug in data generation phase, looks a little strange here
        if len(neg_edges) > 2*len(pos_edges):
            neg_edges = random.sample(neg_edges, 2*len(pos_edges))

        f = open("result/features"+str(i)+".csv","wb")
        f.write("cn,aa,ra,jc,pa,delta_cn, delta_aa, delta_ra, delta_jc, delta_pa, postive\n")
        for edge in pos_edges:
            u, v = edge[0], edge[1]
            features = AllFeatures(u, v, g1, g2)
            if features:
                f.write(str(features["cn"])+","+str(features["aa"])
                    +","+str(features["ra"])+","+str(features["jc"])
                    +","+str(features["pa"])+","+str(features["delta_cn"])
                    +","+str(features["delta_aa"])+","+str(features["delta_ra"])
                    +","+str(features["delta_jc"])+","+str(features["delta_pa"])+",True\n")

        for edge in neg_edges:
            u, v = edge[0], edge[1]
            features = AllFeatures(u, v, g1, g2)
            if features:
                f.write(str(features["cn"])+","+str(features["aa"])
                    +","+str(features["ra"])+","+str(features["jc"])
                    +","+str(features["pa"])+","+str(features["delta_cn"])
                    +","+str(features["delta_aa"])+","+str(features["delta_ra"])
                    +","+str(features["delta_jc"])+","+str(features["delta_pa"])+",False\n")

        f.close()
        print "++++++++++++++++ Generate feature"+str(i)+"++++++++++++++++++"

if __name__ == "__main__":
    num_threads = 25
    for i in range(num_threads):
        p = mp.Process(target=getAll, args=(i,i+1))
        p.start()
