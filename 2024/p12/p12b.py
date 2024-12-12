def neigh(l, c):
    vs = ((0, 1, "R"), (1, 0, "D"), (0, -1, "L"), (-1, 0, "U"))
    _neigh = []
    for v in vs:
        if 0 <= (n0:=l + v[0]) < L and 0 <= (n1:=c + v[1]) < C:
            _neigh.append((n0, n1))
    return _neigh


def expand_field(inner, outer):
    expanded_outer = set()
    for l, c in outer:
        for n in neigh(l, c):
            if n not in inner and raw_fields[l][c] == raw_fields[n[0]][n[1]]:
                expanded_outer.add(n)

    if not expanded_outer:
        return

    inner.update(outer)
    outer.clear()
    outer.update(expanded_outer)
    expand_field(inner, outer)


def fences(field):
    _fences = set()
    for l, c in field:
        vs = ((0, 1, "R"), (1, 0, "D"), (0, -1, "L"), (-1, 0, "U"))
        for v in vs:
            if 0 <= (n0 := l + v[0]) < L and 0 <= (n1 := c + v[1]) < C:
                if raw_fields[n0][n1] != raw_fields[l][c]:
                    _fences.add((l, c, v[2]))
            else:
                _fences.add((l, c, v[2]))
    return _fences


def expand_side(side, fs):
    side_ss = set(side)
    for side_f in side_ss:
        for f in set(fs):
            if side_f[2] == f[2]:
                if side_f[2] in "UD" and side_f[0] == f[0] and (side_f[1] == f[1] + 1 or side_f[1] == f[1] - 1):
                    side.add(f)
                if side_f[2] in "RL" and side_f[1] == f[1] and (side_f[0] == f[0] + 1 or side_f[0] == f[0] - 1):
                    side.add(f)
    if side_ss == side:
        return
    expand_side(side, fs)


def sides(fs):
    count = 0
    while fs:
        f = fs.pop()
        side = set()
        side.add(f)
        expand_side(side, fs)
        fs -= side
        count += 1
    return count


if __name__ == "__main__":
    raw_fields = open(0).read().splitlines()
    L, C = len(raw_fields), len(raw_fields[0])
    processed = set()
    fields = []
    for l in range(L):
        for c in range(C):
            if (l, c) in processed:
                continue
            else:
                inner, outer = set(), set()
                outer.add((l, c))
                expand_field(inner, outer)
                fields.append(inner.union(outer))
                processed.update(inner, outer)

    fencing_price = 0
    for field in fields:
        fencing_price += len(field) * sides(fences(field))

    print(fencing_price)


