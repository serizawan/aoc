if __name__ == "__main__":
    encrypted_file = []
    for line in open(0).read().splitlines():
        encrypted_file.append(int(line))

    mixed_positions = list(range(len(encrypted_file)))
    mixed_file = encrypted_file[:]

    for initial_pos in range(len(encrypted_file)):
        value = encrypted_file[initial_pos]
        move = value % (len(encrypted_file) - 1)
        current_pos = mixed_positions.index(initial_pos)
        adjust = (current_pos + move) // len(encrypted_file)
        next_pos = (current_pos + move + adjust) % len(encrypted_file)
        # The below commented code is not mandatory for the result to be correct! But it shall actually be run to comply
        # with the given sample output. When a value reach an edge, it shall be appended at the other side (-2 example
        # in the sample). This does not change the relative position of values which only matters.
        # Zero does not move (even on the edges):
        # if value != 0:
        #    if next_pos == len(encrypted_file) - 1:
        #        next_pos = 0
        #    elif next_pos == 0:
        #        next_pos = len(encrypted_file) - 1
        mixed_positions.insert(next_pos, mixed_positions.pop(current_pos))

    mixed_file = [encrypted_file[pos] for pos in mixed_positions]
    i_0 = mixed_file.index(0)
    print(sum([
        mixed_file[(i_0 + 1000) % len(mixed_file)],
        mixed_file[(i_0 + 2000) % len(mixed_file)],
        mixed_file[(i_0 + 3000) % len(mixed_file)]
    ]))
