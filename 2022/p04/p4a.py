import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Missing input file. Run with: python {sys.argv[0]} [FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    count_redundancies = 0
    for line in lines:
        left, right = line.split(",")
        left_elf, right_elf = [int(i) for i in left.split("-")], [int(i) for i in right.split("-")]
        left_has_right = left_elf[0] <= right_elf[0] and left_elf[1] >= right_elf[1]
        right_has_left = right_elf[0] <= left_elf[0] and right_elf[1] >= left_elf[1]
        # += left_has_right or right_has_left works as well
        count_redundancies += 1 if left_has_right or right_has_left else 0
    print(count_redundancies)
