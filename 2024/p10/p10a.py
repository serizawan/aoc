def neighbors(p):
    vs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    p_neighbors = []
    for v in vs:
        if 0 <= (l:=p[0] + v[0]) < L and 0 <= (c:=p[1] + v[1]) < C:
            p_neighbors.append((l,c))
    return p_neighbors


def count_trails(p, trails_end):
    if map[p[0]][p[1]] == 9:
        trails_end.add(p)

    for n in neighbors(p):
        if map[n[0]][n[1]] == map[p[0]][p[1]] + 1:
            count_trails(n, trails_end)


if __name__ == "__main__":
    map = open(0).read().splitlines()
    map = [[int(i) for i in line] for line in map]
    L, C = len(map), len(map[0])
    zeroes = [(l, c) for l in range(L) for c in range(C) if map[l][c] == 0]

    scores_sum = 0
    for z in zeroes:
        trails_end = set()
        count_trails(z, trails_end)
        scores_sum += len(trails_end)

    print(scores_sum)