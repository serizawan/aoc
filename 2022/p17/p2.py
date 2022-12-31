import sys


N_ROCKS = 1000000000000
# The pattern must be periodic at some point (can we mathematically forecast it?).
# By experimenting, we notice it occurs (both with sample and in) before 10k rocks have felt.
# We pick 8250 since one can notice that the pattern is complete with that value and no rocks will fall under
# (even under the pattern signature) later (for both sample and in). These has been found by trial and error.
# The first 20 lines shall be adequate to identify a period signature and identify the period length.
# Note that taking X top lines may lead to an incomplete pattern (hence none periodic), as it may be incomplete because
# future rocks would affect the X top lines.
# This parametrization works also for sample.txt
N_ROCKS_PERIOD = 8250
N_SIGNATURE_PERIOD = 20

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
        return 0

    @property
    def period(self):
        start_idx = len(self.values) - self.height
        for i in range(start_idx + N_SIGNATURE_PERIOD, len(self.values)):
            if all(self.values[i + j] == self.signature[j] for j in range(N_SIGNATURE_PERIOD)):
                return i - start_idx

    @property
    def signature(self):
        start_idx = len(self.values) - self.height
        return self.values[start_idx: start_idx + N_SIGNATURE_PERIOD]

    @property
    # The returned value is the index of the first occurrence of the period from the ground of the grid.
    def period_first_occurrence_from_end(self):
        has_occurred = False
        i = 0
        while not has_occurred:
            i += 1
            if all(self.values[-i - j] == self.signature[-1 - j] for j in range(N_SIGNATURE_PERIOD)):
                has_occurred = True
        return i

    def compute_floor_idx(self):
        for idx, line in enumerate(self.values):
            if "#" in line:
                return idx
        return idx

    def simulate(self, rock_idx, jet_idx, floor_idx):
        shape = SHAPES[rock_idx % len(SHAPES)]
        left_idx = FROM_LEFT
        top_idx = 0
        rock = Rock(shape, left_idx, top_idx)
        grid.values = grid.values[floor_idx:]
        grid.values = [["."] * W for i in range(FROM_BOTTOM)] + grid.values
        grid.values = [["."] * W for i in range(len(shape))] + grid.values
        has_felt = True
        while has_felt:
            rock.move(jets[jet_idx])
            has_felt = rock.fall()
            jet_idx = (jet_idx + 1) % len(jets)

        rock.add_to_grid()
        floor_idx = grid.compute_floor_idx()

        return jet_idx, floor_idx

    def __str__(self):
        return "\n".join(["".join(line) for line in self.values]) + "\n"


class Rock:
    def __init__(self, shape, left_idx, top_idx):
        self.shape = shape
        self.left_idx = left_idx
        self.top_idx = top_idx

    @property
    def can_move_right(self):
        for idx, line in enumerate(self.shape):
            is_out = (self.left_idx + len(line) == W)
            is_filled = is_out or any([(line[jdx], grid.values[self.top_idx + idx][self.left_idx + jdx + 1]) == ("#", "#") for jdx in range(len(line))])
            if is_filled:
                return False
        return True

    @property
    def can_move_left(self):
        for idx, line in enumerate(self.shape):
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
        if jet == ">" and self.can_move_right:
            self.left_idx += 1
        elif jet == "<" and self.can_move_left:
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
    for i in range(N_ROCKS_PERIOD):
        jet_idx, floor_idx = grid.simulate(i, jet_idx, floor_idx)

    period_first_occurence_from_end = grid.period_first_occurrence_from_end
    grid_height = grid.height
    grid_period = grid.period

    grid = Grid([])
    jet_idx = 0
    floor_idx = 0
    i = 0
    while grid.height != period_first_occurence_from_end + N_SIGNATURE_PERIOD - 1:
        jet_idx, floor_idx = grid.simulate(i, jet_idx, floor_idx)
        i += 1

    n_rocks_to_reach_first_period_occurence_included = i
    remaining_rocks = N_ROCKS_PERIOD - n_rocks_to_reach_first_period_occurence_included
    remaining_grid_height = grid_height - grid.height
    n_period_in_remaining_grid = remaining_grid_height // grid_period
    n_rocks_per_period = remaining_rocks // n_period_in_remaining_grid
    n_period = (N_ROCKS - n_rocks_to_reach_first_period_occurence_included) // n_rocks_per_period
    n_rocks_to_complete = (N_ROCKS - n_rocks_to_reach_first_period_occurence_included) % n_rocks_per_period

    for i in range(n_rocks_to_complete):
        jet_idx, floor_idx = grid.simulate(i, jet_idx, floor_idx)

    print(grid_period * n_period + grid.height)
