import math


def neighs(l, c):
    vs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    _neighs = []
    for v in vs:
        if memory_map[l][c] == "." and 0 <= l + v[0] < L and 0 <= c + v[1] < C and memory_map[l + v[0]][c + v[1]] == "." :
            _neighs.append(((l + v[0], c + v[1]), 1))
    return _neighs


def compute_dijkstra_shortest_paths_naive(graph, start_node):
    visited = {}
    unvisited = {node: math.inf for node in graph.keys()}
    unvisited[start_node] = 0
    current_distance = 0
    node = start_node
    while unvisited and node:
        for neighbour, distance in graph[node]:
            node_distance = current_distance + distance
            if neighbour not in visited and node_distance < unvisited[neighbour]:
                unvisited[neighbour] = node_distance
        visited[node] = current_distance
        unvisited.pop(node)
        candidates = [(n, d) for n, d in unvisited.items() if d != math.inf]
        node, current_distance = min(candidates, key=lambda x: x[1]) if candidates else (None, None)
    return visited


if __name__ == "__main__":
    bytes = open(0).read().splitlines()
    bytes = [tuple(int(i) for i in byte.split(",")[::-1]) for byte in bytes]
    L, C = 71, 71

    n_bytes = len(bytes)
    upper = n_bytes
    lower = 1024
    is_lower_byte_breaking = False
    while upper > lower + 1:
        bytes_read_count = (lower + upper) // 2
        memory_map = [list("." * C) for i in range(L)]
        for byte in bytes[:bytes_read_count]:
            memory_map[byte[0]][byte[1]] = "#"

        graph = dict()
        for l in range(L):
            for c in range(C):
                graph[(l, c)] = neighs(l, c)

        if (L - 1, C - 1) in compute_dijkstra_shortest_paths_naive(graph, (0, 0)):
            lower = bytes_read_count
        else:
            upper = bytes_read_count
            is_lower_byte_breaking = True

    if is_lower_byte_breaking:
        print(bytes[lower][::-1])
    else:
        print(bytes[upper][::-1])


