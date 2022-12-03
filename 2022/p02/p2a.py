import sys


RPS_MAPPING = {
    "A": "X",
    "B": "Y",
    "C": "Z"
}

SCORE_MAPPING = {
    "X": 1,
    "Y": 2,
    "Z": 3
}


def vs(opponent_hand, my_hand):
    opponent_hand = RPS_MAPPING[opponent_hand]
    if opponent_hand == my_hand:
        return 3 + SCORE_MAPPING[my_hand]
    if opponent_hand == "X" and my_hand == "Y":
        return 6 + SCORE_MAPPING[my_hand]
    if opponent_hand == "Y" and my_hand == "X":
        return 0 + SCORE_MAPPING[my_hand]
    if opponent_hand == "Z" and my_hand == "X":
        return 6 + SCORE_MAPPING[my_hand]
    if opponent_hand == "X" and my_hand == "Z":
        return 0 + SCORE_MAPPING[my_hand]
    if opponent_hand == "Y" and my_hand == "Z":
        return 6 + SCORE_MAPPING[my_hand]
    if opponent_hand == "Z" and my_hand == "Y":
        return 0 + SCORE_MAPPING[my_hand]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    score = 0
    for line in lines:
        opponent_hand, my_hand = line.split(" ")
        score += vs(opponent_hand, my_hand)

    print(score)
