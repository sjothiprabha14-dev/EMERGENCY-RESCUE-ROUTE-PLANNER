"""
Emergency Rescue Route Planner
--------------------------------
An intelligent agent (rescue robot) that finds a path from the
Entrance (A) to the Patient location (L) in a hospital/city graph
using three different search strategies:

1. Breadth-First Search (BFS)          -> shortest path by number of hops
2. Uniform Cost Search (UCS)           -> minimum cost path (weighted edges)
3. Iterative Deepening Search (IDS)    -> DFS with increasing depth limits
"""

from collections import deque
import heapq

# ---------------------------------------------------------
# 1. ENVIRONMENT DEFINITION
# ---------------------------------------------------------

# Unweighted graph (used for BFS and IDS)
graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": ["H"],
    "E": ["H"],
    "F": ["I"],
    "G": ["J"],
    "H": ["K"],
    "I": ["K"],
    "J": ["K"],
    "K": ["L"],
    "L": []
}

# Weighted version of the same graph (used for UCS).
# Costs could represent distance, time, or difficulty of travel.
weighted_graph = {
    "A": [("B", 2), ("C", 1)],
    "B": [("D", 2), ("E", 4)],
    "C": [("F", 3), ("G", 2)],
    "D": [("H", 2)],
    "E": [("H", 1)],
    "F": [("I", 2)],
    "G": [("J", 2)],
    "H": [("K", 3)],
    "I": [("K", 2)],
    "J": [("K", 1)],
    "K": [("L", 2)],
    "L": []
}

START = "A"
GOAL = "L"


# ---------------------------------------------------------
# 2. BREADTH-FIRST SEARCH (BFS)
# ---------------------------------------------------------
def bfs(graph, start, goal):
    """Finds the path with the fewest hops from start to goal."""
    visited = {start}
    queue = deque([[start]])  # queue of paths

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None  # no path found


# ---------------------------------------------------------
# 3. UNIFORM COST SEARCH (UCS)
# ---------------------------------------------------------
def ucs(weighted_graph, start, goal):
    """Finds the minimum-cost path from start to goal using a priority queue."""
    # Each entry: (cumulative_cost, path_list)
    frontier = [(0, [start])]
    visited_cost = {}  # best known cost to reach a node

    while frontier:
        cost, path = heapq.heappop(frontier)
        node = path[-1]

        if node == goal:
            return path, cost

        if node in visited_cost and visited_cost[node] <= cost:
            continue
        visited_cost[node] = cost

        for neighbor, edge_cost in weighted_graph.get(node, []):
            new_cost = cost + edge_cost
            if neighbor not in visited_cost or new_cost < visited_cost[neighbor]:
                heapq.heappush(frontier, (new_cost, path + [neighbor]))

    return None, float("inf")  # no path found


# ---------------------------------------------------------
# 4. ITERATIVE DEEPENING SEARCH (IDS)
# ---------------------------------------------------------
def depth_limited_search(graph, node, goal, limit, path):
    """DFS restricted to a maximum depth (limit)."""
    if node == goal:
        return path

    if limit <= 0:
        return None

    for neighbor in graph.get(node, []):
        if neighbor not in path:  # avoid cycles
            result = depth_limited_search(graph, neighbor, goal, limit - 1, path + [neighbor])
            if result is not None:
                return result

    return None


def ids(graph, start, goal, max_depth=20):
    """Repeats depth-limited search with increasing depth limits."""
    for depth in range(max_depth + 1):
        result = depth_limited_search(graph, start, goal, depth, [start])
        if result is not None:
            return result, depth
    return None, -1  # no path found within max_depth


# ---------------------------------------------------------
# 5. RUN AND DISPLAY RESULTS
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=" * 55)
    print(" EMERGENCY RESCUE ROUTE PLANNER")
    print(f" Start: {START}  ->  Target (Patient): {GOAL}")
    print("=" * 55)

    # --- BFS ---
    bfs_path = bfs(graph, START, GOAL)
    print("\n[1] Breadth-First Search (BFS)")
    print("    Path :", " -> ".join(bfs_path) if bfs_path else "No path found")
    print("    Hops :", len(bfs_path) - 1 if bfs_path else "-")

    # --- UCS ---
    ucs_path, ucs_cost = ucs(weighted_graph, START, GOAL)
    print("\n[2] Uniform Cost Search (UCS)")
    print("    Path :", " -> ".join(ucs_path) if ucs_path else "No path found")
    print("    Cost :", ucs_cost)

    # --- IDS ---
    ids_path, ids_depth = ids(graph, START, GOAL)
    print("\n[3] Iterative Deepening Search (IDS)")
    print("    Path  :", " -> ".join(ids_path) if ids_path else "No path found")
    print("    Depth :", ids_depth)

    print("\n" + "=" * 55)