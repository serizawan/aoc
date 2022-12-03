import sys


N_LETTERS = 26


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    priorities_sum = 0
    for i in range(len(lines) // 3):
        elf1, elf2, elf3 = set(lines[3 * i]), set(lines[3 * i + 1]), set(lines[3 * i + 2])
        shared = elf1.intersection(elf2).intersection(elf3)
        for s in shared:
            if s.lower() == s:
                priorities_sum += (ord(s) - ord('a') + 1)
            else:
                priorities_sum += (ord(s) - ord('A') + 1 + N_LETTERS)

    print(priorities_sum)
