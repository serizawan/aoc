from collections import defaultdict


if __name__ == "__main__":
    map = open(0).read().splitlines()
    L, C = len(map), len(map[0])
    antennas = defaultdict(list)
    for l in range(L):
        for c in range(C):
            if (item:=map[l][c]) != ".":
                antennas[item].append((l, c))

    antinodes = set()
    for antenna_id, antenna_positions in antennas.items():
        for antenna_i in antenna_positions:
            for antenna_j in antenna_positions:
                if antenna_i != antenna_j:
                    v = antenna_i[0] - antenna_j[0], antenna_i[1] - antenna_j[1]
                    antinode = antenna_i[0] + v[0], antenna_i[1] + v[1]
                    if 0 <= antinode[0] < L and 0 <= antinode[1] < C:
                        antinodes.add(antinode)

    print(len(antinodes))