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
        sys.exit()

    points, instructions = parse(sys.argv[1])
    max_i, max_j = max(point[0] for point in points), max(point[1] for point in points)

    for instruction in instructions:
        result = set()
        for point in points:
            if instruction[0] == 'y' and point[0] > instruction[1]:
                sym_point = (2 * instruction[1] - point[0], point[1])
                result.add(sym_point)
            elif instruction[0] == 'x' and point[1] > instruction[1]:
                sym_point = (point[0], 2 * instruction[1] - point[1])
                result.add(sym_point)
            else:
                result.add(point)
        if instruction[0] == 'y':
            max_i = instruction[1]
        else:
            max_j = instruction[1]
        points = result

    white_bkg = '\u001b[47m'
    reset = '\u001b[0m'
    for i in range(max_i):
        line = ""
        for j in range(max_j):
            if (i, j) in points:
                line += white_bkg + " " + reset
            else:
                line += " "
        print(line)


if __name__ == "__main__":
    run()
