import sys


def is_valid(l, value):
    return value in {a + b for idx, a in enumerate(l) for b in l[idx + 1:]}


def compute_contiguous_sub_sum_indexes(l, value):
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            if value == sum(l[i:j]):
                return i, j


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    l = [int(r) for r in l]
    preamble_len = 25

    # Find the invalid number
    idx = preamble_len
    while is_valid(l[idx - preamble_len:idx], l[idx]):
        idx += 1

    invalid = l[idx]

    # Find the contiguous subsum that adds up to it
    i, j = compute_contiguous_sub_sum_indexes(l, invalid)
    print(min(l[i:j]) + max(l[i:j]))
