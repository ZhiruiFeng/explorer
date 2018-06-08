def reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return []
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path
