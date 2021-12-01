import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    measures = [int(line) for line in lines]

    inc_count = 0
    for i in range(len(measures) - 1):
        if measures[i + 1] - measures[i] > 0:
            inc_count += 1

    print(inc_count)
