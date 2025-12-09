if __name__ == "__main__":
    tiles = [[int(i) for i in l.split(",")] for l in open(0).read().splitlines()]
    max_area = 0
    for t1 in tiles:
        for t2 in tiles:
            max_area = max(max_area, (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1))

    print(max_area)
