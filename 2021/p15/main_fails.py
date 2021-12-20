from copy import deepcopy
import sys


# This solution script explores only paths with moves RIGHT or DOWN.
# Despite it finds the right solution for the example.in input, it fails to find the correct one for data.in input.
# In some situations, it is more optimal to go UP or LEFT (move around areas even if it moves away from end)
# because it has a lower cost.
# Example:
# 1 9 1 1 1
# 1 1 1 9 1
# 9 9 9 9 1
#
# 1 paths (with UP moves) is cheaper than using only RIGHT or DOWN moves (and cross "9"s cells)
#
# This script has a O(h * w) complexity.


def parse(filename) -> list[list[int]]:
    with open(filename) as f:
        lines = f.read().splitlines()

    matrix = []
    for line in lines:
        matrix_line = [int(i) for i in line]
        matrix.append(matrix_line)
    return matrix


def expand(matrix):
    expand_factor = 5
    expanded_matrix_x = []
    for line in matrix:
        expanded_line = line[:]
        for j in range(1, expand_factor):
            expanded_line += [v + j if v + j <= 9 else (v + j) % 9 for v in line]
        expanded_matrix_x.append(expanded_line)

    expanded_matrix = deepcopy(expanded_matrix_x)
    for i in range(1, expand_factor):
        inc_expanded_matrix_x = []
        for expanded_line_x in expanded_matrix_x:
            inc_expanded_line_x = [v + i if v + i <= 9 else (v + i) % 9 for v in expanded_line_x]
            inc_expanded_matrix_x.append(inc_expanded_line_x)
        expanded_matrix += inc_expanded_matrix_x

    for line in expanded_matrix:
        print(''.join([str(v) for v in line]))

    return expanded_matrix


def compute_sum(matrix: list[list[int]]) -> list[list[int]]:
    h, w = len(matrix), len(matrix[0])
    line_sum = [matrix[0][0]]
    column_sum = [matrix[0][0]]
    for i in range(1, w):
        line_sum.append(line_sum[i - 1] + matrix[0][i])

    matrix_sum = [line_sum]

    for j in range(1, h):
        column_sum.append(column_sum[j - 1] + matrix[j][0])

    for v in column_sum[1:]:
        matrix_sum.append([v])

    for i in range(1, h):
        for j in range(1, w):
            matrix_sum[i].append(min(matrix_sum[i-1][j], matrix_sum[i][j-1]) + matrix[i][j])

    return matrix_sum


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr);
        sys.exit()

    matrix = parse(sys.argv[1])
    # Un-comment
    # matrix = expand(matrix)
    matrix_sum = compute_sum(matrix)
    print(matrix_sum[-1][-1] - matrix[0][0])


if __name__ == "__main__":
    run()
