from __future__ import annotations
import logging


BOARD_LEN = 10
DICE_SIDE_NB = 100
N_ROLLS = 3
WIN_SCORE = 1000


def run() -> None:
    p1_pos, p2_pos = 1, 10
    p1_score, p2_score = 0, 0
    n_total_rolls = 0
    rolls = list(range(-N_ROLLS + 1, 1))
    player_turn = 1
    while p1_score < WIN_SCORE and p2_score < WIN_SCORE:
        n_total_rolls += N_ROLLS
        rolls = [dr + N_ROLLS if dr + N_ROLLS <= DICE_SIDE_NB else (dr + N_ROLLS) % DICE_SIDE_NB for dr in rolls]
        if player_turn == 1:
            if (p1_pos + sum(rolls)) % BOARD_LEN == 0:
                p1_pos = BOARD_LEN
            else:
                p1_pos = (p1_pos + sum(rolls)) % BOARD_LEN
            p1_score += p1_pos
        else:
            if (p2_pos + sum(rolls)) % BOARD_LEN == 0:
                p2_pos = BOARD_LEN
            else:
                p2_pos = (p2_pos + sum(rolls)) % BOARD_LEN
            p2_score += p2_pos
        logging.debug(f'{player_turn=}, ({p1_pos=}, {p1_score=}), ({p2_pos=}, {p2_score=}), {n_total_rolls=}')
        player_turn = (player_turn % 2) + 1
    print(min(p1_score, p2_score) * n_total_rolls)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
