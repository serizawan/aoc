from __future__ import annotations
import logging


BOARD_LEN = 10
DICE_SIDE_NB = 3
N_ROLLS = 3
WIN_SCORE = 21
TOTAL_ROLLS_AND_UNIVERSES_COUNT = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]


def count_wins(p1_pos, p2_pos, p1_score, p2_score, p_turn):
    if p1_score >= WIN_SCORE or p2_score >= WIN_SCORE:
        if p1_score > p2_score:
            return 1, 0
        else:
            return 0, 1

    p1_wins_count, p2_wins_count = 0, 0
    for (total_rolls, universes_count) in TOTAL_ROLLS_AND_UNIVERSES_COUNT:
        p1_pos_copy, p2_pos_copy = p1_pos, p2_pos
        p1_score_copy, p2_score_copy = p1_score, p2_score
        if p_turn == 1:
            if p1_pos + total_rolls == BOARD_LEN:
                p1_pos = BOARD_LEN
            else:
                p1_pos = (p1_pos + total_rolls) % BOARD_LEN
            p1_score += p1_pos
        else:
            if p2_pos + total_rolls == BOARD_LEN:
                p2_pos = BOARD_LEN
            else:
                p2_pos = (p2_pos + total_rolls) % BOARD_LEN
            p2_score += p2_pos
        p1_wins_inc, p2_wins_inc = count_wins(p1_pos, p2_pos, p1_score, p2_score, p_turn % 2 + 1)
        p1_wins_count += universes_count * p1_wins_inc
        p2_wins_count += universes_count * p2_wins_inc
        p1_pos, p2_pos = p1_pos_copy, p2_pos_copy
        p1_score, p2_score = p1_score_copy, p2_score_copy
    return p1_wins_count, p2_wins_count


def run() -> None:
    # p1_pos, p2_pos = 4, 8
    p1_pos, p2_pos = 1, 10
    p1_score, p2_score = 0, 0
    p_turn = 1
    p1_wins_count, p2_wins_count = count_wins(p1_pos, p2_pos, p1_score, p2_score, p_turn)
    print(max(p1_wins_count, p2_wins_count))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
