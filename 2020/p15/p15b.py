import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    starting_numbers = [int(i) for i in lines[0].split(',')]
    last_last_spoken = starting_numbers[-2]
    last_spoken = starting_numbers[-1]
    spokens = {int(i): idx + 1 for idx, i in enumerate(starting_numbers)}
    start = len(spokens)
    stop = 30000000
    for i in range(start, stop):
        spokens[last_last_spoken] = i - 1
        last_last_spoken = last_spoken
        if last_spoken not in spokens:
            last_spoken = 0
        else:
            last_spoken = i - spokens[last_spoken]
    print(last_spoken)
