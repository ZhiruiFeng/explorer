import networkx as nx
import operator
from random import choice
import math

C = 10

def fastmap_L1(G, K, epsilon):
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
            if abs(NG[i][j]['weight'])<0.00001:
                NG[i][j]['weight'] = 0
    print("The final dimension of embedding: {}".format(r+1))
    return embedding

def adjust_length(raw_length, embedding, the_node, r):
    nodes = list(embedding.keys())
    length = {}
    for node in nodes:
        length[node] = raw_length[node]**2
        i = 0
        while i < r:
            length[node] -= (embedding[node][i]-embedding[the_node][i])**2
            i = i+1
    return length

def fastmap_L2(G, K, epsilon):
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
            raw_length = nx.single_source_dijkstra_path_length(NG, node_a)
            length = adjust_length(raw_length, embedding, node_a, r)
            node_c = max(length.items(), key=operator.itemgetter(1))[0]
            if node_c == node_b:
                break
            else:
                node_b = node_a
                node_a = node_c
        raw_length_a = nx.single_source_dijkstra_path_length(NG, node_a)
        length_a = adjust_length(raw_length_a, embedding, node_a, r)
        raw_length_b = nx.single_source_dijkstra_path_length(NG, node_b)
        length_b = adjust_length(raw_length_b, embedding, node_b, r)
        dis_ab = length_a[node_b]
        if dis_ab < epsilon:
            break
        # Calcute the embedding
        for node in list(NG.nodes()):
            p_ir = float(length_a[node]+dis_ab-length_b[node])/(2*math.sqrt(dis_ab))
            embedding[node].append(p_ir)

    print("The final dimension of embedding: {}".format(r+1))
    return embedding

def store_undirected_distances(G, dis_store, pnode, raw_length):
    if pnode not in dis_store['pivots']:
        dis_store['pivots'].add(pnode)
        for node in G.nodes():
            dis_store[node][pnode] = raw_length[node]

def fastmap_L1_store(G, K, epsilon, dis_store, PNumber):
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
        if r < PNumber:
            store_undirected_distances(G, dis_store, node_a, nx.single_source_dijkstra_path_length(G, node_a))
            store_undirected_distances(G, dis_store, node_b, nx.single_source_dijkstra_path_length(G, node_b))
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
            if abs(NG[i][j]['weight'])<0.00001:
                NG[i][j]['weight'] = 0
    print("The final dimension of embedding: {}".format(r+1))
    return embedding

def fastmap_L2_store(G, K, epsilon, dis_store, PNumber):
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
            raw_length = nx.single_source_dijkstra_path_length(NG, node_a)
            length = adjust_length(raw_length, embedding, node_a, r)
            node_c = max(length.items(), key=operator.itemgetter(1))[0]
            if node_c == node_b:
                break
            else:
                node_b = node_a
                node_a = node_c
        raw_length_a = nx.single_source_dijkstra_path_length(NG, node_a)
        length_a = adjust_length(raw_length_a, embedding, node_a, r)
        raw_length_b = nx.single_source_dijkstra_path_length(NG, node_b)
        length_b = adjust_length(raw_length_b, embedding, node_b, r)
        if r < PNumber:
            store_undirected_distances(G, dis_store, node_a, raw_length_a)
            store_undirected_distances(G, dis_store, node_b, raw_length_b)
        dis_ab = length_a[node_b]
        if dis_ab < epsilon:
            break
        # Calcute the embedding
        for node in list(NG.nodes()):
            p_ir = float(length_a[node]+dis_ab-length_b[node])/(2*math.sqrt(dis_ab))
            embedding[node].append(p_ir)

    print("The final dimension of embedding: {}".format(r+1))
    return embedding
