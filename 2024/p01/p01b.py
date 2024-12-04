if __name__ == "__main__":
    location_ids_lines = open(0).read().splitlines()
    left_ids = []
    right_ids = []
    for location_ids_line in location_ids_lines:
        left, right = location_ids_line.split("   ")
        left_ids.append(int(left))
        right_ids.append(int(right))

    similarity = 0
    for l in left_ids:
        similarity += l * right_ids.count(l)

    print(similarity)