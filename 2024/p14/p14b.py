import re


if __name__ == "__main__":
    L, C = 103, 101
    robots = open(0).read().splitlines()
    robots = [[int(i) for i in re.findall(r'[-]?\d+', robot)] for robot in robots]
    robots_init = [robot[:] for robot in robots]
    vs = [(i, j) for i in range(3) for j in range(3)]
    easter_egg = False
    s = 1
    while True:
        top_left_c, top_right_c, bottom_left_c, bottom_right_c = 0, 0, 0, 0
        for robot in robots:
            robot[0], robot[1] = (robot[0] + s * robot[2]) % C, (robot[1] + s * robot[3])  % L

        tiles = [list('.' * C) for i in range(L)]

        for robot in robots:
            tiles[robot[1]][robot[0]] = "1" if tiles[robot[1]][robot[0]] == "." else str(int(tiles[robot[1]][robot[0]]) + 1)

        for i in range(2, L - 2):
            for j in range(2, C - 2):
                if all([tiles[i + v[0]][j + v[1]] == "1" for v in vs]):
                    easter_egg = True

        if easter_egg:
            # print("\n".join(["".join(l) for l in tiles]))
            print(s)
            break

        # Robots have reached their initial positions which means the loop cycle is completed.
        if robots == robots_init:
            break

        robots = [robot[:] for robot in robots_init]
        s += 1
