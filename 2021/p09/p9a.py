import sys


DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Heatmap:
    def __init__(self, grid) -> None:
        self.grid = grid

    @property
    def h(self) -> int:
        return len(self.grid)

    @property
    def w(self) -> int:
        return len(self.grid[0])

    def is_low(self, i: int, j: int) -> bool:
        for d in DIRECTIONS:
            if 0 <= i + d[0] < self.h and 0 <= j + d[1] < self.w and self.grid[i][j] >= self.grid[i + d[0]][j + d[1]]:
                return False
        return True


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    grid = []
    for line in lines:
        grid.append([int(c) for c in line])

    heatmap = Heatmap(grid)
    risk_level_total = 0
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if heatmap.is_low(i, j):
                risk_level_total += 1 + heatmap.grid[i][j]

    print(risk_level_total)


if __name__ == "__main__":
    run()