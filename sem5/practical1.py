from collections import deque

# Route starts from Jankalyan Nagar, Malad West -> MVLU College, Andheri East
andheri_map = {
    # Jankalyan Nagar (Malad West) connecting toward Andheri via WEH
    'Jankalyan Nagar': ['Liberty Garden Malad'],
    'Liberty Garden Malad': ['Western Express Highway'],
    'Western Express Highway': ['Andheri Subway Road', 'Marol Maroshi Road'],

    # Branch A - via Andheri Subway (shorter, direct to convergence point)
    'Andheri Subway Road': ['Sahar Road Junction'],

    # Branch B - via Marol (Seven Hills removed, Marol Maroshi Road connects directly onward)
    'Marol Maroshi Road': ['Andheri-Kurla Road', 'Marol Naka', 'Chakala Junction'],

    # Route 1 (via Marol / Airport Road)
    'Marol Naka': ['Marol Church Road'],
    'Marol Church Road': ['Andheri Airport Road'],
    'Andheri Airport Road': ['Sahar Road Junction'],

    # Route 2 (via Andheri-Kurla Road / Chakala)
    'Chakala Junction': ['J B Nagar Road'],
    'J B Nagar Road': ['Sahar Road Junction'],

    # Route 3 (via Andheri-Kurla Road直 to Station)
    'Andheri-Kurla Road': ['Sakinaka Junction'],
    'Sakinaka Junction': ['Sahar Road Junction'],

    # Converging route toward Azad Nagar / MVLU
    'Sahar Road Junction': ['Andheri Station East'],
    'Andheri Station East': ['A S Marg'],
    'A S Marg': ['Azad Nagar'],

    # Destination
    'Azad Nagar': ['MVLU College'],
    'MVLU College': []
}

# ==========================================
# A) Breadth First Search (BFS) Implementation
# ==========================================
def bfs_shortest_path(graph, start, destination):
    queue = deque([(start, [start])])
    visited = set([start])
    nodes_explored_count = 0

    while queue:
        current, path = queue.popleft()
        nodes_explored_count += 1

        if current == destination:
            return path, nodes_explored_count

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None, nodes_explored_count

# ==========================================
# B) Iterative Depth First Search (DFS) Implementation
# ==========================================
def iterative_dfs_path(graph, start, destination):
    stack = [(start, [start])]
    visited = set()
    nodes_explored_count = 0

    while stack:
        current, path = stack.pop()
        nodes_explored_count += 1

        if current == destination:
            return path, nodes_explored_count

        if current not in visited:
            visited.add(current)
            for neighbor in reversed(graph.get(current, [])):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return None, nodes_explored_count

# ==========================================
# C) Performance Comparison
# ==========================================
import time

start_node = 'Jankalyan Nagar'
end_node = 'MVLU College'

t0 = time.perf_counter()
bfs_path, bfs_count = bfs_shortest_path(andheri_map, start_node, end_node)
t1 = time.perf_counter()

t2 = time.perf_counter()
dfs_path, dfs_count = iterative_dfs_path(andheri_map, start_node, end_node)
t3 = time.perf_counter()

print("--- BFS Results ---")
print(f"Path Found: {' -> '.join(bfs_path)}")
print(f"Total Steps (Edges): {len(bfs_path) - 1}")
print(f"Total Nodes Visited/Checked: {bfs_count}")
print(f"Time Taken: {t1 - t0:.8f}s\n")

print("--- Iterative DFS Results ---")
print(f"Path Found: {' -> '.join(dfs_path)}")
print(f"Total Steps (Edges): {len(dfs_path) - 1}")
print(f"Total Nodes Visited/Checked: {dfs_count}")
print(f"Time Taken: {t3 - t2:.8f}s")