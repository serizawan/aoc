import sys


def get_neighbors(i, j, h, w) -> [tuple[int]]:
    neighbors = []
    for u, v in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        if (0 <= i + u < h) and (0 <= j + v < w):
            neighbors.append((i + u, j + v))
    return neighbors


def parse(filename) -> (list[str], dict[dict]):
    with open(filename) as f:
        lines = f.read().splitlines()

    matrix = []
    for line in lines:
        matrix_line = [int(i) for i in line]
        matrix.append(matrix_line)

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

    unvisited = {node: None for node in nodes}
    visited = {}
    c = "id_0_0"
    c_dist = 0
    unvisited[c] = c_dist

    while True:
        for neighbour, distance in distances[c].items():
            if neighbour not in unvisited:
                continue
            n_dist = c_dist + distance
            if unvisited[neighbour] is None or unvisited[neighbour] > n_dist:
                unvisited[neighbour] = n_dist
        visited[c] = c_dist
        del unvisited[c]
        if not unvisited:
            break
        candidates = [node for node in unvisited.items() if node[1]]
        c, c_dist = sorted(candidates, key=lambda x: x[1])[0]

    print(visited[f"id_{h - 1}_{w - 1}"])


if __name__ == "__main__":
    run()
