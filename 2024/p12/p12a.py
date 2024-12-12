def neigh(l, c):
    vs = ((0, 1), (1, 0), (0, -1), (-1, 0))
    _neigh = []
    for v in vs:
        if 0 <= (n0:=l + v[0]) < L and 0 <= (n1:=c + v[1]) < C:
            _neigh.append((n0, n1))
    return _neigh


def expand(inner, outer):
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
    expand(inner, outer)


def perimeter(field):
    p = 0
    for l, c in field:
        for n in (ns:=neigh(l, c)):
            if raw_fields[n[0]][n[1]] != raw_fields[l][c]:
                p += 1
        p += 4 - len(ns)
    return p


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
                expand(inner, outer)
                fields.append(inner.union(outer))
                processed.update(inner, outer)

    fencing_price = 0
    for field in fields:
        fencing_price += len(field) * perimeter(field)

    print(fencing_price)


