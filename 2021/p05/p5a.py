import sys


def run():
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    us, vs = [], []
    for line in lines:
        u, v = line.split(' -> ')
        u, v = [int(i) for i in u.split(',')], [int(j) for j in v.split(',')]
        if u[0] == v[0] or u[1] == v[1]:
            us.append(u)
            vs.append(v)

    assert len(us) == len(vs)

    max_ux, max_uy = max(us, key=lambda item: item[0])[0], max(us, key=lambda item: item[1])[1]
    max_vx, max_vy = max(vs, key=lambda item: item[0])[0], max(vs, key=lambda item: item[1])[1]

    diagram = [[0] * (max(max_uy, max_vy) + 1) for _ in range(max(max_ux, max_vx) + 1)]

    for u, v in zip(us, vs):
        uv = v[0] - u[0], v[1] - u[1]
        norm = abs(uv[0] + uv[1])
        direction = uv[0] // norm, uv[1] // norm

        for i in range(norm + 1):
            diagram[u[0] + direction[0] * i][u[1] + direction[1] * i] += 1

    count = 0
    for line in diagram:
        for value in line:
            if value >= 2:
                count += 1
    return count


if __name__ == "__main__":
    print(run())
