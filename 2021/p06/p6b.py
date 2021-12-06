from collections import defaultdict
import sys


DAYS = 256


class Fish:
    gestation_period = 6
    fecundity_age = 2

    def __init__(self, timer: int) -> None:
        self.timer = timer


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    timer_to_fish_count = defaultdict(int)
    fishes = [Fish(int(i)) for i in lines[0].split(',')]
    for fish in fishes:
        timer_to_fish_count[fish.timer] += 1

    for day in range(DAYS):
        max_timer = Fish.fecundity_age + Fish.gestation_period
        delivering_fish_count = timer_to_fish_count[0]
        for timer in range(1, max_timer + 1):
            timer_to_fish_count[timer - 1] = timer_to_fish_count[timer]
        timer_to_fish_count[max_timer] = delivering_fish_count
        timer_to_fish_count[Fish.gestation_period] += delivering_fish_count

    print(sum(timer_to_fish_count.values()))


if __name__ == "__main__":
    run()
