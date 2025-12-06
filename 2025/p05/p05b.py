if __name__ == "__main__":
    my_in = open(0).read().splitlines()
    sep = my_in.index("")
    ranges = list([tuple(int(i) for i in r.split("-")) for r in my_in[:sep]])
    ranges.sort(key=lambda x: x[0])
    can_merge = True
    while can_merge:
        i = 0
        lr = len(ranges)
        while i < lr - 1:
            if ranges[i][1] >= ranges[i + 1][0]:
                ranges[i] = (ranges[i][0], max(ranges[i][1], ranges[i + 1][1]))
                ranges = ranges[:i + 1] + ranges[i + 2:]
                break
            i += 1
        if i == lr - 1:
            can_merge = False

    freshable_count = 0
    for r in ranges:
        freshable_count += r[1] - r[0] + 1

    print(freshable_count)

