import sys


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

    # outlet is 0 jolt
    previous_v = 0
    one_jolt_diff = 0
    three_jolt_diff = 0
    # Computed just by curiosity
    two_jolt_diff = 0
    for v in l:
        if v - previous_v == 1:
            one_jolt_diff += 1
        elif v - previous_v == 3:
            three_jolt_diff += 1
        else:
            two_jolt_diff += 1
            continue
        previous_v = v

    # By curiosity
    # print(two_jolt_diff)
    print(one_jolt_diff * three_jolt_diff)
