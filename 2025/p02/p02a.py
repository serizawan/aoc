if __name__ == "__main__":
    ranges = open(0).read().splitlines()[0].split(",")
    repeat_sum = 0
    for r in ranges:
        start, stop = [int(i) for i in r.split("-")]
        for i in range(start, stop + 1):
            li = len(str(i))
            if li % 2 == 0 and i // (10 ** (li // 2)) == (i % (10 ** (li // 2))):
                repeat_sum += i
    print(repeat_sum)
