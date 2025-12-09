# Return True if [u, v] and [x, y] do overlap.
def do_overlap(u, v, x, y):
    mini_sup = min(max(u, v), max(x, y))
    maxi_inf = max(min(u, v), min(x, y))
    return maxi_inf < mini_sup

# Return True if [tu, tv] segment crosses the (inner) rectangle defined by t1 and t2 corners.
def is_crossed(tu, tv, t1, t2):
    if tu == t1 or tu == t2 or tv == t1 or tv == t2:
        return False

    # Vertical case.
    if tu[0] == tv[0] and min(t1[0], t2[0]) < tu[0] < max(t1[0], t2[0]) and do_overlap(tu[1], tv[1], t1[1], t2[1]):
        return True
    # Horizontal case.
    if tu[1] == tv[1] and min(t1[1], t2[1]) < tu[1] < max(t1[1], t2[1]) and do_overlap(tu[0], tv[0], t1[0], t2[0]):
        return True

    return False


if __name__ == "__main__":
    tiles = [[int(i) for i in l.split(",")] for l in open(0).read().splitlines()]
    max_area = 0
    for t1 in tiles:
        for t2 in tiles:
            # Actually this trick works only because the input has some (inferred) constraints.
            # It would not work with any random tiles (only respecting the problem statement).
            # Basically, we consider a rectangle valid whether there is no other consecutive tiles segment that
            # crosses its inner area (but that may exclude valid rectangles).
            if not any(is_crossed(tu, tv, t1, t2) for tu, tv in zip(tiles, tiles[1:] + [tiles[0]])):
                max_area = max(max_area, (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1))

    print(max_area)
