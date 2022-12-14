import math
import sys


Y_SOURCE = 500
# Pick enough large for the sand to reach source and not fall apart
T_Y = 80


def simulate(cave, source):
    sand_count = 0
    while True:
        sand = source[:]
        moving = True
        while moving:
            if cave[sand[0] + 1][sand[1]] == ".":
                sand[0] += 1
                continue
            if cave[sand[0] + 1][sand[1] - 1] == ".":
                sand[0] += 1
                sand[1] -= 1
                continue
            if cave[sand[0] + 1][sand[1] + 1] == ".":
                sand[0] += 1
                sand[1] += 1
                continue

            cave[sand[0]][sand[1]] = "o"
            moving = False

        sand_count += 1
        if sand[0] == 0:
            return sand_count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    min_x, max_x = math.inf, 0
    min_y, max_y = math.inf, 0
    paths = []
    for line in lines:
        vertices = [tuple(int(v) for v in vertex.split(",")) for vertex in line.split(" -> ")]
        paths.append(vertices)
        min_x, max_x = min(min_x, *(vertex[1] for vertex in vertices)), max(max_x, *(vertex[1] for vertex in vertices))
        min_y, max_y = min(min_y, *(vertex[0] for vertex in vertices)), max(max_y, *(vertex[0] for vertex in vertices))

    min_x = 0
    paths = [[(vertex[1] - min_x, vertex[0] - min_y + T_Y) for vertex in vertices] for vertices in paths]
    # Translate by T_Y horizontally to center the cave in a larger grid
    source = [0, Y_SOURCE - min_y + T_Y]
    w = max_y - min_y + 1 + 2 * T_Y
    h = max_x - min_x + 1 + 2

    cave = [["." for i in range(w + 2 * T_Y)] for j in range(h)]

    for i in range(w + 2 * T_Y):
        cave[h - 1][i] = "#"

    for vertices in paths:
        for i in range(1, len(vertices)):
            start, end = vertices[i - 1], vertices[i]
            start_to_end = (end[0] - start[0], end[1] - start[1])
            start_to_end_len = max(abs(start_to_end[0]), abs(start_to_end[1]))
            unit_start_to_end = (start_to_end[0] // start_to_end_len, start_to_end[1] // start_to_end_len)
            for j in range(start_to_end_len + 1):
                cave[start[0] + unit_start_to_end[0] * j][start[1] + unit_start_to_end[1] * j] = "#"

    sand_count = simulate(cave, source)
    print(sand_count)