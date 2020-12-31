import sys


def compute_rc(boarding_pass):
    rows_identifier_len = 7
    r = letters_to_int(boarding_pass[0:rows_identifier_len], 'B')
    c = letters_to_int(boarding_pass[rows_identifier_len:], 'R')
    return r, c


def letters_to_int(letters, one_char):
    n = 0
    bit_pow = 1
    for letter in reversed(letters):
        if letter == one_char:
            n += bit_pow
        bit_pow *= 2
    return n


def compute_id(r, c):
    return r * 8 + c


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    ids = []
    for boarding_pass in l:
        ids.append(compute_id(*compute_rc(boarding_pass)))

    ids.sort()
    i = 0
    while ids[i+1] - ids[i] == 1:
        i += 1

    print(ids[i] + 1)
