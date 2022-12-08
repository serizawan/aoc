import sys


def is_tree_visible(i, j, grid):
    is_visible_from_bottom, is_visible_from_top = True, True
    is_visible_from_right, is_visible_from_left = True, True
    for u in range(i + 1, len(grid)):
        if grid[u][j] >= grid[i][j]:
            is_visible_from_bottom = False
    for v in range(i - 1, -1, -1):
        if grid[v][j] >= grid[i][j]:
            is_visible_from_top = False
    for w in range(j + 1, len(line)):
        if grid[i][w] >= grid[i][j]:
            is_visible_from_right = False
    for x in range(j - 1, -1, -1):
        if grid[i][x] >= grid[i][j]:
            is_visible_from_left = False
    return is_visible_from_bottom or is_visible_from_top or is_visible_from_right or is_visible_from_left


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Missing input file. Run with: python {sys.argv[0]} [FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    grid = []
    for line in lines:
        grid.append([int(i) for i in line])

    visible_tree_count = 0
    for i, line in enumerate(grid):
        for j, height in enumerate(line):
            if is_tree_visible(i, j, grid):
                visible_tree_count += 1

    print(visible_tree_count)


