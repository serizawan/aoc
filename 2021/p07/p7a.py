import sys


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    crab_xs = sorted([int(i) for i in lines[0].split(',')])
    median = crab_xs[len(crab_xs) // 2]
    total_fuel = 0
    for crab_x in crab_xs:
        total_fuel += abs(median - crab_x)
    print(total_fuel)


if __name__ == "__main__":
    run()