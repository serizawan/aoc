import sys


DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
BG_COLORS = {
    'black': '\033[40m',
    'blue': '\033[44m',
    'light_blue': '\033[104m',
    'cyan': '\033[46m',
    'light_cyan': '\033[106m',
    'white': '\033[107m',
    'reset': '\033[0m',
}


def get_ansi(value: int):
    if value == 0:
        ansi = BG_COLORS['black']
    elif value in (1, 2):
        ansi = BG_COLORS['blue']
    elif value in (3, 4):
        ansi = BG_COLORS['light_blue']
    elif value in (5, 6):
        ansi = BG_COLORS['cyan']
    elif value in (7, 8):
        ansi = BG_COLORS['light_cyan']
    else:
        ansi = BG_COLORS['white']
    return ansi


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
            if self.is_in(i + d[0], j + d[1]) and self.grid[i][j] >= self.grid[i + d[0]][j + d[1]]:
                return False
        return True

    def is_in(self, i: int, j: int) -> True:
        return 0 <= i < self.h and 0 <= j < self.w

    def expand_once(self, basin: set) -> set:
        expanded_basin = basin.copy()
        for point in basin:
            x, y = point
            for d in DIRECTIONS:
                if self.is_in(x + d[0], y + d[1]) and self.grid[x][y] <= self.grid[x + d[0]][y + d[1]] < 9:
                    expanded_basin.add((x + d[0], y + d[1]))
        return expanded_basin

    def expand(self, basin: set) -> set:
        expanded_basin = self.expand_once(basin)
        while expanded_basin != basin:
            basin = expanded_basin.copy()
            expanded_basin = self.expand_once(expanded_basin)
        return basin

    def __str__(self) -> str:
        result = ''
        for line in self.grid:
            for value in line:
                ansi = get_ansi(value)
                result += ansi + ' ' + BG_COLORS['reset']
            result += '\n'
        return result


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
    basin_sizes = []
    for i in range(heatmap.h):
        for j in range(heatmap.w):
            if heatmap.is_low(i, j):
                basin = heatmap.expand({(i, j)})
                basin_sizes.append(len(basin))

    sorted_basin_size = sorted(basin_sizes, reverse=True)
    # print(heatmap)
    print(sorted_basin_size[0] * sorted_basin_size[1] * sorted_basin_size[2])


if __name__ == "__main__":
    run()
