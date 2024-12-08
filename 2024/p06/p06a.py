if __name__ == "__main__":
    map = open(0).read().splitlines()
    map = [list(line) for line in map]
    L = len(map)
    C = len(map[0])
    g = [0, 0]
    for l in range(L):
        for c in range(C):
            if map[l][c] == "^":
                g = [l, c]
                map[l][c] = "X"

    vs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up (Clockwise order)
    v_i = 3

    while 0 <= g[0] < L and 0 <= g[1] < C:
        next_g = [g[0] + vs[v_i][0], g[1] + vs[v_i][1]]
        if not (0 <= next_g[0] < L) or not (0 <= next_g[1] < C):
            g = next_g
        elif map[next_g[0]][next_g[1]] in ".X":
            g = next_g
            map[g[0]][g[1]] = "X"
        else:
            v_i = (v_i + 1) % len(vs)

    count = 0
    for l in map:
        for c in l:
            if c == "X":
                count += 1

    for line in map:
        print(''.join(line))
    print(count)


