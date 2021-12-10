import sys


OPENINGS_TO_CLOSINGS = {'(': ')', '[': ']', '{': '}', '<': '>'}
SCORES = {')': 3, ']': 57, '}': 1197, '>': 25137}


def is_corrupted(line):
    stack = []
    for c in line:
        if c in OPENINGS_TO_CLOSINGS.keys():
            stack.append(c)
        elif c in OPENINGS_TO_CLOSINGS.values() and OPENINGS_TO_CLOSINGS[stack.pop()] != c:
            return True, c
    return False, None


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    score = 0
    for line in lines:
        _, c = is_corrupted(line)
        score += SCORES.get(c, 0)

    print(score)


if __name__ == "__main__":
    run()