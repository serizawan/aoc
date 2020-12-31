import sys


def pop_until_3_jolts_gap(l):
    n_popped = 0
    # Pop encountered consecutive 1-jolt gaps and count them
    while (l[1] - l[0] == 1):
        l.pop(0)
        n_popped += 1

    # Pop encountered consecutive 3-jolts gaps
    while (len(l) > 1 and l[1] - l[0] == 3):
        l.pop(0)

    # Pop last link of the 3-jolts gaps chain
    l.pop(0)
    return n_popped


def compute_arrangements_of_n_one_jolts(n):
    # Note that in the input file there is never more than 3 consecutives adapters separated by 1-jolt gaps on both sides.
    # Hence we don't need to implement a function that can compute the arrangements for any n.
    if n == 0:
        return 1
    if n == 1:
        return 2
    if n == 2:
        return 4
    if n == 3:
        return 7


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    l = [int(r) for r in l]
    l.sort()

    # Personal device adapter
    l.append(l[-1] + 3)

    arrangements = 1
    while l:
        n_popped = pop_until_3_jolts_gap(l)
        arrangements *= compute_arrangements_of_n_one_jolts(n_popped)

    print(arrangements)
