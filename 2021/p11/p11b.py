from __future__ import annotations
import sys


class Octopus:
    MAX_ENERGY = 9

    def __init__(self, x: int, y: int, energy_level: int) -> None:
        self.x = x
        self.y = y
        self.energy_level = energy_level

    def get_neighbors(self, octopus_grid: OctopusGrid) -> list[Octopus]:
        neighbors = set()
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if (i != 0 or j != 0) and 0 <= self.x + i < octopus_grid.h and 0 <= self.y + j < octopus_grid.w:
                    neighbors.add(octopus_grid.octopuses[self.x + i][self.y + j])

        return neighbors


class OctopusGrid:
    def __init__(self, octopuses: list[list[Octopus]], flash_count=0) -> None:
        self.octopuses = octopuses
        self.flash_count = flash_count

    @property
    def h(self):
        return len(self.octopuses)

    @property
    def w(self):
        return len(self.octopuses[0])

    def _inc_by_one(self) -> None:
        for i, octopus_line in enumerate(self.octopuses):
            for j, octopus in enumerate(octopus_line):
                octopus.energy_level += 1

    def _flash_once(self) -> None:
        for i, octopus_line in enumerate(self.octopuses):
            for j, octopus in enumerate(octopus_line):
                if octopus.energy_level > Octopus.MAX_ENERGY:
                    self.flash_count += 1
                    octopus.energy_level = 0
                    neighbors = octopus.get_neighbors(self)
                    for neighbor in neighbors:
                        if neighbor.energy_level != 0:
                            neighbor.energy_level += 1

    @property
    def shall_flash(self):
        for octopus_line in self.octopuses:
            for octopus in octopus_line:
                if octopus.energy_level > Octopus.MAX_ENERGY:
                    return True
        return False

    def _flash(self) -> None:
        while self.shall_flash:
            self._flash_once()

    def next_step(self) -> None:
        self._inc_by_one()
        self._flash()

    @property
    def have_all_flashed(self) -> bool:
        return not sum(sum(octopus.energy_level for octopus in octopus_line) for octopus_line in self.octopuses)

    def __str__(self) -> str:
        bright_yellow = '\u001b[33;1m'
        reset = '\u001b[0m'
        grid_str = ''
        for octopus_line in self.octopuses:
            for octopus in octopus_line:
                if octopus.energy_level == 0:
                    grid_str += bright_yellow + str(octopus.energy_level) + reset
                else:
                    grid_str += str(octopus.energy_level)
            grid_str += '\n'
        return grid_str

    def glow(self, step):
        bright_yellow_bkg = '\u001b[43;1m'
        reset = '\u001b[0m'
        # +2 for line break on last grid line and step prints
        cursor_up_seq = f"\r\033[{self.h + 2}A"
        glowed_str = ''
        for octopus_line in self.octopuses:
            for octopus in octopus_line:
                if octopus.energy_level == 0:
                    glowed_str += bright_yellow_bkg + ' ' + reset
                else:
                    glowed_str += ' '
            glowed_str += '\n'
        print(f'{step = }')
        print(glowed_str)
        print(cursor_up_seq, end="")


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    octopuses = []
    for i, octopus_line in enumerate(lines):
        octopuses.append([Octopus(i, j, int(energy_level)) for j, energy_level in enumerate(octopus_line)])

    octopus_grid = OctopusGrid(octopuses)

    step = 0
    while not octopus_grid.have_all_flashed:
        step += 1
        octopus_grid.next_step()

    print(step)


if __name__ == "__main__":
    run()
