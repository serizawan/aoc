from __future__ import annotations
import logging
import sys


EMPTY = "."
RIGHT = ">"
DOWN = "v"


def pf(floor):
    """Print a floor."""
    for line in floor:
        print("".join(line))
    print()


def sf(floor):
    """Sign a floor."""
    return "".join(["".join(line) for line in floor])


def parse(filename: str):
    with open(filename) as f:
        lines = f.read().splitlines()

    floor = []
    for line in lines:
        floor.append(list(line))
    return floor


def run() -> None:
    if len(sys.argv) != 2:
        logging.error("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]))
        sys.exit()

    floor = parse(sys.argv[1])
    previous_floor_sign = ""
    step = 0
    while (floor_signature := sf(floor)) != previous_floor_sign:
        previous_floor_sign = floor_signature
        # Move right
        for line in floor:
            moves = []
            for i, c in enumerate(line):
                right_c_idx = (i + 1) % len(line)
                right_c = line[right_c_idx]
                if c == RIGHT and right_c == EMPTY:
                    moves.append((i, right_c_idx))
            for move in moves:
                line[move[0]] = EMPTY
                line[move[1]] = RIGHT

        # Move down
        for column_idx in range(len(floor[0])):
            moves = []
            for i, line in enumerate(floor):
                c = line[column_idx]
                down_c_idx = (i + 1) % len(floor)
                down_c = floor[down_c_idx][column_idx]
                if c == DOWN and down_c == EMPTY:
                    moves.append((i, down_c_idx))
            for move in moves:
                floor[move[0]][column_idx] = EMPTY
                floor[move[1]][column_idx] = DOWN

        step += 1

    print(step)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
