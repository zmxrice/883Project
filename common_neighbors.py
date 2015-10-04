def common_neighbors(test_g, train_g):
    f = open("common_neighbors.txt","wb")
    for edge in test_g.edges():
        node_one, node_two = edge[0], edge[1]
        num_common_neighbors = 0
        try:
            neighbors_one, neighbors_two = train_g.neighbors(node_one), train_g.neighbors(node_two)
            for neighbor in neighbors_one:
                if neighbor in neighbors_two:
                    num_common_neighbors += 1
        except:
            pass
        f.write(str(node_one)+" "+str(node_two)+" "+str(num_common_neighbors)+"\n")

    f.close()
