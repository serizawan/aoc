from collections import defaultdict


BLINKS = 75
if __name__ == "__main__":
    stones = open(0).read().split(" ")
    stones = [int(s) for s in stones]
    stones_counts = defaultdict(int)
    for s in stones:
        stones_counts[s] += 1

    for i in range(BLINKS):
        next_stones_counts = defaultdict(int)
        for s, c in stones_counts.items():
            if s == 0:
                next_stones_counts[1] += c
            elif len(str(s)) % 2:
                next_stones_counts[s * 2024] += c
            else:
                ss = str(s)
                left_s, right_s = int(ss[:len(ss) // 2]), int(ss[len(ss) // 2:])
                next_stones_counts[left_s] += c
                next_stones_counts[right_s] += c

        stones_counts = dict(next_stones_counts)

    print(sum(stones_counts.values()))