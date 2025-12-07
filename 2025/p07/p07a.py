if __name__ == "__main__":
    map = open(0).read().splitlines()
    splits = 0
    s_indexes = {map[0].index("S")}
    for line in map[1:]:
        next_s_indexes = set()
        for s_index in s_indexes:
            if line[s_index] == "^":
                splits += 1
                next_s_indexes.add(s_index - 1)
                next_s_indexes.add(s_index + 1)
            else:
                next_s_indexes.add(s_index)

        s_indexes = next_s_indexes
    print(splits)

    from collections import defaultdict

    if __name__ == "__main__":
        map = open(0).read().splitlines()
        splits = 0
        s_indexes = {map[0].index("S"): 1}
        for line in map[1:]:
            next_s_indexes = defaultdict(int)
            for s_index in s_indexes:
                if line[s_index] == "^":
                    splits += 1
                    next_s_indexes[s_index - 1] += s_indexes[s_index]
                    next_s_indexes[s_index + 1] += s_indexes[s_index]
                else:
                    next_s_indexes.add(s_index)
            s_indexes = next_s_indexes

        print(splits)