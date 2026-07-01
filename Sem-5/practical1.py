import time
from collections import deque

# Map: Jankalyan Nagar (Malad West) -> MVLU College (Andheri East)
ANDHERI_MAP = {
    'Jankalyan Nagar': ['Liberty Garden Malad'],
    'Liberty Garden Malad': ['Western Express Highway'],
    'Western Express Highway': ['Andheri Subway Road', 'Marol Maroshi Road'],
    'Andheri Subway Road': ['Sahar Road Junction'],
    'Marol Maroshi Road': ['Andheri-Kurla Road', 'Marol Naka', 'Chakala Junction'],
    'Marol Naka': ['Marol Church Road'],
    'Marol Church Road': ['Andheri Airport Road'],
    'Andheri Airport Road': ['Sahar Road Junction'],
    'Chakala Junction': ['J B Nagar Road'],
    'J B Nagar Road': ['Sahar Road Junction'],
    'Andheri-Kurla Road': ['Sakinaka Junction'],
    'Sakinaka Junction': ['Sahar Road Junction'],
    'Sahar Road Junction': ['Andheri Station East'],
    'Andheri Station East': ['A S Marg'],
    'A S Marg': ['Azad Nagar'],
    'Azad Nagar': ['MVLU College'],
    'MVLU College': [],
}


def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = {start}
    explored = 0

    while queue:
        node, path = queue.popleft()
        explored += 1
        if node == goal:
            return path, explored
        for nxt in graph.get(node, []):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))

    return None, explored


def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    explored = 0

    while stack:
        node, path = stack.pop()
        explored += 1
        if node == goal:
            return path, explored
        if node not in visited:
            visited.add(node)
            for nxt in reversed(graph.get(node, [])):
                if nxt not in visited:
                    stack.append((nxt, path + [nxt]))

    return None, explored


def run(fn, graph, start, goal):
    t0 = time.perf_counter()
    path, explored = fn(graph, start, goal)
    elapsed = time.perf_counter() - t0
    return path, explored, elapsed


def show(label, path, explored, elapsed):
    print(f"--- {label} ---")
    if path:
        print(f"Path: {' -> '.join(path)}")
        print(f"Steps: {len(path) - 1}")
    else:
        print("No path found.")
    print(f"Nodes explored: {explored}")
    print(f"Time: {elapsed:.8f}s\n")


def compare(bfs_path, bfs_explored, bfs_time, dfs_path, dfs_explored, dfs_time):
    bfs_len = len(bfs_path) - 1 if bfs_path else None
    dfs_len = len(dfs_path) - 1 if dfs_path else None

    if bfs_len is None or dfs_len is None:
        shorter = "BFS" if dfs_len is None and bfs_len is not None else \
                  "DFS" if bfs_len is None and dfs_len is not None else "Neither"
    else:
        shorter = "BFS" if bfs_len < dfs_len else "DFS" if dfs_len < bfs_len else "Tie"

    faster = "BFS" if bfs_time < dfs_time else "DFS" if dfs_time < bfs_time else "Tie"
    fewer = "BFS" if bfs_explored < dfs_explored else "DFS" if dfs_explored < bfs_explored else "Tie"

    print("=" * 50)
    print("SEARCH ALGORITHM COMPARISON")
    print("=" * 50)
    print(f"Shorter path : {shorter}")
    print(f"Fewer nodes  : {fewer}")
    print(f"Faster       : {faster}")
    print("=" * 50)
    print("Note: BFS guarantees the shortest path on unweighted graphs.")
    print("DFS may explore fewer/more nodes but isn't guaranteed shortest.")
    print("=" * 50)


def main():
    start, goal = 'Jankalyan Nagar', 'MVLU College'

    bfs_path, bfs_explored, bfs_time = run(bfs, ANDHERI_MAP, start, goal)
    dfs_path, dfs_explored, dfs_time = run(dfs, ANDHERI_MAP, start, goal)

    show("BFS", bfs_path, bfs_explored, bfs_time)
    show("DFS", dfs_path, dfs_explored, dfs_time)
    compare(bfs_path, bfs_explored, bfs_time, dfs_path, dfs_explored, dfs_time)


if __name__ == "__main__":
    main()