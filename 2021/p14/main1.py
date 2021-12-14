from collections import defaultdict
import sys


STEPS = 10


def parse(filename) -> (defaultdict[str, int], defaultdict[str, int], dict[str, str]):
    with open(filename) as f:
        lines = f.read().splitlines()

    template = lines[0]
    letters = defaultdict(int)
    for letter in template:
        letters[letter] += 1

    pairs = defaultdict(int)
    for i in range(len(template) - 1):
        pair = template[i] + template[i+1]
        pairs[pair] += 1

    mapper = {}
    for line in lines[2:]:
        pair, insert = line.split(' -> ')
        mapper[pair] = insert

    return letters, pairs, mapper


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr);
        sys.exit();

    letters, pairs, mapper = parse(sys.argv[1])

    for step in range(STEPS):
        next_pairs = defaultdict(int)
        for pair, count in pairs.items():
            letters[mapper[pair]] += count
            next_pairs[pair[0] + mapper[pair]] += count
            next_pairs[mapper[pair] + pair[1]] += count
        pairs = next_pairs

    print(max(letters.values()) - min(letters.values()))


if __name__ == "__main__":
    run()
