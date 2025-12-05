if __name__ == "__main__":
    instructions = open(0).read().splitlines()
    count = 50
    m = 100
    zeroes = 0
    for instruction in instructions:
        d, c = instruction[0], int(instruction[1:])
        if d == "L":
            count -= c
        elif d == "R":
            count += c
        count %= m
        if count == 0:
            zeroes += 1

    print(zeroes)