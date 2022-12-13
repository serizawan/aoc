from copy import deepcopy
from functools import cmp_to_key
import sys


N_LINES_PER_CASE = 3
LOW_DIVIDER_PACKET = [[2]]
HIGH_DIVIDER_PACKET = [[6]]


# Compares WITHOUT side effect on method parameters
def compare(left_list, right_list):
    left_list_copy = deepcopy(left_list)
    right_list_copy = deepcopy(right_list)
    compare_result = cmp(left_list, right_list)
    left_list.clear(), right_list.clear()
    left_list += left_list_copy
    right_list += right_list_copy
    return compare_result


# Compares WITH side effect on method parameters
def cmp(left_list, right_list):
    while left_list and right_list:
        left = left_list.pop(0)
        right = right_list.pop(0)
        if type(left) == int and type(right) == int:
            if left < right:
                return -1
            elif left > right:
                return 1
        elif type(left) == int and type(right) == list:
            if (compare_result := cmp([left], right)) in (-1, 1):
                return compare_result
        elif type(left) == list and type(right) == int:
            if (compare_result := cmp(left, [right])) in (-1, 1):
                return compare_result
        else:
            if (compare_result := cmp(left, right)) in (-1, 1):
                return compare_result
    if not left_list and right_list:
        return -1
    if left_list and not right_list:
        return 1
    if not left_list and not right_list:
        return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    items = []
    for i in range(len(lines) // N_LINES_PER_CASE + 1):
        p1 = eval(lines[N_LINES_PER_CASE * i])
        p2 = eval(lines[N_LINES_PER_CASE * i + 1])
        items.append(p1), items.append(p2)

    items.append(LOW_DIVIDER_PACKET)
    items.append(HIGH_DIVIDER_PACKET)
    items = sorted(items, key=cmp_to_key(compare))

    low_idx, high_idx = 0, 0
    for idx, i in enumerate(items):
        if i == LOW_DIVIDER_PACKET:
            low_idx = idx + 1
        if i == HIGH_DIVIDER_PACKET:
            high_idx = idx + 1

    print(low_idx * high_idx)