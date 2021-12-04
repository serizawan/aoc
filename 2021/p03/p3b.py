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

    o2_rating = lines.copy()
    i = 0
    while len(o2_rating) > 1:
        count = 0
        for o2_rating_line in o2_rating:
            if o2_rating_line[i] == '1':
                count += 1
        bit = '0'
        if count * 2 >= len(o2_rating):
            bit = '1'
        o2_rating = [line for line in o2_rating if line[i] == bit]
        i += 1

    co2_rating = lines.copy()
    j = 0
    while len(co2_rating) > 1:
        count = 0
        for co2_rating_line in co2_rating:
            if co2_rating_line[j] == '1':
                count += 1
        bit = '1'
        if count * 2 >= len(co2_rating):
            bit = '0'
        co2_rating = [line for line in co2_rating if line[j] == bit]
        j += 1

    print(o2_rating, co2_rating)
    print(int(''.join(o2_rating), 2) * int(''.join(co2_rating), 2))
