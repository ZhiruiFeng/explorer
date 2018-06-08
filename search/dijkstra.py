import os, sys
lib_path = os.path.abspath(os.path.join('../'))
sys.path.append(lib_path)
from search.myqueue import PriorityQueue
from search.tools import reconstruct_path

def dijkstra(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    graph.set_labeled(start)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break
        for next_node in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.get_weight(current, next_node)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost
                frontier.put(next_node, priority)
                came_from[next_node] = current
                graph.set_labeled(next_node)
        graph.set_scanned(current)
    if current != goal:
        return [], float("INF")
    path = reconstruct_path(came_from, start, goal)
    return path, cost_so_far[goal]
