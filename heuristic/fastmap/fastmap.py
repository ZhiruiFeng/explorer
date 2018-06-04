import networkx as nx
import operator
from random import choice

C = 3

def readgraph(infile):
    G = nx.Graph()
    with open(infile) as f:
        l = f.readline()
        while l:
            node1, node2, weight = l.strip().split()
            G.add_edge(node1, node2, weight=float(weight))
            l = f.readline()
    return G

def difastmap(G, K, epsilon):
    NG = G.copy()
    embedding = {}
    # initial the embedding as a dict
    for node in list(NG.nodes()):
        embedding[node]=[]
    for r in range(K):
        node_a = choice(list(NG.nodes()))
        node_b = node_a
        # Find the farthest nodes a, b
        for t in range(C):
            length = nx.single_source_dijkstra_path_length(NG, node_a)
            node_c = max(length.items(), key=operator.itemgetter(1))[0]
            if node_c == node_b:
                break
            else:
                node_b = node_a
                node_a = node_c
        length_a = nx.single_source_dijkstra_path_length(NG, node_a)
        length_b = nx.single_source_dijkstra_path_length(NG, node_b)
        dis_ab = length_a[node_b]
        if dis_ab < epsilon:
            break
        # Calcute the embedding
        for node in list(NG.nodes()):
            p_ir = float(length_a[node]+dis_ab-length_b[node])/2
            embedding[node].append(p_ir)
        # Update the weight of the graph
        for i, j in NG.edges():
            w = NG[i][j]['weight']
            NG[i][j]['weight'] = w - abs(embedding[i][r]-embedding[j][r])
    return embedding

if __name__ == "__main__":
    infile = "../test/undirected_4_4"
    G = readgraph(infile)
    print(G.nodes())
    embedding = fastmap(G, 3, 0.01)
    print(embedding)
