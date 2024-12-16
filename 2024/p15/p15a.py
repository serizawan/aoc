def move(rl, rc, mv, obj):
    v = mvs_to_vs[mv]

    if obj == "." or obj == "#":
        return False, rl, rc

    if wh[rl + v[0]][rc + v[1]] == ".":
        wh[rl][rc] = "."
        wh[rl + v[0]][rc + v[1]] = obj
        return True, rl + v[0], rc + v[1]
    elif wh[rl + v[0]][rc + v[1]] == "O" and move(rl + v[0], rc + v[1], mv, "O")[0]:
        wh[rl][rc] = "."
        wh[rl + v[0]][rc + v[1]] = obj
        return True, rl + v[0], rc + v[1]
    # Blocked, do not move.
    else:
        return False, rl, rc

if __name__ == "__main__":
    wh_and_mvs = open(0).read().splitlines()
    i = wh_and_mvs.index("")
    wh = [list(l) for l in wh_and_mvs[:i]]
    mvs = "".join(wh_and_mvs[i+1:])
    mvs_to_vs = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
    rl, rc = 0, 0
    for i, l in enumerate(wh):
        for j, c in enumerate(l):
            if c == "@":
                rl, rc = i, j

    for mv in mvs:
        has_moved, rl, rc = move(rl, rc, mv,"@")

    sum_of_gps_lcs = sum([100 * i + j for i, l in enumerate(wh) for j, c in enumerate(l) if c == "O"])
    print(sum_of_gps_lcs)