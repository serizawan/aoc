if __name__ == "__main__":
    location_ids_lines = open(0).read().splitlines()
    left_ids = []
    right_ids = []
    for location_ids_line in location_ids_lines:
        left, right = location_ids_line.split("   ")
        left_ids.append(int(left))
        right_ids.append(int(right))

    left_ids.sort()
    right_ids.sort()

    zipped_ids = zip(left_ids, right_ids)
    distance = 0
    for l, r in zipped_ids:
        distance += abs(l - r)

    print(distance)