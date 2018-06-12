import networkx as nx
import numpy as np
import math
from random import sample
import sys
import multiprocessing as mp

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

def dinrmsd(G, embedding_aver, embedding_diff, dis_store, S, alg = 'L1'):
    if S<=1:
        print("S should bigger than 1")
        exit
    subset = sample(list(G.nodes()), S)
    real_sigma = 0
    pred_sigma = 0
    tune_sigma = 0
    ave_d = 0
    cnt_right = 0
    span = S/100
    for i in range(S):
        if i%span == 0:
            sys.stdout.write("\rAnalysis Process: {}%".format(i/span))
        node_1 = subset[i]
        embcomb_1 = np.array(embedding_aver[node_1])
        embdiff_1 = np.array(embedding_diff[node_1])
        length = nx.single_source_dijkstra_path_length(G, node_1)
        for j in range(S):
            node_2 = subset[j]
            if node_1 == node_2:
                continue
            embcomb_2 = np.array(embedding_aver[node_2])
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
            cmp_res, cmp_p, tune_embdis = compare_DiEdge(dis_store['pivots'], dis_store[node_1], dis_store[node_2], maxdis, mindis)
            if distance > distance_reverse:
                real_embdis = maxdis
                if cmp_p == 0:
                    cnt_right += 1
            elif distance == distance_reverse:
                real_embdis = embdis_comb
                cnt_right += 1
            else:
                real_embdis = mindis
                if cmp_p == 2:
                    cnt_right += 1
            if cmp_p == 0:
                pred_embdis = maxdis
            elif cmp_p == 1:
                pred_embdis = embdis_comb
            else:
                pred_embdis = mindis
            real_sigma += (distance-real_embdis)*(distance-real_embdis)
            pred_sigma += (distance-pred_embdis)*(distance-pred_embdis)
            tune_sigma += (distance-tune_embdis)*(distance-tune_embdis)
            ave_d += distance
    base = S*(S-1)
    real_sigma = math.sqrt(float(real_sigma)/base)
    pred_sigma = math.sqrt(float(pred_sigma)/base)
    tune_sigma = math.sqrt(float(tune_sigma)/base)
    ave_d = float(ave_d)/base
    precision = float(cnt_right)/base
    distorsion_real = float(real_sigma)/ave_d
    distorsion_pred = float(pred_sigma)/ave_d
    distorsion_tune = float(tune_sigma)/ave_d
    return precision, distorsion_real, distorsion_pred, distorsion_tune

def meta_calculation(node_1):
    global G, embedding_aver, embedding_diff, dis_store, alg, subset
    embcomb_1 = np.array(embedding_aver[node_1])
    embdiff_1 = np.array(embedding_diff[node_1])
    length = nx.single_source_dijkstra_path_length(G, node_1)
    cnt_right = 0
    real_sigma = 0
    pred_sigma = 0
    tune_sigma = 0
    ave_d = 0
    for j in range(S):
        node_2 = subset[j]
        if node_1 == node_2:
            continue
        embcomb_2 = np.array(embedding_aver[node_2])
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
        cmp_res, cmp_p, tune_embdis = compare_DiEdge(dis_store['pivots'], dis_store[node_1], dis_store[node_2], maxdis, mindis)
        if distance > distance_reverse:
            real_embdis = maxdis
            if cmp_p == 0:
                cnt_right += 1
        elif distance == distance_reverse:
            real_embdis = embdis_comb
            cnt_right += 1
        else:
            real_embdis = mindis
            if cmp_p == 2:
                cnt_right += 1
        if cmp_p == 0:
            pred_embdis = maxdis
        elif cmp_p == 1:
            pred_embdis = embdis_comb
        else:
            pred_embdis = mindis
        real_sigma += (distance-real_embdis)*(distance-real_embdis)
        pred_sigma += (distance-pred_embdis)*(distance-pred_embdis)
        tune_sigma += (distance-tune_embdis)*(distance-tune_embdis)
        ave_d += distance
    return [real_sigma, pred_sigma, tune_sigma, ave_d, cnt_right]

def dinrmsd_mp(G, embedding_aver, embedding_diff, dis_store, subset, alg = 'L1'):
    input_set = list(subset)
    real_sigma = 0
    pred_sigma = 0
    tune_sigma = 0
    ave_d = 0
    cnt_right = 0
    pool_size = mp.cpu_count() * 2
    print("Pool size: {}".format(pool_size))
    pool = mp.Pool(processes=pool_size)
    pool_outputs = pool.map(meta_calculation, input_set)
    pool.close()
    pool.join()
    # Sum the result of metacalculation
    pool_outputs = np.array(pool_outputs)
    real_sigma, pred_sigma, tune_sigma, ave_d, cnt_right = np.sum(pool_outputs, 0)
    base = S*(S-1)
    real_sigma = math.sqrt(float(real_sigma)/base)
    pred_sigma = math.sqrt(float(pred_sigma)/base)
    tune_sigma = math.sqrt(float(tune_sigma)/base)
    ave_d = float(ave_d)/base
    precision = float(cnt_right)/base
    distorsion_real = float(real_sigma)/ave_d
    distorsion_pred = float(pred_sigma)/ave_d
    distorsion_tune = float(tune_sigma)/ave_d
    return precision, distorsion_real, distorsion_pred, distorsion_tune

def distortion(G, embedding, S, alg='L1', variant='undirected'):
    if S<=1:
        print("S should bigger than 1")
        exit
    subset = sample(list(G.nodes()), S)
    sigma = 0
    ave_d = 0
    span = S/100
    for i in range(S):
        if i%span == 0:
            sys.stdout.write("\rAnalysis Process: {}%".format(i/span))
        node_1 = subset[i]
        emb_1 = np.array(embedding[node_1])
        length = nx.single_source_dijkstra_path_length(G, node_1)
        for j in range(i+1, S):
            node_2 = subset[j]
            emb_2 = np.array(embedding[node_2])
            distance = length[node_2]
            if variant == 'undirected':
                target_dis = distance
            elif variant == 'average':
                distance_reverse = nx.dijkstra_path_length(G, node_2, node_1)
                target_dis = (float(distance) + float(distance_reverse))/2
            elif variant == 'max':
                distance_reverse = nx.dijkstra_path_length(G, node_2, node_1)
                target_dis = max(float(distance), float(distance_reverse))
            elif variant == 'diff':
                distance_reverse = nx.dijkstra_path_length(G, node_2, node_1)
                target_dis = abs(float(distance) - float(distance_reverse))/2
            if alg == 'L1':
                embdis = np.sum(np.abs(emb_1-emb_2))
            elif alg == 'L2':
                embdis = math.sqrt(np.dot(emb_1-emb_2, emb_1-emb_2))
            sigma += (target_dis-embdis)*(target_dis-embdis)
            ave_d += target_dis
    base = float(S)*float(S-1)/2
    sigma = math.sqrt(float(sigma)/base)
    ave_d = float(ave_d)/base
    return float(sigma)/ave_d
