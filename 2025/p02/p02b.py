def has_repeat_pattern(n):
    ln = len(str(n))
    for i in range(1, ln // 2 + 1):
        if ln % i == 0:
            n_i = n
            k = n % (10 ** i)
            while n_i and n_i % (10 ** i) == k:
                n_i //= (10 ** i)
            if not n_i:
                return True
    return False

if __name__ == "__main__":
    ranges = open(0).read().splitlines()[0].split(",")
    repeat_sum = 0
    for r in ranges:
        start, stop = [int(i) for i in r.split("-")]
        for i in range(start, stop + 1):
            if has_repeat_pattern(i):
                repeat_sum += i
    print(repeat_sum)
