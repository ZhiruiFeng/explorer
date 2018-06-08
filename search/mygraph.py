import os, sys
lib_path = os.path.abspath(os.path.join('../'))
sys.path.append(lib_path)

import networkx as nx
from heuristic.fastmap import difastmap
import math

class SimpleGraph:
    def __init__(self, G):
        self.graph = G
        self.scanned_cnt = 0
        self.labeled_cnt = 0
        # initial the state of every nodes as 'unreached'
        self.reset()

    def neighbors(self, nodeid):
        return list(self.graph.adj[nodeid])

    def get_state(self, nodeid):
        return self.graph.nodes[nodeid]['state']

    def set_unreached(self, nodeid):
        self.graph.nodes[nodeid]['state'] = 'unreached'

    def set_labeled(self, nodeid):
        self.labeled_cnt += 1
        self.graph.nodes[nodeid]['state'] = 'labeled'

    def set_scanned(self, nodeid):
        self.scanned_cnt += 1
        self.graph.nodes[nodeid]['state'] = 'scanned'

    def get_weight(self, node1, node2):
        return self.graph.edges[(node1,node2)]['weight']

    def reset(self):
        self.scanned_cnt = 0
        self.labeled_cnt = 0
        for i in self.graph.nodes():
            self.graph.nodes[i]['state'] = 'unreached'

    def number_of_scanned(self):
        return self.scanned_cnt

    def number_of_labeled(self):
        return self.labeled_cnt

    def get_networkx_graph(self):
        return self.graph

    def mark_path(self, path):
        start = path[0]
        self.graph.nodes[start]['state'] = 'start'
        goal = path[-1]
        self.graph.nodes[goal]['state'] = 'goal'
        for nodeid in path[1:-1]:
            self.graph.nodes[nodeid]['state'] = 'path'

class GridGraph(SimpleGraph):
    def __init__(self, Grid):
        # input G is the grid type in env.grid
        self.PassableTerrain = Grid.TerrainPassable
        self.graph = Grid.get_networkx_graph()
        self.height, self.width = Grid.get_size()
        self.reset()

    def is_legal_goal(self, start, goal):
        if not start in self.graph.nodes:
            print("start point out of range")
            return False
        if not goal in self.graph.nodes:
            print("goal point out of range")
            return False
        if not self.graph.nodes[start]['terrain'] in self.PassableTerrain:
            print("start point unpassable")
            return False
        if not self.graph.nodes[goal]['terrain'] in self.PassableTerrain:
            print("goal point unpassable")
            return False
        if start == goal:
            print("start and goal at the same place")
        return True

    def get_heuristic(self, node1, node2, alg='Manhattan'):
        i1, j1 = node1
        i2, j2 = node2
        if alg == 'Manhattan':
            heuristic = abs(i1-i2)+abs(j1-j2)
        elif alg == 'Straight':
            heuristic = math.sqrt((i1-i2)**2 + (j1-j2)**2)

        return heuristic

    def print_terrain(self):
        for i in range(self.height):
            sys.stdout.write('\n')
            for j in range(self.width):
                nodeid = (i,j)
                sys.stdout.write(self.graph.nodes[nodeid]['terrain'])

    def print_exploration(self, path):
        for i in range(self.height):
            sys.stdout.write('\n')
            for j in range(self.width):
                nodeid = (i,j)
                if self.get_state(nodeid) == 'unreached':
                    sys.stdout.write(self.graph.nodes[nodeid]['terrain'])
                elif self.get_state(nodeid) == 'start':
                    sys.stdout.write('?')
                elif self.get_state(nodeid) == 'goal':
                    sys.stdout.write('$')
                elif self.get_state(nodeid) == 'path':
                    sys.stdout.write('+')
                else:
                    sys.stdout.write('~')

class DirectedGraph(SimpleGraph):
    def get_heuristic(self, node1, node2):
        # TODO
        pass

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
        pass
