from __future__ import annotations
import sys


def parse(filename) -> (set[tuple[int]], list[tuple]):
    with open(filename) as f:
        lines = f.read().splitlines()

    points = set()
    while line := lines.pop(0):
        j, i = line.split(',')
        points.add((int(i), int(j)))

    instructions = []
    while lines and (line := lines.pop(0)):
        axis, value = line.split('=')
        axis, value = axis[-1], int(value)
        instructions.append((axis, value))
    return points, instructions


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr);
        sys.exit();

    points, instructions = parse(sys.argv[1])

    max_i, max_j = max(point[0] for point in points), max(point[1] for point in points)
    result = set()
    for point in points:
        if instructions[0][0] == 'y' and point[0] > max_i // 2:
            sym_point = (max_i - point[0], point[1])
            result.add(sym_point)
        elif instructions[0][0] == 'x' and point[1] > max_j // 2:
            sym_point = (point[0], max_j - point[1])
            result.add(sym_point)
        else:
            result.add(point)
    print(len(result))


if __name__ == "__main__":
    run()
