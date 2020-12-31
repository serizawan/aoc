import sys


if len(sys.argv) != 2:
    print("Missing input file: python {} file".format(sys.argv[0]))
    sys.exit()

with open(sys.argv[1]) as f:
    l = f.read().splitlines()

x, y = 0, 0
step = 3
slope = 1
h = len(l)

n_trees = 0
while y <= h - slope:
    n_trees = n_trees + 1 if l[y][x] == '#' else n_trees
    # Pattern repeat horizontally
    x = (x + step) % len(l[0])
    y += slope

print(n_trees)
