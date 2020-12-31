import functools
import math
import operator
import sys


# Note: The script does only work on the 21.txt (and not on the samplea.txt) since assembling the top left corner is "hand-made".
# Indeed the right flips and rotations have been crafter by visually looking at the top left three tiles (see line 160)
# It can though be adapted by making the same analysis on samplea.txt.


class Tile:
    def __init__(self, id, content):
        self.id = id
        self.content = content

    def __str__(self):
        s = "Tile: {}\n".format(self.id)
        for line in self.content:
            s += ''.join(line) + '\n'
        return s

    @property
    def top(self):
        return self.content[0]

    @property
    def bottom(self):
        return self.content[-1]

    @property
    def left(self):
        return [l[0] for l in self.content]

    @property
    def right(self):
        return [l[-1] for l in self.content]

    @property
    def borders(self):
        return [self.top, self.bottom, self.left, self.right]

    def flip_left_right(self):
        flipped = []
        for line in self.content:
            flipped.append(list(reversed(line)))
        self.content = flipped
        return self

    def flip_up_down(self):
        flipped = []
        for line in self.content:
            flipped.insert(0, line)
        self.content = flipped
        return self

    def rotate_90_clockwise(self):
        rotated = [['' for i in range(len(line))] for line in self.content]
        for i, line in enumerate(self.content):
            for j, value in enumerate(line):
                rotated[j][-1 - i] = value
        self.content = rotated
        return self

    def count_matching_borders(self, tile):
        count = 0
        for self_border in self.borders:
            for tile_border in tile.borders:
                if self_border == tile_border or list(reversed(self_border)) == tile_border:
                    count += 1
        return count

    def match_bottom(self, tile):
        # Check top/bottom matching and rotate if False
        for i in range(4):
            if self.bottom == tile.top:
                return True
            tile.rotate_90_clockwise()
        return False

    def match_right(self, tile):
        # Check right/left matching and rotate if False
        for i in range(4):
            if self.right == tile.left:
                return True
            tile.rotate_90_clockwise()
        return False


def is_sm(i, j, sea_monster, assembled_image):
    for x in range(len(sea_monster)):
        for y in range(len(sea_monster[0])):
            if sea_monster[x][y] == '#' and not (assembled_image[i + x][j + y] == '#' or assembled_image[i + x][j + y] == 'O'):
                return False
    return True


def tag_sm(i, j, sea_monster, assembled_image):
    for x in range(len(sea_monster)):
        for y in range(len(sea_monster[0])):
            if sea_monster[x][y] == '#':
                assembled_image[i + x][j + y] = 'O'


def count_sm(sea_monster, assembled_image):
    assembled_img_size = len(assembled_image)
    count_sm = 0
    for i in range(assembled_img_size - len(sea_monster) + 1):
        for j in range(assembled_img_size - len(sea_monster[0]) + 1):
            is_sm_i_j = is_sm(i, j, sea_monster, assembled_image)
            if is_sm_i_j:
                tag_sm(i, j, sea_monster, assembled_image)
                count_sm += 1
    return count_sm

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

    size = int(math.sqrt(len(tiles)))

    matching_tiles = []
    for i, tile_i in enumerate(tiles):
        count_matching_tiles = 0
        for tile_j in (tiles[:i] + tiles[i+1:]):
            count_matching_borders = tile_i.count_matching_borders(tile_j)
            if count_matching_borders >= 1:
                count_matching_tiles += 1
        matching_tiles.append(count_matching_tiles)

    edges = [tiles[i] for i, matching_tiles_count in enumerate(matching_tiles) if matching_tiles_count == 2]
    image = [[None for j in range(size)] for i in range(size)]

    # First build the top left corner (edge tile, right edge tile, bottom edge tile)
    top_left_tile = edges[0]
    tiles = [tile for tile in tiles if tile.id != top_left_tile.id]
    matching_top_left = [tile for tile in tiles if top_left_tile.count_matching_borders(tile) > 0]

    print("TL, TLB, TLR:")
    print(top_left_tile)
    print(matching_top_left[0])
    print(matching_top_left[1])

    # By looking at above printings, tiles can be rotated/flipped to build the top left corner
    matching_top_left[0].flip_left_right().rotate_90_clockwise()
    matching_top_left[1].flip_up_down()

    # Print top left corner tiles (top left, top left right, top left bottom)
    print("TL, TLB, TLR after flips/rotations:")
    print(top_left_tile)
    print(matching_top_left[0])
    print(matching_top_left[1])

    image[0][0] = top_left_tile
    image[0][1] = matching_top_left[1]
    image[1][0] = matching_top_left[0]

    tiles = [tile for tile in tiles if tile.id != image[0][1].id and tile.id != image[1][0].id]

    # Build the image first column
    for i in range(2, size):
        top_tile = image[i - 1][0]
        bottom_tile = None
        for tile in tiles:
            if top_tile.match_bottom(tile) or top_tile.match_bottom(tile.flip_up_down()):
                bottom_tile = tile
                image[i][0] = bottom_tile
                break
        tiles = [tile for tile in tiles if tile.id != bottom_tile.id]

    # Print the image first column
    # print("Image first column:")
    # for line in image:
    #    print(line[0])

    # Build every line
    # Put top left "1st line, 2nd column" tile back in the list to have generic code
    tiles.append(image[0][1])
    for i in range(size):
        for j in range(1, size):
            left_tile = image[i][j - 1]
            right_tile = None
            for tile in tiles:
                if left_tile.match_right(tile) or left_tile.match_right(tile.flip_left_right()):
                    right_tile = tile
                    image[i][j] = right_tile
                    break
            tiles = [tile for tile in tiles if tile.id != right_tile.id]

    # Print image tiles ids
    for i in range(size):
        print(' '.join([tile.id for tile in image[i]]))
    print()

    # Assemble the image
    assembled_image = []
    for i in range(size):
        # Remove top and bottom borders of each content
        for j in range(1, len(image[0][0].content) - 1):
            image_line = []
            for k in range(size):
                # Remove left and right borders of each content
                image_line = image_line + image[i][k].content[j][1:-1]
            assembled_image.append(image_line)

    # Print assembled image
    for assembled_image_line in assembled_image:
        print(''.join(assembled_image_line))

    sea_monster = [
        list('                  # '),
        list('#    ##    ##    ###'),
        list(' #  #  #  #  #  #   '),
    ]

    # Put assembled image in tile to used corresponding methods
    assembled_image_tile = Tile("0", assembled_image)
    for i in range(4):
        count = count_sm(sea_monster, assembled_image_tile.content)
        if count:
            print(assembled_image_tile)
            break
        assembled_image_tile.rotate_90_clockwise()

    print(''.join([''.join(line) for line in assembled_image_tile.content]).count('#'))

    # Don't need to flip the image since sea monsters are detected by the above loop
    # assembled_image_tile.flip_left_right()
    # for i in range(4):
    #    count = count_sm(sea_monster, assembled_image_tile.content)
    #    if count:
    #        break
    #    assembled_image_tile.rotate_90_clockwise()
