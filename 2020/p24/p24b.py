import sys


# Actually these vectors do not fit with regular hexagonal tiles.
# Indeed if east hexagonal tile is located at (2, 0) then north-east tile is located at (1, sqrt(3)).
# But the problem remains the same with non-regular tiles which can still pave the plan.
# We can then use below integer coordinates as tiles center without loss of generality.
direction_to_vect = {
    'e': (2, 0),
    'w': (-2, 0),
    'ne': (1, 1),
    'nw': (-1, 1),
    'se': (1, -1),
    'sw': (-1, -1),
}

def parse(line):
    tile_directions = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == 'e' or c =='w':
            tile_directions.append(c)
            i += 1
        else:
            tile_directions.append(c + line[i + 1])
            i += 2
    return tile_directions


def count_arounds(coord, flipped):
    count = 0
    for vect in direction_to_vect.values():
        u, v = coord[0] + vect[0], coord[1] + vect[1]
        if (u, v) in flipped:
            count += 1
    return count


def get_adjacent_white_tiles(flipped):
    adjacent_tiles = set()
    for coord in flipped:
        for vect in direction_to_vect.values():
            u, v = coord[0] + vect[0], coord[1] + vect[1]
            adjacent_tiles.add((u, v))
    return adjacent_tiles - flipped


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    flipped = set()
    for line in lines:
        tile_directions = parse(line)
        coord = [0, 0]
        for tile_direction in tile_directions:
            x, y = direction_to_vect[tile_direction]
            coord[0], coord[1] = coord[0] + x, coord[1] + y
        if tuple(coord) in flipped:
            flipped.remove(tuple(coord))
        else:
            flipped.add(tuple(coord))

    n_days = 100
    for day in range(n_days):
        next_day_flipped = set()
        for coord in flipped:
            count = count_arounds(coord, flipped)
            if count == 1 or count == 2:
                next_day_flipped.add(coord)
        white_tiles = get_adjacent_white_tiles(flipped)
        for coord in white_tiles:
            count = count_arounds(coord, flipped)
            if count == 2:
                next_day_flipped.add(coord)
        flipped = next_day_flipped
    print(len(flipped))
