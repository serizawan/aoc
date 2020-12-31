import copy
import sys


# Vocabulary used:
# The three dimensional object is named cube.
# A slice of the cube is a two dimensional object named a layer.
# A slice of the layer is a one dimensional object named a line.
# A slice of a layer is a zero dimensional object named an element.
# At every w, x, y, z of the hypercube an element is located.


def expand(cube):
    expanded_cube = copy.deepcopy(cube)
    for z, layer in enumerate(cube):
        for y, line in enumerate(layer):
            for x, element in enumerate(line):
                element = get_switched_element(x, y, z, cube)
                expanded_cube[z][y][x] = element
    return expanded_cube


def get_switched_element(x, y, z, cube):
    element = cube[z][y][x]
    arounds = [(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1) if (i != 0 or j != 0 or k != 0)]
    count_on_around = 0
    for i, j, k in arounds:
        is_it_in = (
                0 <= z + k and z + k < len(cube) and
                0 <= y + j and y + j < len(cube[0]) and
                0 <= x + i and x + i < len(cube[0][0])
        )
        if is_it_in and cube[z + k][y + j][x + i] == '#':
            count_on_around += 1

    # Stays active or activates
    if (element == '#' and count_on_around in [2, 3]) or (element == '.' and count_on_around == 3):
        return '#'
    # Stays inactive or deactivate
    else:
        return '.'


def add_border(layer):
    # Add dots at the beginning and end of each line
    for i in range(0, len(layer)):
        layer[i] = ['.'] + layer[i] + ['.']

    # Add top and bottom '.' lines
    layer.insert(0, ['.'] * len(layer[0]))
    layer.append(['.'] * len(layer[0]))

    return layer


def add_wrapper(cube):
    # First add borders around every layer
    for layer in cube:
        add_border(layer)

    # Then add a . layer on top and bottom of the global cube
    dot_layer_top = [['.'] * len(cube[0][0]) for i in range(len(cube[0]))]
    dot_layer_bottom = dot_layer_top[:]
    cube.insert(0, dot_layer_top)
    cube.append(dot_layer_bottom)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    cube = [[list(line) for line in l]]
    n_rounds = 6
    for i in range(n_rounds):
        # At the beginning of each round add a . wrapper around the current global cube
        # Newly activated cubes can only be off-by-one from the previous element coordinates
        add_wrapper(cube)
        cube = expand(cube)

    print(''.join([''.join([''.join(l) for l in layer]) for layer in cube]).count('#'))
