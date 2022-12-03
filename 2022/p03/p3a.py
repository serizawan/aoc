import sys


LOWER_A_ORD = 97
UPPER_A_ORD = 65
N_LETTERS = 26


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    priorities_sum = 0
    for line in lines:
        half_n_items = len(line) // 2
        left = set(line[:half_n_items])
        right = set(line[half_n_items:])
        shared = left.intersection(right)
        for s in shared:
            if s.lower() == s:
                priorities_sum += (ord(s) - LOWER_A_ORD + 1)
            else:
                priorities_sum += (ord(s) - UPPER_A_ORD + 1 + N_LETTERS)

    print(priorities_sum)
