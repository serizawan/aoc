import re
import sys


TOTAL_SPACE = 70000000
REQUIRED_SPACE = 30000000


# Note that this walkthrough works because commands follow a DFS pattern.
def visit(lines, dir_sizes):
    total_size = 0
    while lines:
        head = lines.pop(0)
        if head == "$ cd ..":
            dir_sizes.append(total_size)
            return total_size, dir_sizes
        elif extract_size := re.match("(\d*) .*", head):
            total_size += int(extract_size.group(1))
        elif re.match("\$ cd (.*)", head):
            sub_total_size, dir_sizes = visit(lines, dir_sizes)
            total_size += sub_total_size
        else:
            # Skip useless ls and dir commands
            continue
    dir_sizes.append(total_size)
    return total_size, dir_sizes


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Missing input file. Run with: python {sys.argv[0]} [FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    total_size, dir_sizes = visit(lines, [])
    sorted_dir_sizes = sorted(dir_sizes)
    space_left = TOTAL_SPACE - total_size
    dir_size_idx = 0
    dir_size = sorted_dir_sizes[dir_size_idx]
    while (dir_size := sorted_dir_sizes[dir_size_idx]) < REQUIRED_SPACE - space_left:
        dir_size_idx += 1

    print(sorted_dir_sizes[dir_size_idx])
