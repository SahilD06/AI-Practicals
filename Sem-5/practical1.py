from collections import deque
import time


class RouteGraph:
    """Encapsulates the map and both search algorithms."""

    def __init__(self, adjacency):
        self.graph = adjacency

    def neighbors(self, node):
        return self.graph.get(node, [])

    def bfs(self, start, destination):
        queue = deque([(start, [start])])
        visited = {start}
        explored = 0

        while queue:
            current, path = queue.popleft()
            explored += 1

            if current == destination:
                return path, explored

            for neighbor in self.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None, explored

    def dfs(self, start, destination):
        stack = [(start, [start])]
        visited = set()
        explored = 0

        while stack:
            current, path = stack.pop()
            explored += 1

            if current == destination:
                return path, explored

            if current not in visited:
                visited.add(current)
                for neighbor in reversed(self.neighbors(current)):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))

        return None, explored


class RouteReport:
    """Formats and prints results for a single search run."""

    def __init__(self, label, path, explored, elapsed):
        self.label = label
        self.path = path
        self.explored = explored
        self.elapsed = elapsed

    def display(self):
        print(f"--- {self.label} Results ---")
        if self.path:
            print(f"Path Found: {' -> '.join(self.path)}")
            print(f"Total Steps (Edges): {len(self.path) - 1}")
        else:
            print("No path found.")
        print(f"Total Nodes Visited/Checked: {self.explored}")
        print(f"Time Taken: {self.elapsed:.8f}s\n")


class RouteComparison:
    """Compares BFS and DFS results side by side."""

    def __init__(self, bfs_report, dfs_report):
        self.bfs = bfs_report
        self.dfs = dfs_report

    def _shorter_path_label(self):
        bfs_len = len(self.bfs.path) - 1 if self.bfs.path else None
        dfs_len = len(self.dfs.path) - 1 if self.dfs.path else None

        if bfs_len is None and dfs_len is None:
            return "Neither found a path"
        if bfs_len is None:
            return "DFS (BFS found no path)"
        if dfs_len is None:
            return "BFS (DFS found no path)"
        if bfs_len < dfs_len:
            return "BFS"
        if dfs_len < bfs_len:
            return "DFS"
        return "Tie"

    def _faster_label(self):
        if self.bfs.elapsed < self.dfs.elapsed:
            return "BFS"
        if self.dfs.elapsed < self.bfs.elapsed:
            return "DFS"
        return "Tie"

    def _fewer_explored_label(self):
        if self.bfs.explored < self.dfs.explored:
            return "BFS"
        if self.dfs.explored < self.bfs.explored:
            return "DFS"
        return "Tie"

    def display(self):
        bfs_len = len(self.bfs.path) - 1 if self.bfs.path else "N/A"
        dfs_len = len(self.dfs.path) - 1 if self.dfs.path else "N/A"

        print("=" * 50)
        print("        SEARCH ALGORITHM COMPARISON")
        print("=" * 50)
        print(f"{'Metric':<28}{'BFS':<12}{'DFS':<12}")
        print("-" * 50)
        print(f"{'Path Length (edges)':<28}{str(bfs_len):<12}{str(dfs_len):<12}")
        print(f"{'Nodes Explored':<28}{self.bfs.explored:<12}{self.dfs.explored:<12}")
        print(f"{'Time Taken (s)':<28}{self.bfs.elapsed:<12.8f}{self.dfs.elapsed:<12.8f}")
        print("-" * 50)
        print(f"Shorter path found by  : {self._shorter_path_label()}")
        print(f"Fewer nodes explored by: {self._fewer_explored_label()}")
        print(f"Faster runtime         : {self._faster_label()}")
        print(f"Nodes explored diff    : {abs(self.bfs.explored - self.dfs.explored)} "
              f"(BFS - DFS = {self.bfs.explored - self.dfs.explored})")
        print(f"Time diff              : {abs(self.bfs.elapsed - self.dfs.elapsed):.8f}s")
        print("=" * 50)
        print("Note: BFS guarantees the shortest path (fewest edges) on")
        print("unweighted graphs. DFS may find *a* path faster or with")
        print("fewer/more nodes explored, but it is not guaranteed to be")
        print("the shortest one.")
        print("=" * 50 + "\n")


def timed_run(fn, *args):
    start_time = time.perf_counter()
    result, count = fn(*args)
    elapsed = time.perf_counter() - start_time
    return result, count, elapsed


# ==========================================
# Map data: Jankalyan Nagar (Malad West) -> MVLU College (Andheri East)
# ==========================================
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
    'MVLU College': []
}


def main():
    router = RouteGraph(ANDHERI_MAP)
    start_node, end_node = 'Jankalyan Nagar', 'MVLU College'

    bfs_path, bfs_count, bfs_time = timed_run(router.bfs, start_node, end_node)
    dfs_path, dfs_count, dfs_time = timed_run(router.dfs, start_node, end_node)

    bfs_report = RouteReport("BFS", bfs_path, bfs_count, bfs_time)
    dfs_report = RouteReport("Iterative DFS", dfs_path, dfs_count, dfs_time)

    bfs_report.display()
    dfs_report.display()

    RouteComparison(bfs_report, dfs_report).display()


if __name__ == "__main__":
    main()