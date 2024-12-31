def next(n):
    l, c = n
    vs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for v in vs:
        if race[l + v[0]][c + v[1]] in ".E" and (l + v[0], c + v[1]) not in track:
            return l + v[0], c + v[1]


def cheat(n, _id):
    l, c = n
    vs = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    cheats = []
    for v in vs:
        if 0 <= l + v[0] < L and 0 <= c + v[1] < C and (l + v[0], c + v[1]) in track and track[(l + v[0], c + v[1])] > _id:
            cheats.append(((l + v[0], c + v[1]), track[(l + v[0], c + v[1])]))
    return cheats


if __name__ == "__main__":
    race = open(0).read().splitlines()
    L, C = len(race), len(race[0])
    s = (None, None)
    e = (None, None)
    for l, line in enumerate(race):
        for c, value in enumerate(line):
            if value == "S":
                s = (l, c)
            elif value == "E":
                e = (l, c)

    track = {s: 0}
    n = s
    _id = 0
    while n:=next(n):
        _id += 1
        track[n] = _id

    hundred_ps_save_cheat_count = 0
    for n, _id in track.items():
        cheats = cheat(n, _id)
        for cheat_n in cheats:
            if cheat_n[1] - _id - 2 >= 100:
                hundred_ps_save_cheat_count += 1

    print(hundred_ps_save_cheat_count)





