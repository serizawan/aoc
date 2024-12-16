def can_move(rl, rc, mv, obj):
    v = mvs_to_vs[mv]

    if obj == "." or obj == "#":
        return False

    if obj == "@":
        if wh[rl + v[0]][rc + v[1]] == ".":
            return True
        if wh[rl + v[0]][rc + v[1]] in "[]":
            return can_move(rl + v[0], rc + v[1], mv, "[]") if wh[rl + v[0]][rc + v[1]] == "[" else can_move(rl + v[0], rc - 1 + v[1], mv, "[]")
        return False

    if obj == "[]":
        if mv == "<" and wh[rl + v[0]][rc + v[1]] != "#":
            return wh[rl + v[0]][rc + v[1]] == "." or can_move(rl + v[0], rc - 1 + v[1], mv, "[]")
        if mv == ">" and wh[rl + v[0]][rc + v[1]] != "#":
            return wh[rl + v[0]][rc + v[1]] == "." or can_move(rl + v[0], rc + v[1], mv, "[]")
        if mv in "^v":
            if wh[rl + v[0]][rc + v[1]] == "." and wh[rl + v[0]][rc + 1 + v[1]] == ".":
                return True
            if wh[rl + v[0]][rc + v[1]] == "[":
                return can_move(rl + v[0], rc + v[1], mv, "[]")
            if wh[rl + v[0]][rc + v[1]] == "]" and wh[rl + v[0]][rc + 1 + v[1]] == ".":
                return can_move(rl + v[0], rc + - 1 + v[1], mv, "[]")
            if wh[rl + v[0]][rc + v[1]] == "." and wh[rl + v[0]][rc + 1 + v[1]] == "[":
                return can_move(rl + v[0], rc + 1 + v[1], mv, "[]")
            if wh[rl + v[0]][rc + v[1]] == "]" and wh[rl + v[0]][rc + 1 + v[1]] == "[":
                return can_move(rl + v[0], rc + - 1 + v[1], mv, "[]") and can_move(rl + v[0], rc + 1 + v[1], mv, "[]")
        return False

    return False

def move(rl, rc, mv, obj):
    v = mvs_to_vs[mv]

    if obj == "." or obj == "#":
        return rl, rc

    if obj == "@":
        if wh[rl + v[0]][rc + v[1]] in "[]":
            move(rl + v[0], rc + v[1], mv, "[]") if wh[rl + v[0]][rc + v[1]] == "[" else move(rl + v[0], rc - 1 + v[1], mv, "[]")
        wh[rl][rc] = "."
        wh[rl + v[0]][rc + v[1]] = "@"
        return rl + v[0], rc + v[1]

    if obj == "[]":
        if (mv == ">" and wh[rl + v[0]][rc + 1 + v[1]] == ".") or (mv in "<" and wh[rl + v[0]][rc + v[1]] == "."):
            wh[rl][rc] = "."
            wh[rl + v[0]][rc + v[1]], wh[rl + v[0]][rc + v[1] + 1] = "[", "]"
            return rl + v[0], rc + v[1]
        if mv in ">" and wh[rl + v[0]][rc + 1 + v[1]] == "[":
            move(rl + v[0], rc + v[1] + 1, mv, "[]")
            wh[rl][rc] = "."
            wh[rl + v[0]][rc + v[1]], wh[rl + v[0]][rc + v[1] + 1] = "[", "]"
            return rl + v[0], rc + v[1]
        if mv in "<" and wh[rl + v[0]][rc + v[1]] == "]":
            move(rl + v[0], rc - 1 + v[1], mv, "[]")
            wh[rl][rc + 1] = "."
            wh[rl + v[0]][rc + v[1]], wh[rl + v[0]][rc + v[1] + 1] = "[", "]"
            return rl + v[0], rc + v[1]
        if mv in "^v":
            if wh[rl + v[0]][rc + v[1]] == "[":
                move(rl + v[0], rc + v[1], mv, "[]")
            if wh[rl + v[0]][rc + v[1]] == "]" and wh[rl + v[0]][rc + 1 + v[1]] == ".":
                move(rl + v[0], rc - 1 + v[1], mv, "[]")
            if wh[rl + v[0]][rc + v[1]] == "." and wh[rl + v[0]][rc + 1 + v[1]] == "[":
                move(rl + v[0], rc + 1 + v[1], mv, "[]")
            if wh[rl + v[0]][rc + v[1]] == "]" and wh[rl + v[0]][rc + 1 + v[1]] == "[":
                move(rl + v[0], rc - 1 + v[1], mv, "[]")
                move(rl + v[0], rc + 1 + v[1], mv, "[]")
            wh[rl][rc], wh[rl][rc + 1] = ".", "."
            wh[rl + v[0]][rc + v[1]], wh[rl + v[0]][rc + v[1] + 1] = "[", "]"
            return rl + v[0], rc + v[1]


if __name__ == "__main__":
    wh_and_mvs = open(0).read().splitlines()
    i = wh_and_mvs.index("")
    wh = wh_and_mvs[:i]
    for i in range(len(wh)):
        wh[i] = wh[i].replace("#", "##")
        wh[i] = wh[i].replace("O", "[]")
        wh[i] = wh[i].replace(".", "..")
        wh[i] = wh[i].replace("@", "@.")

    wh = [list(l) for l in wh]

    mvs = "".join(wh_and_mvs[i+1:])
    mvs_to_vs = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
    rl, rc = 0, 0
    for i, l in enumerate(wh):
        for j, c in enumerate(l):
            if c == "@":
                rl, rc = i, j

    for mv in mvs:
        if can_move(rl, rc, mv, "@"):
            rl, rc = move(rl, rc, mv,"@")

    sum_of_gps_lcs = sum([100 * i + j for i, l in enumerate(wh) for j, c in enumerate(l) if c == "["])
    print(sum_of_gps_lcs)

