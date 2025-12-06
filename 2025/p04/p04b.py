def is_accessible(i, j):
    DIRS = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if (i != 0 or j != 0)]
    MAX_ROLLS = 4
    return sum([grid[i + d[0]][j + d[1]] == "@" for d in DIRS if 0 <= i + d[0] < l and 0 <= j + d[1] < c]) < MAX_ROLLS

if __name__ == "__main__":
    grid = open(0).read().splitlines()
    grid = [list(l) for l in grid]
    l, c = len(grid), len(grid[0])
    removes = 0
    can_remove = True
    while can_remove:
        removed = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "@" and is_accessible(i, j):
                    grid[i][j] = "."
                    removed += 1
        removes += removed
        if not removed:
            can_remove = False

    print(removes)