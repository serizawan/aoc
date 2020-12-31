import functools
import math
import operator
import sys


class Tile:
    def __init__(self, id, content):
        self.id = id
        self.content = content
        self.top = self.content[0]
        self.bottom = self.content[-1]
        self.left = [l[0] for l in content]
        self.right = [l[-1] for l in content]
        self.borders = [self.top, self.bottom, self.left, self.right]

    def count_matching_borders(self, tile):
        count = 0
        for self_border in self.borders:
            for tile_border in tile.borders:
                if self_border == tile_border or list(reversed(self_border)) == tile_border:
                    count += 1
        return count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    tiles = []
    tile = None
    for line in lines:
        if 'Tile' in line:
            # Remove the ':' at the end of the tile id
            tile_id = line.split(' ')[1][:-1]
            content = []
        elif line == '':
            tile = Tile(tile_id, content)
            tiles.append(tile)
        else:
            content.append(list(line))

    size = math.sqrt(len(tiles))

    matching_tiles = []
    for i, tile_i in enumerate(tiles):
        count_matching_tiles = 0
        for tile_j in (tiles[:i] + tiles[i+1:]):
            count_matching_borders = tile_i.count_matching_borders(tile_j)
            if count_matching_borders >= 1:
                count_matching_tiles += 1
        matching_tiles.append(count_matching_tiles)

    edges = [int(tiles[i].id) for i, matching_tiles_count in enumerate(matching_tiles) if matching_tiles_count == 2]
    print(functools.reduce(operator.mul, edges))
