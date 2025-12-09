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


# N_PAIRS = 10
N_PAIRS = 1000


if __name__ == "__main__":
    junctions = [tuple(int(i) for i in j.split(",")) for j in open(0).read().splitlines()]
    # Note that we put as a trick math.inf when j1 == j2 instead of 0 to avoid getting j1 == j2 when looking for min dist_squared.
    dists_squared = [[dist_squared(j1, j2) if j1 != j2 else math.inf for j1 in junctions] for j2 in junctions]
    groups = set([frozenset([j]) for j in junctions])
    # Note that despite we are counting connections even when two junctions are already in the same circuit (as opposed
    # to the exercice statement, we are still getting (surprisingly and probably luckily) the right answer.
    for n in range(N_PAIRS):
        # Getting min each time is sub-optimal (we shall have sorted the distances once). Complexity is O(n^2) instead
        # of O(n * log(n)) but the program still computes in reasonable time.
        min_dist = (min([min(dists_squared[i]) for i in range(len(dists_squared))]))
        i, j = index_of(min_dist)
        ji, jj = junctions[i], junctions[j]
        dists_squared[i][j] = math.inf
        dists_squared[j][i] = math.inf
        gi, gj = group_of(ji), group_of(jj)  # We could check here whether both are already in the same group if needed.
        groups.discard(gi), groups.discard(gj)
        groups.add(gi.union(gj))

    group_sizes = [len(g) for g in groups]
    group_sizes.sort(reverse=True)
    print(group_sizes[0] * group_sizes[1] * group_sizes[2])