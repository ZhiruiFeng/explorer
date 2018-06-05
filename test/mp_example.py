import os, sys
lib_path = os.path.abspath(os.path.join('../heuristic/'))
sys.path.append(lib_path)

import fastmap.utils as utils
from fastmap.difastmap import init_dis_store, difastmap_average, difastmap_diff
import fastmap.analyse as analyse

import matplotlib.pyplot as plt
import networkx as nx
import random
import multiprocessing as mp
from random import sample
import math
import numpy as np

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
        cmp_res, cmp_p, tune_embdis = analyse.compare_DiEdge(dis_store['pivots'], dis_store[node_1], dis_store[node_2], maxdis, mindis)
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


if __name__ == "__main__":
    n = 1000
    p = 0.007
    low = 1
    high = 5
    G, density = utils.generate_random_digraph(n, p, low, high)

    K = 20
    epsilon = 0.01
    alg = 'L2'
    dis_store = init_dis_store(G)
    embedding_aver = difastmap_average(G, K, epsilon, dis_store, alg)
    embedding_diff = difastmap_diff(G, K, epsilon, dis_store, alg)

    S = int(0.2*len(list(G.nodes())))
    subset = sample(list(G.nodes()), S)
    results = dinrmsd_mp(G, embedding_aver, embedding_diff,dis_store, subset, alg)
    print("\nPrecision: "+str(results[0]))
    print("Distortion_real: "+ str(results[1]))
    print("Distortion_pred: "+ str(results[2]))
    print("Distortion_tune: "+ str(results[3]))
