import sys


if len(sys.argv) != 2:
    print("Missing input file: python {} file".format(sys.argv[0]))
    sys.exit()

with open(sys.argv[1]) as f:
    l = f.read().splitlines()

steps_and_slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
h = len(l)

l_trees = []
for step, slope in steps_and_slopes:
    x, y = 0, 0
    n_trees = 0
    while y <= h - slope:
        n_trees = n_trees + 1 if l[y][x] == '#' else n_trees
        # Pattern repeat horizontally
        x = (x + step) % len(l[0])
        y += slope
    l_trees.append(n_trees)

result = 1
for n in l_trees:
    result *= n

print(result)
