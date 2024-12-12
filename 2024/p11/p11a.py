BLINKS = 25


if __name__ == "__main__":
    stones = open(0).read().split(" ")
    stones = [int(s) for s in stones]

    for i in range(BLINKS):
        next_stones = []
        for s in stones:
            if s == 0:
                next_stones.append(1)
            elif len(str(s)) % 2:
                next_stones.append(s * 2024)
            else:
                ss = str(s)
                left_s, right_s = int(ss[:len(ss) // 2]), int(ss[len(ss) // 2:])
                next_stones += [left_s, right_s]

        stones = next_stones[:]

    print(len(stones))