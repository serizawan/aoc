import sys


SCORE_MAPPING = {
    "A": 1,
    "B": 2,
    "C": 3
}


def vs(opponent_hand, result):
    if result == "Y":
        return SCORE_MAPPING[opponent_hand] + 3
    if result == "X":
        if opponent_hand == "A":
            return 0 + SCORE_MAPPING["C"]
        if opponent_hand == "B":
            return 0 + SCORE_MAPPING["A"]
        if opponent_hand == "C":
            return 0 + SCORE_MAPPING["B"]
    if result == "Z":
        if opponent_hand == "A":
            return 6 + SCORE_MAPPING["B"]
        if opponent_hand == "B":
            return 6 + SCORE_MAPPING["C"]
        if opponent_hand == "C":
            return 6 + SCORE_MAPPING["A"]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    score = 0
    for line in lines:
        opponent_hand, result = line.split(" ")
        score += vs(opponent_hand, result)

    print(score)
