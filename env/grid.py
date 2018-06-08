import networkx as nx
import sys
import math

class GCCPGrid(object):

    TerrainPassable = ['.', 'G', 'S']
    TerrainUnpassable = ['@', 'O', 'T', 'W']

    def __init__(self, filename):
        self.graph = nx.Graph()
        with open(filename) as f:
            while True:
                line = f.readline()
                li = line.strip().split()
                if li[0] == 'type':
                    self.type = li[1]
                elif li[0] == 'height':
                    self.height = int(li[1])
                elif li[0] == 'width':
                    self.width = int(li[1])
                elif li[0] == 'map':
                    break
            for i in range(self.height):
                line = f.readline()
                for j in range(self.width):
                    terrain = line[j]
                    nodeid = (i,j)
                    self.graph.add_node(nodeid, terrain=terrain)
        # Add edges
        for i in range(self.height):
            for j in range(self.width):
                nodeid = (i, j)
                if not self.passable(nodeid):
                    continue
                l1 = [(i, j+1), (i+1, j)]
                l2 = [(i-1, j+1), (i+1, j+1)]
                for next_nodeid in l1:
                    if self.passable(next_nodeid):
                        self.graph.add_edge(nodeid, next_nodeid, weight=1)
                for next_nodeid in l2:
                    if self.passable(next_nodeid):
                        self.graph.add_edge(nodeid, next_nodeid, weight=math.sqrt(2))

    def passable(self, nodeid):
        if nodeid not in self.graph.nodes:
            return False
        if self.graph.nodes[nodeid]['terrain'] in GCCPGrid.TerrainPassable:
            return True
        return False

    def get_size(self):
        return self.height, self.width

    def printGrid(self):
        for i in range(self.height):
            sys.stdout.write('\n')
            for j in range(self.width):
                nodeid = (i,j)
                sys.stdout.write(self.graph.nodes[nodeid]['terrain'])

    def get_networkx_graph(self):
        return self.graph

if __name__ == "__main__":
    filename = "../data/grid/arena.map"
    G = GCCPGrid(filename)
    G.printGrid()
