import copy
import sys


def count_around_occupied(l, i, j):
    arounds = [(u, v) for u in (i - 1, i, i + 1) for v in (j - 1, j, j + 1) if u != i or v != j]
    count = 0
    for u, v in arounds:
        if u >= 0 and u < len(l) and v >= 0 and v < len(l[u]) and l[u][v] == '#':
            count += 1
    return count


def print_seats(seats):
    for row in seats:
        print(''.join(row))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    seats = [list(r) for r in l]
    seats_next = [['.'] * len(r) for r in l]
    # -1 to enter once the main while loop
    changes = -1
    while changes:
        changes = 0
        # seats_next = seats.copy (or seats[:] or list(seats) only perform a shallow copy).
        # Inner list would still have the same references with above assignments.
        seats_next = copy.deepcopy(seats)
        for i in range(len(seats)):
            for j in range(len(seats[i])):
                count = count_around_occupied(seats, i, j)
                if seats[i][j] == 'L' and count == 0:
                    seats_next[i][j] = '#'
                    changes += 1
                elif seats[i][j] == '#' and count >= 4:
                    seats_next[i][j] = 'L'
                    changes += 1
                else:
                    continue
        seats = seats_next

seats_as_str = ''.join([''.join(row) for row in seats])
print(seats_as_str.count('#'))
