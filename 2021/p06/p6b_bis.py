import sys

from sympy import *


DAYS = 256
GESTATION_PERIOD = 6
FECUNDITY_AGE = 2


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    timers = [int(i) for i in lines[0].split(',')]
    counts = [[0] for i in range(GESTATION_PERIOD + FECUNDITY_AGE + 1)]
    for timer in timers:
        counts[timer][0] += 1

    C = Matrix(counts)
    M = Matrix([[0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0]])

    print(sum((M ** DAYS) * C))


if __name__ == "__main__":
    run()
