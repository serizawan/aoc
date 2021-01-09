import sys


def run(values, noun, verb):
    values[1], values[2] = noun, verb
    idx = 0
    while (op := values[idx]) != 99:
        if op == 1:
            values[values[idx + 3]] =  values[values[idx + 1]] + values[values[idx + 2]]
        elif op == 2:
            values[values[idx + 3]] =  values[values[idx + 1]] * values[values[idx + 2]]
        else:
            raise Exception("Wrong op value: {} (only 1, 2 and 99 are possible).".format(op))
        idx += 4
    return values[0]


def find(init):
    for n in range(100):
        for v in range(100):
            values = init[:]
            if run(values, n, v) == 19690720:
                return n, v


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    init = [int(i) for i in lines[0].split(',')]
    noun, verb = find(init)

    print(100 * noun + verb)
