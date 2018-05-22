import networkx as nx
import operator
from random import choice

C = 3

def readgraph(infile):
    G = nx.DiGraph()
    with open(infile) as f:
        l = f.readline()
        while l:
            node1, node2, weight = l.strip().split()
            G.add_edge(node1, node2, weight=float(weight))
            l = f.readline()
    return G

def combine_length(G, length_o, length_i):
    nodes = list(G.nodes())
    length = {}
    for node in nodes:
        if node in length_o:
            lo = length_o[node]
        else:
            print("Not a strongly connected graph.")
            exit
        if node in length_i:
            li = length_i[node]
        else:
            print("Not a strongly connected graph.")
            exit
        length[node] = float(li + lo)/2
    return length

def difastmap(G, K, epsilon):
    NG = G.copy()
    RG = nx.reverse(NG)
    embedding = {}
    # initial the embedding as a dict
    for node in list(NG.nodes()):
        embedding[node]=[]
    for r in range(K):
        for i,j in NG.edges():
            print(i+" "+j+" "+str(NG[i][j]['weight']))
        node_a = choice(list(NG.nodes()))
        node_b = node_a
        # Find the farthest nodes a, b
        for t in range(C):
            length_o = nx.single_source_dijkstra_path_length(NG, node_a)
            length_i = nx.single_source_dijkstra_path_length(RG, node_a)
            length = combine_length(NG, length_o, length_i)
            node_c = max(length.items(), key=operator.itemgetter(1))[0]
            if node_c == node_b:
                break
            else:
                node_b = node_a
                node_a = node_c
        length_oa = nx.single_source_dijkstra_path_length(NG, node_a)
        length_ia = nx.single_source_dijkstra_path_length(RG, node_a)
        length_a = combine_length(NG, length_oa, length_ia)
        length_ob = nx.single_source_dijkstra_path_length(NG, node_b)
        length_ib = nx.single_source_dijkstra_path_length(RG, node_b)
        length_b = combine_length(NG, length_ob, length_ib)
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
            if NG[i][j]['weight'] < 0:
                NG[i][j]['weight'] = 0
    return embedding

if __name__ == "__main__":
    infile = "../test/directed_4_4"
    G = readgraph(infile)
    embedding = difastmap(G, 3, 0.01)
    print(embedding)
