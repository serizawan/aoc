from copy import deepcopy
import math
import sys


def get_neighbors(i, j, h, w) -> [tuple[int]]:
    neighbors = []
    for u, v in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        if (0 <= i + u < h) and (0 <= j + v < w):
            neighbors.append((i + u, j + v))
    return neighbors


def expand(matrix):
    expand_factor = 5
    expanded_matrix_x = []
    for line in matrix:
        expanded_line = line[:]
        for j in range(1, expand_factor):
            expanded_line += [v + j if v + j <= 9 else (v + j) % 9 for v in line]
        expanded_matrix_x.append(expanded_line)

    expanded_matrix = deepcopy(expanded_matrix_x)
    for i in range(1, expand_factor):
        inc_expanded_matrix_x = []
        for expanded_line_x in expanded_matrix_x:
            inc_expanded_line_x = [v + i if v + i <= 9 else (v + i) % 9 for v in expanded_line_x]
            inc_expanded_matrix_x.append(inc_expanded_line_x)
        expanded_matrix += inc_expanded_matrix_x

    return expanded_matrix


def parse(filename) -> (list[str], dict[dict]):
    with open(filename) as f:
        lines = f.read().splitlines()

    matrix = []
    for line in lines:
        matrix_line = [int(i) for i in line]
        matrix.append(matrix_line)

    matrix = expand(matrix)

    h, w = len(matrix), len(matrix[0])
    nodes = []
    distances = {}
    for i in range(h):
        for j in range(w):
            nodes.append(f"id_{i}_{j}")
            neighbors = get_neighbors(i, j, h, w)
            distances[f"id_{i}_{j}"] = {f"id_{n[0]}_{n[1]}": matrix[n[0]][n[1]] for n in neighbors}
    return h, w, nodes, distances


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr);
        sys.exit()

    h, w, nodes, distances = parse(sys.argv[1])

    unvisited = {node: math.inf for node in nodes}
    visited = {}
    c = "id_0_0"
    c_dist = 0
    unvisited[c] = c_dist

    # Simple Djikstra implementation
    # This version is not optimized (using heapq would improve significantly performances)
    while unvisited:
        print(len(unvisited))
        for neighbour, distance in distances[c].items():
            n_dist = c_dist + distance
            if neighbour not in visited and n_dist < unvisited[neighbour]:
                unvisited[neighbour] = n_dist
        visited[c] = c_dist
        unvisited.pop(c)
        candidates = [(node, dist) for node, dist in unvisited.items() if dist]
        c, c_dist = min(candidates, key=lambda x: x[1]) if candidates else (None, None)

    print(visited[f"id_{h - 1}_{w - 1}"])


if __name__ == "__main__":
    run()
