def is_possible(design):
    if design in cache:
        return cache[design]

    for pattern in patterns:
        if design.startswith(pattern):
            remaining_design = design.replace(pattern, "", 1)
            if is_possible(remaining_design):
                cache[design] = True
                return True

    cache[design] = False
    return False

if __name__ == "__main__":
    patterns_and_designs = open(0).read().splitlines()
    patterns = patterns_and_designs[0].split(", ")
    designs = patterns_and_designs[2:]
    is_possible_counts = 0
    cache = {pattern: True for pattern in patterns }
    for design in designs:
        if is_possible(design):
            is_possible_counts += 1
    print(is_possible_counts)
