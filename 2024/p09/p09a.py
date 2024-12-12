if __name__ == "__main__":
    disk_map_dense = open(0).read()
    disk_map =[]
    is_free = False
    for i, l in enumerate(disk_map_dense):
        if is_free:
            disk_map += list("." * int(l))
        else:
            disk_map += [str(i // 2) for j in range(int(l))]
        is_free = not is_free

    dot_indexes = [i for i, v in enumerate(disk_map) if v == "."]

    while dot_indexes:
        last_disk_id = disk_map.pop()
        if last_disk_id == ".":
            dot_indexes.pop()
        else:
            dot_i = dot_indexes.pop(0)
            disk_map[dot_i] = last_disk_id

    checksum = 0
    for i, v in enumerate(disk_map):
        checksum += i * int(v)

    print(checksum)


