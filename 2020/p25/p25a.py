import sys


def transform(value, subject):
    d = 20201227
    return (value * subject) % d


def encrypt(public_key, loop_size):
    res = 1
    for i in range(loop_size):
        res = transform(res, public_key)
    return res


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    card_pk = int(lines[0])
    door_pk = int(lines[1])

    card_loop_cand = 1
    card_ls = None
    value = 1
    public_subject = 7
    while not card_ls:
        if (value := transform(value, public_subject)) == card_pk:
            card_ls = card_loop_cand
        card_loop_cand += 1

    print(encrypt(door_pk, card_ls))
