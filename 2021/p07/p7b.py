import sys


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    crab_xs = [int(i) for i in lines[0].split(',')]
    min_total_fuel = sys.maxsize
    for pos in range(max(crab_xs) + 1):
        total_fuel = 0
        for crab_x in crab_xs:
            total_fuel += (abs(pos - crab_x))*(abs(pos - crab_x) + 1) // 2
        if total_fuel <= min_total_fuel:
            # Commented lines are just an experimental test to check if "mean" of crab position minimizes fuel spent
            # It turns out it is almost true: Sometimes it is floor(mean) and sometimes it is ceil(mean) but round(mean)
            # does not give always the right result (test with example.txt vs 7.txt).
            # min_pos = pos
            min_total_fuel = total_fuel
        # min_pos_exp = sum(crab_xs) / len(crab_xs)
    # print(min_pos, min_pos_exp)
    print(min_total_fuel)


if __name__ == "__main__":
    run()