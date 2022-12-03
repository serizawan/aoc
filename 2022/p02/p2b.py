from enum import Enum
import sys


ELF_MAPPING = {
    "A": "ROCK",
    "B": "PAPER",
    "C": "SCISSORS"
}

RESULT_MAPPING = {
    "X": "LOOSE",
    "Y": "DRAW",
    "Z": "WIN"
}


class Result(Enum):
    LOOSE = 0
    DRAW = 3
    WIN = 6


class Game(Enum):
    # Value, Win against, Lose against
    ROCK = (1, "SCISSORS", "PAPER")
    PAPER = (2, "ROCK", "SCISSORS")
    SCISSORS = (3, "PAPER", "ROCK")


def vs(opponent_hand, result):
    if result == Result.DRAW:
        return opponent_hand.value[0] + Result.DRAW.value
    if result == Result.LOOSE:
        my_hand = Game[opponent_hand.value[1]]
        return my_hand.value[0] + Result.LOOSE.value
    my_hand = Game[opponent_hand.value[2]]
    return my_hand.value[0] + Result.WIN.value


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    score = 0
    for line in lines:
        opponent_hand, result = line.split(" ")
        score += vs(Game[ELF_MAPPING[opponent_hand]], Result[RESULT_MAPPING[result]])

    print(score)
