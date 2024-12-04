def xmas_count(l, c):
    xmas = "XMAS"
    vs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    count = 0
    for v in vs:
        is_xmas = True
        for i in range(len(xmas)):
            if not(0 <= l + v[0] * i < L) or not(0 <= c + v[1] * i < C) or xmas_lines[l + v[0] * i][c + v[1] * i] != xmas[i]:
                is_xmas = False
        if is_xmas:
            count += 1
    return count


if __name__ == "__main__":
    xmas_lines = open(0).read().splitlines()
    L = len(xmas_lines)
    C = len(xmas_lines[0])

    total_xmas_count = 0
    for l in range(L):
        for c in range(C):
            total_xmas_count += xmas_count(l, c)

    print(total_xmas_count)