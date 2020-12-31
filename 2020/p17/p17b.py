import copy
import sys


# Vocabulary used:
# The four dimensional object is named hypercube.
# A slice of the hypercube is a three dimensional object named cube.
# A slice of the cube is a two dimensional object named a layer.
# A slice of the layer is a one dimensional object named a line.
# A slice of a layer is a zero dimensional object named an element.
# At every w, x, y, z of the hypercube an element is located.


def expand(hypercube):
    expanded_hypercube = copy.deepcopy(hypercube)
    for z, cube in enumerate(hypercube):
        for y, layer in enumerate(cube):
            for x, line in enumerate(layer):
                for w, element in enumerate(line):
                    element = get_switched_element(w, x, y, z, hypercube)
                    expanded_hypercube[z][y][x][w] = element
    return expanded_hypercube


def get_switched_element(w, x, y, z, hypercube):
    element = hypercube[z][y][x][w]
    arounds = [(i, j, k, l)
            for i in (-1, 0, 1)
            for j in (-1, 0, 1)
            for k in (-1, 0, 1)
            for l in (-1, 0, 1) if (i != 0 or j != 0 or k != 0 or l != 0)]

    count_on_around = 0
    for i, j, k,l in arounds:
        is_it_in = (
                0 <= z + l and z + l < len(hypercube) and
                0 <= y + k and y + k < len(hypercube[0]) and
                0 <= x + j and x + j < len(hypercube[0][0]) and
                0 <= w + i and w + i < len(hypercube[0][0][0])
        )
        if is_it_in and hypercube[z + l][y + k][x + j][w + i] == '#':
            count_on_around += 1

    # Stays active or activates
    if (element == '#' and count_on_around in [2, 3]) or (element == '.' and count_on_around == 3):
        return '#'
    # Stays inactive or deactivate
    else:
        return '.'


def add_border(layer):
    # First add dots at the beginning and end of each line
    for i in range(0, len(layer)):
        layer[i] = ['.'] + layer[i] + ['.']

    # Then add top and bottom '.' lines
    layer.insert(0, ['.'] * len(layer[0]))
    layer.append(['.'] * len(layer[0]))

    return layer


def add_wrapper(cube):
    # First add borders around every layer
    for layer in cube:
        add_border(layer)

    # Then add a . layer on top and bottom of the cube
    dot_layer_top = [['.'] * len(cube[0][0]) for i in range(len(cube[0]))]
    dot_layer_bottom = copy.deepcopy(dot_layer_top)
    cube.insert(0, dot_layer_top)
    cube.append(dot_layer_bottom)


def add_hyperwrapper(hypercube):
    # First add wrapper around every cube
    for cube in hypercube:
        add_wrapper(cube)

    # Then add a . cube on top and bottom of the hypercube
    dot_cube_top = [[['.'] * len(hypercube[0][0][0]) for i in range(len(hypercube[0][0]))] for j in range(len(hypercube[0]))]
    dot_cube_bottom = copy.deepcopy(dot_cube_top)
    hypercube.insert(0, dot_cube_top)
    hypercube.append(dot_cube_bottom)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    hypercube = [[[list(line) for line in l]]]
    n_rounds = 6
    for i in range(n_rounds):
        # At the beginning of each round add a . wrapper around the current global cube
        # Newly activated cubes can only be off-by-one from the previous element coordinates
        add_hyperwrapper(hypercube)
        hypercube = expand(hypercube)

    print(''.join([''.join([''.join([''.join(l) for l in layer]) for layer in cube]) for cube in hypercube]).count('#'))
