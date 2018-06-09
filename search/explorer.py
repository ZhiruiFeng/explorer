import os, sys
lib_path = os.path.abspath(os.path.join('../'))
sys.path.append(lib_path)

from search.dijkstra import dijkstra
from search.astar import astar
from heuristic.fastmap.fastmap import fastmap_L1

class Explorer:
    def __init__(self, graph):
        self.graph = graph
        self.graph.reset()

    def plan_dijkstra(self, start, goal):
        self.graph.reset()
        path, cost = dijkstra(self.graph, start, goal)
        number_of_visited = self.graph.number_of_labeled()
        number_of_expanded = self.graph.number_of_scanned()
        if len(path) == 0:
            print("There is no path exist")
            self.graph.mark_start_goal(start, goal)
        self.graph.mark_path(path)
        return path, cost, number_of_visited, number_of_expanded

    def plan_astar(self, start, goal, heuristic):
        self.graph.reset()
        if heuristic == 'FastMap_L1':
            self.graph.setembedding(self.embedding_fastmap_L1)
        path, cost = astar(self.graph, start, goal, heuristic)
        number_of_visited = self.graph.number_of_labeled()
        number_of_expanded = self.graph.number_of_scanned()
        if len(path) == 0:
            print("There is no path exist")
            self.graph.mark_start_goal(start, goal)
        self.graph.mark_path(path)
        return path, cost, number_of_visited, number_of_expanded

    def print_exploration(self):
        self.graph.print_exploration()

    def preprocessing_fastmap_L1(self, K, epsilon):
        tempgraph = self.graph.get_networkx_graph().copy
        nodelist = list(tempgraph.node)
        for node in nodelist:
            if tempgraph.degree[node] == 0:
                tempgraph.remove_node(node)

        self.embedding_fastmap_L1 = fastmap_L1(tempgraph, K, epsilon)
