def is_possible(design, count):
    if design == "":
        return count + 1

    if design in cache:
        return count + cache[design]

    c = count
    for pattern in patterns:
        if design.startswith(pattern):
            remaining_design = design.replace(pattern, "", 1)
            count = is_possible(remaining_design, count)

    if count == c:
        cache[design] = 0
    else:
        cache[design] = count - c

    return count

if __name__ == "__main__":
    patterns_and_designs = open(0).read().splitlines()
    patterns = patterns_and_designs[0].split(", ")
    designs = patterns_and_designs[2:]
    total_arrangement_counts = 0
    cache = {}
    for design in designs:
        arrangement_counts = is_possible(design, 0)
        total_arrangement_counts += arrangement_counts

    print(total_arrangement_counts)
