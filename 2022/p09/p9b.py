from enum import Enum
import math
import sys


N_KNOTS = 10


class Direction(Enum):
    L = (0, -1)
    R = (0, 1)
    U = (1, 0)
    D = (-1, 0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Missing input file. Run with: python {sys.argv[0]} [FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    visited_pos = set()
    rope_positions = [[0, 0] for i in range(N_KNOTS)]
    visited_pos.add(tuple(rope_positions[0]))
    for line in lines:
        direction, n_steps = line.split(" ")
        direction = Direction[direction]
        n_steps = int(n_steps)
        for i in range(n_steps):
            h_pos = rope_positions[0]
            h_pos[0], h_pos[1] = h_pos[0] + direction.value[0], h_pos[1] + direction.value[1]
            for t_pos in rope_positions[1:]:
                ht_vec = (h_pos[0] - t_pos[0], h_pos[1] - t_pos[1])
                abs_ht_vec = (abs(ht_vec[0]), abs(ht_vec[1]))
                t_pos[0] = t_pos[0] + math.copysign(abs_ht_vec[0] // 2, ht_vec[0])
                t_pos[1] = t_pos[1] + math.copysign(abs_ht_vec[1] // 2, ht_vec[1])
                if abs_ht_vec == (1, 2):
                    t_pos[0] += ht_vec[0]
                elif abs_ht_vec == (2, 1):
                    t_pos[1] += ht_vec[1]
                h_pos = t_pos

            visited_pos.add(tuple(rope_positions[-1]))

    print(len(visited_pos))
