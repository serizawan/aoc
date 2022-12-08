import sys


def compute_scenic_score(i, j, grid):
    from_bottom_count, from_top_count = 0, 0
    from_right_count, from_left_count = 0, 0
    u = i + 1
    while u < len(grid) and grid[u][j] < grid[i][j]:
        from_bottom_count += 1
        u += 1
    if u < len(grid):
        from_bottom_count += 1

    v = i - 1
    while v >= 0 and grid[v][j] < grid[i][j]:
        from_top_count += 1
        v -= 1
    if v >= 0:
        from_top_count += 1

    w = j + 1
    while w < len(grid[0]) and grid[i][w] < grid[i][j]:
        from_right_count += 1
        w += 1
    if w < len(grid[0]):
        from_right_count += 1

    x = j - 1
    while x >= 0 and grid[i][x] < grid[i][j]:
        from_left_count += 1
        x -= 1
    if x >= 0:
        from_left_count += 1

    return from_bottom_count * from_top_count * from_right_count * from_left_count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Missing input file. Run with: python {sys.argv[0]} [FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    grid = []
    for line in lines:
        grid.append([int(i) for i in line])

    max_scenic_score = 0
    for i, line in enumerate(grid):
        for j, height in enumerate(line):
            if (scenic_score := compute_scenic_score(i, j, grid)) >= max_scenic_score:
                max_scenic_score = scenic_score

    print(max_scenic_score)


