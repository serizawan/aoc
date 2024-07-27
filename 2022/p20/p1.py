if __name__ == "__main__":
    encrypted_file = []
    for line in open(0).read().splitlines():
        encrypted_file.append(int(line))

    mixed_positions = list(range(len(encrypted_file)))
    mixed_file = encrypted_file[:]

    for initial_pos in range(len(encrypted_file)):
        value = encrypted_file[initial_pos]
        current_pos = mixed_positions.index(initial_pos)
        sign = (current_pos + value) // abs(current_pos + value) if abs(current_pos + value) != 0 else -1
        if value == 0 and current_pos == 0:
            sign = 0
        adjust = (current_pos + value + sign) // len(encrypted_file)
        next_pos = (current_pos + value + adjust) % len(encrypted_file)
        mixed_positions.insert(next_pos, mixed_positions.pop(current_pos))

    mixed_file = [encrypted_file[pos] for pos in mixed_positions]
    i_0 = mixed_file.index(0)
    print(sum([
        mixed_file[(i_0 + 1000) % len(mixed_file)],
        mixed_file[(i_0 + 2000) % len(mixed_file)],
        mixed_file[(i_0 + 3000) % len(mixed_file)]
    ]))
