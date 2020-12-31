import re
import sys


def apply_mask(mask, value):
    # Skip '0b' two first characters of a binary string in Python
    value_as_bin_str = bin(value)[2:]
    # Iterate through reversed list to start with less significant bit.
    rev_mask = mask[::-1]
    result = ''
    for i, b in enumerate(rev_mask):
        if b == '0' or b == '1':
            # Don't use += here to append b on the left of result
            result = b + result
        else:
            bit_value = value_as_bin_str[::-1][i] if i < len(value_as_bin_str) else '0'
            result = bit_value + result
    return result


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
            stored_value = apply_mask(mask, value)
            memory[index] = int(stored_value, 2)

    print(sum(memory.values()))
