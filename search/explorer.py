import os, sys
lib_path = os.path.abspath(os.path.join('../'))
sys.path.append(lib_path)

from search.dijkstra import dijkstra
from search.astar import astar

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
