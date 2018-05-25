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

def compare_DiEdge(pivots, pivots_dis_i, pivots_dis_j, maxdis, mindis):
    pivot_ij = float('inf')
    pivot_ji = float('inf')
    for p in pivots:
        temp_ij = pivots_dis_i[p] + pivots_dis_j['-'+str(p)]
        temp_ji = pivots_dis_j[p] + pivots_dis_i['-'+str(p)]
        if temp_ij < pivot_ij:
            pivot_ij = temp_ij
        if temp_ji < pivot_ji:
            pivot_ji = temp_ji
    if pivot_ij > pivot_ji:
        cmp = 0
    elif pivot_ij == pivot_ji:
        cmp = 1
    else:
        cmp = 2
    if pivot_ij < mindis:
        state, dis = 0, pivot_ij
    elif pivot_ij < maxdis:
        '''
        if pivot_ij > pivot_ji:
            cmp = 0
            state, dis = 1, pivot_ij
        elif pivot_ij == pivot_ji:
            cmp = 1
            state, dis = 1, pivot_ij
        else:
            cmp = 2
            state, dis = 2, mindis
        '''
        state, dis = 2, pivot_ij
    else:
        '''
        if pivot_ij > pivot_ji:
            cmp = 0
            state, dis = 3, maxdis
        elif pivot_ij == pivot_ji:
            cmp = 1
            state, dis = 2, maxdis
        else:
            cmp = 2
            state, dis = 4, maxdis
        '''
        state, dis = 4, maxdis
    return state, cmp, dis

def dinrmsd(G, embedding_comb, embedding_diff, dis_store, S, alg = 'L1'):
    if S<=1:
        print("S should bigger than 1")
        exit
    subset = sample(list(G.nodes()), S)
    sigma = 0
    ave_d = 0
    cnt_bigger = [0,0,0,0,0]
    cnt_even = [0,0,0,0,0]
    cnt_smaller = [0,0,0,0,0]
    p_bigger = [0,0,0]
    p_even = [0,0,0]
    p_smaller = [0,0,0]
    span = S/50
    for i in range(S):
        if i%span == 0:
            print(i/span)
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
            maxdis = embdis_comb + embdis_diff
            mindis = embdis_comb - embdis_diff
            cmp_res, cmp_p, embdis = compare_DiEdge(dis_store['pivots'], dis_store[node_1], dis_store[node_2], maxdis, mindis)
            if distance > distance_reverse:
                cnt_bigger[cmp_res] += 1
                p_bigger[cmp_p] += 1
            elif distance == distance_reverse:
                cnt_even[cmp_res] += 1
                p_even[cmp_p] += 1
            else:
                cnt_smaller[cmp_res] += 1
                p_smaller[cmp_p] += 1
            #if cmp_p <1:
            #    embdis = maxdis
            #else:
            #    embdis = mindis
            sigma += (distance-embdis)*(distance-embdis)
            ave_d += distance
    base = S*S
    sigma = math.sqrt(float(sigma)/base)
    ave_d = float(ave_d)/base
    print("######### Compare matrix:")
    print(cnt_bigger)
    print(cnt_even)
    print(cnt_smaller)
    print("######### Pivot Compare matrix:")
    print(p_bigger)
    print(p_even)
    print(p_smaller)
    return float(sigma)/ave_d
