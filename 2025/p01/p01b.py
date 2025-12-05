if __name__ == "__main__":
    instructions = open(0).read().splitlines()
    count = 50
    m = 100
    zeroes = 0
    for instruction in instructions:
        d, c = instruction[0], int(instruction[1:])
        if d == "L":
            zeroes += abs(count - c) // m
            if count and count - c <= 0:
                zeroes += 1
            count -= c
        elif d == "R":
            zeroes += (count + c) // m
            count += c
        count %= m

    print(zeroes)