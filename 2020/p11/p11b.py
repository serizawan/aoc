import copy
import sys


def count_around_occupied(l, i, j):
    occupied = []
    directions = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if i != 0 or j != 0]
    for direction in directions:
        is_occ = False
        u, v = direction
        while 0 <= i + u and i + u < len(l) and 0 <= j + v and j + v < len(l[i]) and not is_occ and l[i + u][j + v] != 'L':
            if l[i + u][j + v] == '#':
                is_occ = True
            u += direction[0]
            v += direction[1]
        occupied.append(is_occ)
    return occupied.count(True)


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
                elif seats[i][j] == '#' and count >= 5:
                    seats_next[i][j] = 'L'
                    changes += 1
                else:
                    continue
        seats = seats_next

seats_as_str = ''.join([''.join(row) for row in seats])
print(seats_as_str.count('#'))
