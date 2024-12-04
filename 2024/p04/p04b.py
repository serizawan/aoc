def is_xmas(l, c):
    xmas = "XMAS"
    if xmas_lines[l][c] == "A" and (1 <= l < L - 1) and (1 <= c < C - 1):
        d1 = xmas_lines[l + 1][c + 1] + xmas_lines[l - 1][c - 1] in ("MS", "SM")
        d2 = xmas_lines[l + 1][c - 1] + xmas_lines[l - 1][c + 1] in ("MS", "SM")
        if d1 and d2:
            return True
    return False


if __name__ == "__main__":
    xmas_lines = open(0).read().splitlines()
    L = len(xmas_lines)
    C = len(xmas_lines[0])

    total_xmas_count = 0
    for l in range(L):
        for c in range(C):
            total_xmas_count += 1 if is_xmas(l, c) else 0

    print(total_xmas_count)