from collections import defaultdict
import math
import sys


sys.setrecursionlimit(5_000)


def neighbors(p, ps):
    return [(p[0] + v[0], p[1] + v[1], v[2]) for v in vs if (p[0] + v[0], p[1] + v[1]) not in ps and maze[p[0] + v[0]][p[1] + v[1]] in ".E"]


def explore(p, ps, score, min_score):
    if p[:2] == e:
        if score < min_score:
            tiles.clear()
            tiles.update(ps)
        elif score == min_score:
            tiles.update(ps)
        return min(score, min_score)

    _neighbors = neighbors(p, ps)
    if not _neighbors:
        return math.inf

    for n in _neighbors:
        updated_score = score + 1 if p[2] == n[2] else score + 1001
        if updated_score < cache[n]:
            cache[n] = updated_score
            ps.add(n[:2])
            min_score = min(explore(n, ps, updated_score, min_score), min_score)
            ps.remove(n[:2])
        elif updated_score == cache[n] and n[:2] in tiles:
            tiles.update(ps)

    return min_score


if __name__ == "__main__":
    maze = open(0).read().splitlines()
    p = (len(maze) - 2, 1, "R")
    ps = {p[:2]}
    vs = [(0, 1, "R"), (1, 0, "D"), (0, -1, "L"), (-1, 0, "U")]
    e = (1, len(maze[0]) - 2)
    cache = defaultdict(lambda: math.inf)
    tiles = set()
    min_score = explore(p, ps, 0, math.inf)
    print(len(tiles))