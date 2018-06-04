import networkx as nx
import operator
from random import choice
import matplotlib.pyplot as plt
from fastmap.analyse import nrmsd, dinrmsd
from fastmap.utils import readDiGraph
import math

C = 10

def combine_length(length_o, length_i, embedding, the_node, r, alg='L1'):
    nodes = list(embedding.keys())
    length = {}
    for node in nodes:
        if node in length_o:
            lo = length_o[node]
        else:
            print("[combine_length]:Not a strongly connected graph.")
            exit
        if node in length_i:
            li = length_i[node]
        else:
            print("[combine_length]:Not a strongly connected graph.")
            exit
        if alg == 'L1':
            length[node] = float(li + lo)/2
        elif alg == 'L2':
            length[node] = (float(li + lo)/2)**2
        i = 0
        while i < r:
            if alg == 'L1':
                length[node] -= abs(embedding[node][i]-embedding[the_node][i])
            elif alg == 'L2':
                length[node] -= (embedding[node][i]-embedding[the_node][i])**2
            i = i+1
    return length

def diff_length(length_o, length_i, embedding, the_node, r, alg='L1'):
    nodes = list(embedding.keys())
    length = {}
    for node in nodes:
        if node in length_o:
            lo = length_o[node]
        else:
            print("[diff_length]:Not a strongly connected graph.")
            exit
        if node in length_i:
            li = length_i[node]
        else:
            print("[diff_length]:Not a strongly connected graph.")
            exit
        if alg == 'L1':
            length[node] = abs(float(li - lo)/2)
        elif alg == 'L2':
            length[node] = (float(li - lo)/2)**2
        i = 0
        while i < r:
            if alg == 'L1':
                length[node] -= abs(embedding[node][i]-embedding[the_node][i])
            elif alg == 'L2':
                length[node] -= (embedding[node][i]-embedding[the_node][i])**2
            i = i+1
    return length

def store_distances(G, dis_store, pnode, length_o, length_i):
    if pnode not in dis_store['pivots']:
        dis_store['pivots'].add(pnode)
        for node in G.nodes():
            if node not in length_i.keys() or node not in length_o.keys():
                print("[store_distances]:Not a strongly connected graph.")
                exit
            dis_store[node][pnode] = length_i[node]
            dis_store[node]['-'+str(pnode)] = length_o[node]

def difastmap_combine(G, K, epsilon, dis_store, alg='L1'):
    NG = G.copy()
    RG = nx.reverse(NG)
    embedding = {}
    # initial the embedding as a dict
    for node in list(NG.nodes()):
        embedding[node]=[]
    for r in range(K):
        #for i,j in NG.edges():
        #    print(i+" "+j+" "+str(NG[i][j]['weight']))
        node_a = choice(list(NG.nodes()))
        node_b = node_a
        # Find the farthest nodes a, b
        for t in range(C):
            length_o = nx.single_source_dijkstra_path_length(NG, node_a)
            length_i = nx.single_source_dijkstra_path_length(RG, node_a)
            length = combine_length(length_o, length_i, embedding, node_a, r, alg)
            node_c = max(length.items(), key=operator.itemgetter(1))[0]
            if node_c == node_b:
                break
            else:
                node_b = node_a
                node_a = node_c
        length_oa = nx.single_source_dijkstra_path_length(NG, node_a)
        length_ia = nx.single_source_dijkstra_path_length(RG, node_a)
        length_a = combine_length(length_oa, length_ia, embedding, node_a, r, alg)
        store_distances(G, dis_store, node_a, length_oa, length_ia)
        length_ob = nx.single_source_dijkstra_path_length(NG, node_b)
        length_ib = nx.single_source_dijkstra_path_length(RG, node_b)
        length_b = combine_length(length_ob, length_ib, embedding, node_b, r, alg)
        store_distances(G, dis_store, node_b, length_ob, length_ib)
        dis_ab = length_a[node_b]
        if dis_ab < epsilon:
            break
        # Calcute the embedding
        for node in list(NG.nodes()):
            if alg == 'L1':
                p_ir = float(length_a[node]+dis_ab-length_b[node])/2
            elif alg == 'L2':
                p_ir = float(length_a[node]+dis_ab-length_b[node])/(2*math.sqrt(dis_ab))
            embedding[node].append(p_ir)
    return embedding

def difastmap_diff(G, K, epsilon, dis_store, alg='L1'):
    NG = G.copy()
    RG = nx.reverse(NG)
    embedding = {}
    # initial the embedding as a dict
    for node in list(NG.nodes()):
        embedding[node]=[]
    for r in range(K):
        #for i,j in NG.edges():
        #    print(i+" "+j+" "+str(NG[i][j]['weight']))
        node_a = choice(list(NG.nodes()))
        node_b = node_a
        # Find the farthest nodes a, b
        for t in range(C):
            length_o = nx.single_source_dijkstra_path_length(NG, node_a)
            length_i = nx.single_source_dijkstra_path_length(RG, node_a)
            length = diff_length(length_o, length_i, embedding, node_a, r, alg)
            node_c = max(length.items(), key=operator.itemgetter(1))[0]
            if node_c == node_b:
                break
            else:
                node_b = node_a
                node_a = node_c
        length_oa = nx.single_source_dijkstra_path_length(NG, node_a)
        length_ia = nx.single_source_dijkstra_path_length(RG, node_a)
        length_a = diff_length(length_oa, length_ia, embedding, node_a, r, alg)
        store_distances(G, dis_store, node_a, length_oa, length_ia)
        length_ob = nx.single_source_dijkstra_path_length(NG, node_b)
        length_ib = nx.single_source_dijkstra_path_length(RG, node_b)
        length_b = diff_length(length_ob, length_ib, embedding, node_b, r, alg)
        store_distances(G, dis_store, node_b, length_ob, length_ib)
        dis_ab = length_a[node_b]
        if dis_ab < epsilon:
            break
        # Calcute the embedding
        for node in list(NG.nodes()):
            if alg == 'L1':
                p_ir = float(length_a[node]+dis_ab-length_b[node])/2
            elif alg == 'L2':
                p_ir = float(length_a[node]+dis_ab-length_b[node])/(2*math.sqrt(dis_ab))
            embedding[node].append(p_ir)
    return embedding

if __name__ == "__main__":
    infile = "../test/p2p-Gnutella08_2068_9313"
    G = readDiGraph(infile)
    dis_store = {}
    dis_store['pivots'] = set()
    for node in G.nodes():
        dis_store[node] = {}
    embedding_comb = difastmap_combine(G, 30, 0.01, dis_store, 'L2')
    embedding_diff = difastmap_diff(G, 30, 0.01, dis_store, 'L2')
    #print("combine:" + str(embedding_comb))
    #print("difference:" + str(embedding_diff))
    print("finish embedding")
    distortion = dinrmsd(G, embedding_comb, embedding_diff,dis_store, 200, 'L2')
    print('distortion:' + str(distortion))
