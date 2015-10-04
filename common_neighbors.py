import csv

def common_neighbors(test_g, train_g):
    csvfile = file("common_neighbors.csv","wb")
    writer = csv.writer(csvfile)
    writer.writerow(['node1',"node2","num_common_neighbors","positive"])
    for edge in test_g.edges(data=True):
        node_one, node_two, tag = edge[0], edge[1], edge[2]['positive']
        num_common_neighbors = 0
        try:
            neighbors_one, neighbors_two = train_g.neighbors(node_one), train_g.neighbors(node_two)
            for neighbor in neighbors_one:
                if neighbor in neighbors_two:
                    num_common_neighbors += 1
        except:
            pass
        writer.writerow([node_one, node_two, num_common_neighbors,tag])
    csvfile.close()
