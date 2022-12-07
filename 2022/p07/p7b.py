import re
import sys


TOTAL_SPACE = 70000000
REQUIRED_SPACE = 30000000


def visit(lines, result_list):
    total_size = 0
    while lines:
        head = lines.pop(0)
        if head == "$ cd ..":
            result_list.append(total_size)
            return result_list, total_size
        if extract_size := re.match("(\d*) .*", head):
            total_size += int(extract_size.group(1))
        elif re.match("\$ cd (.*)", head):
            result, sub_total_size = visit(lines, result_list)
            total_size += sub_total_size
        else:
            # Skip useless ls and dir commands
            continue
    result_list.append(total_size)
    return result_list, total_size


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Missing input file. Run with: python {sys.argv[0]} [FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    result_list, total_size = visit(lines, [])
    sorted_result_list = sorted(result_list)
    space_left = TOTAL_SPACE - total_size
    dir_size_idx = 0
    dir_size = sorted_result_list[dir_size_idx]
    while (dir_size := sorted_result_list[dir_size_idx]) < REQUIRED_SPACE - space_left:
        dir_size_idx += 1

    print(sorted_result_list[dir_size_idx])
