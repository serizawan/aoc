import re
import sys


def get_address_pattern(mask, value):
    # Skip '0b' two first characters of a binary string in Python
    value_as_bin_str = bin(value)[2:]
    # Iterate through reversed list to start with less significant bit.
    rev_mask = mask[::-1]
    address_pattern = ''
    for i, b in enumerate(rev_mask):
        if b == '0':
            bit_value = value_as_bin_str[::-1][i] if i < len(value_as_bin_str) else '0'
            # Don't use += here to append b on the left of address_pattern
            address_pattern = bit_value + address_pattern
        elif b == '1':
            address_pattern = b + address_pattern
        else:
            address_pattern = 'X' + address_pattern
    return address_pattern


def compute_addresses_from_pattern(address_pattern):
    n_X = address_pattern.count('X')
    idx_X = [i for i in range(len(address_pattern)) if address_pattern[i] == 'X']
    addresses = []
    i = 0
    replacements = None
    # Generate every binary number from 00...0 to 11...1 (pad on n_X bits with leading zeroes)
    while replacements != ['1'] * n_X:
        replacements = list(format(i, '0' + str(n_X) + 'b'))
        rp_copy = replacements[:]
        address = [a if a != 'X' else rp_copy.pop(0) for idx, a in enumerate(address_pattern)]
        addresses.append(int(''.join(address), 2))
        i += 1
    return addresses


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    mask = None
    idx_reg = re.compile('^mem\[(\d*)\]$')
    memory = {}
    for i in range(len(l)):
        if 'mask' in l[i]:
            mask = l[i].split(' = ')[1]
        else:
            mem, value_str = l[i].split(' = ')
            index = int(idx_reg.match(mem).group(1))
            value = int(value_str)
            address_pattern = get_address_pattern(mask, index)
            addresses = compute_addresses_from_pattern(address_pattern)
            for address in addresses:
                memory[address] = value
    print(sum(memory.values()))
