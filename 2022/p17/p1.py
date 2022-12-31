import sys


N_ROCKS = 2022
SHAPES = [
    ["####"],
    [".#.",
     "###",
     ".#."],
    ["..#",
     "..#",
     "###"],
    ["#",
     "#",
     "#",
     "#"],
    ["##",
     "##"]
]
FROM_LEFT = 2
FROM_BOTTOM = 3
W = 7


class Grid:
    def __init__(self, values):
        self.values = values

    @property
    def height(self):
        idx = 0
        for line in self.values:
            if "#" in line:
                return len(grid.values) - idx
            idx += 1

    def compute_floor_idx(self):
        for idx, line in enumerate(self.values):
            if "#" in line:
                return idx
        return idx

    def __str__(self):
        return "\n".join(["".join(line) for line in self.values]) + "\n"


class Rock:
    def __init__(self, shape, left_idx, top_idx):
        self.shape = shape
        self.left_idx = left_idx
        self.top_idx = top_idx

    @property
    def can_move_right(self):
        for idx, line in enumerate(shape):
            is_out = (self.left_idx + len(line) == W)
            is_filled = is_out or any([(line[jdx], grid.values[self.top_idx + idx][self.left_idx + jdx + 1]) == ("#", "#") for jdx in range(len(line))])
            if is_filled:
                return False
        return True

    @property
    def can_move_left(self):
        for idx, line in enumerate(shape):
            is_out = (self.left_idx == 0)
            is_filled = is_out or any([(line[jdx], grid.values[self.top_idx + idx][self.left_idx + jdx - 1]) == ("#", "#") for jdx in range(len(line))])
            if is_filled:
                return False
        return True

    @property
    def can_fall(self):
        for idx, line in enumerate(self.shape):
            bottom_shape_idx = self.top_idx + len(self.shape) - 1
            is_out = (bottom_shape_idx + 1 == len(grid.values))
            is_filled = is_out or any([(line[jdx], grid.values[self.top_idx + idx + 1][self.left_idx + jdx]) == ("#", "#") for jdx in range(len(line))])
            if is_filled:
                return False
        return True

    def move(self, jet):
        if jet == ">" and rock.can_move_right:
            self.left_idx += 1
        elif jet == "<" and rock.can_move_left:
            self.left_idx -= 1

    def fall(self):
        can_fall = self.can_fall
        if has_felt := can_fall:
            self.top_idx += 1
        return has_felt

    def add_to_grid(self):
        for idx, line in enumerate(self.shape):
            slice_to_update = grid.values[self.top_idx + idx][self.left_idx:len(line) + self.left_idx]
            for jdx, c in enumerate(line):
                if c == "#" or slice_to_update[jdx] == "#":
                    slice_to_update[jdx] = "#"
            grid.values[self.top_idx + idx][self.left_idx:len(line) + self.left_idx] = slice_to_update


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    jets = lines[0]

    grid = Grid([])
    jet_idx = 0
    floor_idx = 0
    for i in range(N_ROCKS):
        shape = SHAPES[i % len(SHAPES)]
        left_idx = FROM_LEFT
        top_idx = 0
        rock = Rock(shape, left_idx, top_idx)
        grid.values = grid.values[floor_idx:]
        grid.values = [["."] * W for i in range(FROM_BOTTOM)] + grid.values
        grid.values = [["."] * W for i in range(len(shape))] + grid.values
        has_felt = True
        while has_felt:
            jet = jets[jet_idx]
            rock.move(jets[jet_idx])
            has_felt = rock.fall()
            jet_idx = (jet_idx + 1) % len(jets)

        rock.add_to_grid()
        floor_idx = grid.compute_floor_idx()

    print(grid.height)
