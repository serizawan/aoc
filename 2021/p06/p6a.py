from __future__ import annotations
import sys


DAYS = 80


class Fish:
    gestation_period = 6
    fecundity_age = 2

    def __init__(self, timer: int, children: list[Fish]) -> None:
        self.timer = timer
        self.children = children

    def pass_day(self) -> None:
        self.timer -= 1

        for child in self.children:
            child.pass_day()

        if self.timer == -1:
            self.timer = self.gestation_period
            self.children.append(Fish(self.gestation_period + self.fecundity_age, []))

    def pass_n_days(self, n_days: int) -> None:
        for i in range(n_days):
            self.pass_day()

    @property
    def lineage_count(self):
        lineage_count = 1
        if self.children == 0:
            return lineage_count

        for child in self.children:
            lineage_count += child.lineage_count
        return lineage_count


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    school = [Fish(int(i), []) for i in lines[0].split(',')]
    fish_count = 0
    while school:
        fish = school.pop(0)
        fish.pass_n_days(DAYS)
        fish_count += fish.lineage_count
    print(fish_count)


if __name__ == "__main__":
    run()
