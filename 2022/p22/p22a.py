import re


def next_p(p, v_i):
    p = ((p[0] + vs[v_i][0]) % L, (p[1] + vs[v_i][1]) % C)
    while map[p[0]][p[1]] not in ".#":
        p = ((p[0] + vs[v_i][0]) % L, (p[1] + vs[v_i][1]) % C)
    return p

if __name__ == "__main__":
    in_lines = open(0).read().splitlines()
    path = in_lines[-1]
    map = in_lines[:-2]
    L, C = len(map), max(len(line) for line in map)
    # Pad lines with " " to make them the same length.
    map = [line + " " * (C - len(line)) for line in map]
    p = (0, map[0].index("."))
    vs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up (Clockwise order).
    v_i = 0
    path = re.split(r"(L|R)", path)
    path = [int(item) if item != "L" and item != "R" else item for item in path]
    for action in path:
        if action == "L":
            v_i = (v_i - 1) % len(vs)
        elif action == "R":
            v_i = (v_i + 1) % len(vs)
        else:
            steps = 0
            while steps != action and map[next_p(p, v_i)[0]][next_p(p, v_i)[1]] == ".":
                p = next_p(p, v_i)
                steps += 1

    # Row and Column indexes start at 1.
    p = (p[0] + 1, p[1] + 1)

    pwd_line_mul = 1000
    pwd_col_mul = 4
    pwd_vec_mul = 1

    print(pwd_line_mul * p[0] + pwd_col_mul * p[1] + pwd_vec_mul * v_i)