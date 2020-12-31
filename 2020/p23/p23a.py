import sys


if __name__ == "__main__":
    # Sample:
    # cups = [int(i) for i in list('389125467')]
    cups = [int(i) for i in list('364289715')]

    cup_idx = 0
    n_moves = 100
    for i in range(n_moves):
        cup = cups[cup_idx]
        picked = []
        for j in range(3):
            picked.append(cups.pop((cup_idx + 1) % len(cups)))
            cup_idx = cups.index(cup)
        dest = cup - 1 if cup > 1 else max(cups)
        while dest in picked:
            dest = dest - 1 if dest > 1 else max(cups)
        dest_idx = cups.index(dest)
        for p in reversed(picked):
            cups.insert(dest_idx + 1, p)
        cup_idx = (cups.index(cup) + 1) % len(cups)
    idx_1 = cups.index(1)
    res = []
    for i in range(1, len(cups)):
        res.append(str(cups[(idx_1 + i) % len(cups)]))
    print(''.join(res))
