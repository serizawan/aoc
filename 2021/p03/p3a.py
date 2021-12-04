import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    length = len(lines)
    counts = [0] * len(lines[0])
    for line in lines:
        bit_idx = 0
        for bit in line:
            if bit == '1':
                counts[bit_idx] += 1
            bit_idx += 1

    gamma = ['0'] * len(lines[0])
    idx = 0
    for count in counts:
        if count * 2 > length:
            gamma[idx] = '1'
        idx += 1

    epsilon = ['0'] * len(lines[0])
    for jdx in range(len(epsilon)):
        if gamma[jdx] == '0':
            epsilon[jdx] = '1'
    print(epsilon)
    print(int(''.join(gamma), 2) * int(''.join(epsilon), 2))
