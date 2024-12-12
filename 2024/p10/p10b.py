def neighbors(p):
    vs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    p_neighbors = []
    for v in vs:
        if 0 <= (l:=p[0] + v[0]) < L and 0 <= (c:=p[1] + v[1]) < C:
            p_neighbors.append((l,c))
    return p_neighbors


def count_trails_rec(p, c):
    if map[p[0]][p[1]] == 9:
        return c + 1

    for n in neighbors(p):
        if map[n[0]][n[1]] == map[p[0]][p[1]] + 1:
            c = count_trails_rec(n, c)
    return c


def count_trails_it(p):
    trails = [p]
    trails_count = 0
    while trails:
        h = trails.pop()
        if h == 9:
            trails_count += 1
        for n in neighbors(h):
            if map[n[0]][n[1]] == map[h[0]][h[1]] + 1:
                trails.append(n)
    return trails_count


if __name__ == "__main__":
    map = open(0).read().splitlines()
    map = [[int(i) for i in line] for line in map]
    L, C = len(map), len(map[0])
    zeroes = [(l, c) for l in range(L) for c in range(C) if map[l][c] == 0]

    ratings_sum_rec = 0
    ratings_sum_it = 0
    for z in zeroes:
        ratings_sum_rec += count_trails_rec(z, 0)
        ratings_sum_it += count_trails_rec(z, 0)

    print(ratings_sum_rec)
    print(ratings_sum_it)