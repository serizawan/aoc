import sys


OPENINGS_TO_CLOSINGS = {'(': ')', '[': ']', '{': '}', '<': '>'}
SCORES = {')': 1, ']': 2, '}': 3, '>': 4}


def is_corrupted(line: str) -> (bool, str):
    stack = []
    for c in line:
        if c in OPENINGS_TO_CLOSINGS.keys():
            stack.append(c)
        elif c in OPENINGS_TO_CLOSINGS.values() and OPENINGS_TO_CLOSINGS[stack.pop()] != c:
            # True and first wrong char
            return True, c
    # False and remaining stack
    return False, stack


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    scores = []
    for line in lines:
        b, s = is_corrupted(line)
        if not b:
            score = 0
            for c in s[::-1]:
                score *= 5
                score += SCORES[OPENINGS_TO_CLOSINGS[c]]
            scores.append(score)

    print(sorted(scores)[len(scores) // 2])


if __name__ == "__main__":
    run()