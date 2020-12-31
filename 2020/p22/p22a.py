import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    mid = len(lines) // 2
    p1 = [int(line) for line in lines[1:mid]]
    p2 = [int(line) for line in lines[mid + 2:]]

    while p1 and p2:
        if (top1 := p1.pop(0)) > (top2 := p2.pop(0)):
            p1 += [top1, top2]
        else:
            p2 += [top2, top1]

    winner = p1 if len(p1) else p2
    score = sum([(i + 1) * value for i, value in enumerate(reversed(winner))])
    print(score)
