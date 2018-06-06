import os, sys
lib_path = os.path.abspath(os.path.join('../'))
sys.path.append(lib_path)

import networkx as nx
from heuristic.fastmap import difastmap

class SimpleGraph:
    def __init__(self, G):
        self.graph = G
        # initial the state of every nodes as 'unreached'
        for i in self.graph.nodes():
            self.graph[i]['state'] = 'unreached'

    def neighbors(self, id):
        return list(self.graph.adj[id])

    def get_state(self, id):
        return self.graph[i]['state']

    def set_unreached(self, id):
        self.graph[id]['state'] = 'unreached'

    def set_labeled(self, id):
        self.graph[id]['state'] = 'labeled'

    def set_scanned(self, id):
        self.graph[id]['state'] = 'scanned'

    def get_weight(self, node1, node2):
        return self.graph[node1][node2]['weight']

class DirectedGraph(SimpleGraph):
    def get_heuristic(self, node1, node2):
        # TODO


class FastMapDiGraph(DirectedGraph):
    def __init__(self, G, K, epsilon, alg='L2'):
        DirectedGraph.__init__(self, G)
        self.K = K
        self.epsilon = epsilon
        self.alg = alg
        self.dis_store = difastmap.init_dis_store(self.graph)
        self.embedding_aver = difastmap.difastmap_average(G, self.K, self.epsilon, self.dis_store, self.alg)
        self.embedding_diff = difastmap.difastmap_diff(G, self.K, self.epsilon, self.dis_store, self.alg)

    def get_heuristic(self, node1, node2):
        # TODO
