from collections import defaultdict
import heapq
import math
import sys


DEFAULT_COST = 1


def compute_dijkstra_shortest_paths(graph, start_node):
    visited = defaultdict(lambda: math.inf)
    unvisited = defaultdict(lambda: math.inf)
    unvisited[start_node] = 0
    heap = [(0, start_node)]
    while heap:
        current_distance, node = heapq.heappop(heap)
        if node not in visited:
            for neighbour, distance in graph[node]:
                node_distance = current_distance + distance
                if neighbour not in visited and node_distance < unvisited[neighbour]:
                    unvisited[neighbour] = node_distance
                    heapq.heappush(heap, (node_distance, neighbour))
            visited[node] = current_distance
            unvisited.pop(node)
    return visited


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    h, w = len(lines), len(lines[0])

    start_node = None
    end_node = None
    for i in range(h):
        for j in range(w):
            if lines[i][j] == "S":
                start_node = (i, j)
                lines[i] = lines[i].replace("S", "a")
            elif lines[i][j] == "E":
                end_node = (i, j)
                lines[i] = lines[i].replace("E", "z")
            else:
                continue

    nodes = {(i, j): [] for i in range(h) for j in range(w)}

    for i in range(h):
        for j in range(w):
            if i + 1 < h and (ord(lines[i + 1][j]) - ord(lines[i][j])) <= 1:
                nodes[(i, j)].append(((i + 1, j), DEFAULT_COST))
            if i - 1 >= 0 and (ord(lines[i - 1][j]) - ord(lines[i][j])) <= 1:
                nodes[(i, j)].append(((i - 1, j), DEFAULT_COST))
            if j + 1 < w and (ord(lines[i][j + 1]) - ord(lines[i][j])) <= 1:
                nodes[(i, j)].append(((i, j + 1), DEFAULT_COST))
            if j - 1 >= 0 and (ord(lines[i][j - 1]) - ord(lines[i][j])) <= 1:
                nodes[(i, j)].append(((i, j - 1), DEFAULT_COST))

    print(compute_dijkstra_shortest_paths(nodes, start_node)[end_node])



