import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Missing input file. Run with: python {sys.argv[0]} [FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    marker_len = 14
    i = marker_len
    for line in lines:
        while len(set(line[i-marker_len: i])) != marker_len:
            i += 1
        print(i)
