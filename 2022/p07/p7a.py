import re
import sys


DIR_SIZE_LIMIT = 100000


# Note that this walkthrough works because commands follow a DFS pattern.
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
    print(sum([dir_size for dir_size in result_list if dir_size <= DIR_SIZE_LIMIT]))
