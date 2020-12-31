from functools import reduce
import sys


def extended_euclidean_alg(r1, u1, v1, r2, u2, v2):
    if r2 == 0:
        return (r1, u1, v1)
    return extended_euclidean_alg(r2, u2, v2, r1 - (r1 // r2) * r2, u1 - (r1 // r2) * u2, v1 - (r1 // r2) * v2)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    bus_ids = [int(i) for i in l[1].split(',') if i != 'x']
    gaps = [i for i in range(len(l[1].split(','))) if l[1].split(',')[i] != 'x']

    bus_ids_prod = reduce((lambda x, y: x * y), bus_ids)

    ts = 0
    # Solved by using the chinese remainder theorem
    for i, bus_id in enumerate(bus_ids):
        r, u, v = extended_euclidean_alg(bus_ids_prod // bus_id, 1, 0, bus_id, 0, 1)
        ts += (bus_id - gaps[i]) * (u * bus_ids_prod // bus_id)

    while ts < 0:
        ts += bus_ids_prod

    print(ts)
