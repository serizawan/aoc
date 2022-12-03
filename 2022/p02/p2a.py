from enum import Enum
import sys


ELF_MAPPING = {
    "A": "ROCK",
    "B": "PAPER",
    "C": "SCISSORS"
}

MY_MAPPING = {
    "X": "ROCK",
    "Y": "PAPER",
    "Z": "SCISSORS"
}


class Game(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def __lt__(self, other):
        winner1 = self == Game.ROCK and other == Game.PAPER
        winner2 = self == Game.PAPER and other == Game.SCISSORS
        winner3 = self == Game.SCISSORS and other == Game.ROCK
        return winner1 or winner2 or winner3


def vs(opponent_hand, my_hand):
    win_score = 6
    draw_score = 3
    loose_score = 0
    total_score = my_hand.value
    if opponent_hand < my_hand:
        return total_score + win_score
    if opponent_hand > my_hand:
        return total_score + loose_score
    return total_score + draw_score


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    score = 0
    for line in lines:
        opponent_hand, my_hand = line.split(" ")
        opponent_hand, my_hand = Game[ELF_MAPPING[opponent_hand]], Game[MY_MAPPING[my_hand]]
        score += vs(opponent_hand, my_hand)

    print(score)
