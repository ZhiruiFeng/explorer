import networkx as nx
import numpy as np
import math
from random import sample

def nrmsd(G, embedding, S, alg = 'L1'):
    if S<=1:
        print("S should bigger than 1")
        exit
    subset = sample(list(G.nodes()), S)
    sigma = 0
    ave_d = 0
    for i in range(S):
        node_1 = subset[i]
        emb_1 = np.array(embedding[node_1])
        length = nx.single_source_dijkstra_path_length(G, node_1)
        for j in range(S):
            node_2 = subset[j]
            emb_2 = np.array(embedding[node_2])
            distance = length[node_2]
            if alg == 'L1':
                embdis = np.sum(np.abs(emb_1-emb_2))
            elif alg == 'L2':
                embdis = math.sqrt(np.dot(emb_1-emb_2, emb_1-emb_2))
            sigma += (distance-embdis)*(distance-embdis)
            ave_d += distance
    base = S*S
    sigma = math.sqrt(float(sigma)/base)
    ave_d = float(ave_d)/base
    return float(sigma)/ave_d

def dinrmsd(G, embedding_comb, embedding_diff, S, alg = 'L1'):
    if S<=1:
        print("S should bigger than 1")
        exit
    subset = sample(list(G.nodes()), S)
    sigma = 0
    ave_d = 0
    for i in range(S):
        node_1 = subset[i]
        embcomb_1 = np.array(embedding_comb[node_1])
        embdiff_1 = np.array(embedding_diff[node_1])
        length = nx.single_source_dijkstra_path_length(G, node_1)
        for j in range(S):
            node_2 = subset[j]
            embcomb_2 = np.array(embedding_comb[node_2])
            embdiff_2 = np.array(embedding_diff[node_2])
            distance = length[node_2]
            if alg == 'L1':
                embdis_comb = np.sum(np.abs(embcomb_1-embcomb_2))
                embdis_diff = np.sum(np.abs(embdiff_1-embdiff_2))
            elif alg == 'L2':
                embdis_comb = math.sqrt(np.dot(embcomb_1-embcomb_2, embcomb_1-embcomb_2))
                embdis_diff = math.sqrt(np.dot(embdiff_1-embdiff_2, embdiff_1-embdiff_2))
            distance_reverse = nx.dijkstra_path_length(G, node_2, node_1)
            if distance >= distance_reverse:
                embdis = embdis_comb + embdis_diff
            else:
                embdis = embdis_comb - embdis_diff
            sigma += (distance-embdis)*(distance-embdis)
            ave_d += distance
    base = S*S
    sigma = math.sqrt(float(sigma)/base)
    ave_d = float(ave_d)/base
    return float(sigma)/ave_d
