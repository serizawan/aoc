import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    x, y = 0, 0
    for line in lines:
        direction, inc = line.split()
        inc = int(inc)
        if direction == 'forward':
            x += inc
        elif direction == 'up':
            y -= inc
        else:
            y += inc
    print(x*y)
