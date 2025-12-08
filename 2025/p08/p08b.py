import math


def dist_squared(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2


def index_of(min_dist):
    for li, l in enumerate(dists_squared):
        if min_dist in l:
            lj = l.index(min_dist)
            return li, lj
    return None, None


def group_of(p):
    for g in groups:
        if p in g:
            return g
    return frozenset()


if __name__ == "__main__":
    junctions = [tuple(int(i) for i in j.split(",")) for j in open(0).read().splitlines()]
    # Note that we put as a trick math.inf when j1 == j2 instead of 0 to avoid getting j1 == j2 when looking for min dist_squared.
    dists_squared = [[dist_squared(j1, j2) if j1 != j2 else math.inf for j1 in junctions] for j2 in junctions]
    groups = set([frozenset([j]) for j in junctions])
    while len(groups) != 1:
        # Getting min each time is sub-optimal (we shall have sorted the distances once). Complexity is O(n^2) instead
        # of O(n * log(n)) but the program still computes in reasonable time.
        min_dist = (min([min(dists_squared[i]) for i in range(len(dists_squared))]))
        i, j = index_of(min_dist)
        ji, jj = junctions[i], junctions[j]
        dists_squared[i][j] = math.inf
        dists_squared[j][i] = math.inf
        gi, gj = group_of(ji), group_of(jj)
        groups.discard(gi), groups.discard(gj)
        groups.add(gi.union(gj))

    print(ji[0] * jj[0])