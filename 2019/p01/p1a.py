import sys


def compute_fuel(mass):
    return mass // 3 - 2


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    res = 0
    for line in lines:
        res += compute_fuel(int(line))

    print(res)
