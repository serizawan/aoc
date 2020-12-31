import sys


def is_valid(l, value):
    return value in {a + b for idx, a in enumerate(l) for b in l[idx + 1:]}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    l = [int(r) for r in l]
    preamble_len = 25

    idx = preamble_len
    while is_valid(l[idx - preamble_len:idx], l[idx]):
        idx += 1

    print(l[idx])
