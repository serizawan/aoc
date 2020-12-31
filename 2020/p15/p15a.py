import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    spokens = [int(i) for i in lines[0].split(',')]
    start = len(spokens)
    stop = 2020
    for i in range(start, stop):
        last_spoken = spokens[-1]
        if last_spoken not in spokens[:-1]:
            spokens.append(0)
        else:
            # reversed() returns an iterator which has no index method.
            last_last_spokens_age = list(reversed(spokens[:-1])).index(last_spoken) + 1
            spokens.append(last_last_spokens_age)

    print(spokens[-1])
