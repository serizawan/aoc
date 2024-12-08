from collections import defaultdict


if __name__ == "__main__":
    printer_manual = open(0).read().splitlines()
    rules = defaultdict(set)
    for i, line in enumerate(printer_manual):
        if line == "":
            break
        left, right = line.split("|")
        left, right = int(left), int(right)
        rules[left].add(right)

    updates_instructions = printer_manual[i+1:]
    updates_instructions = [[int(item) for item in line.split(",")] for line in updates_instructions]

    valid_middle_page_sum = 0
    for updates in updates_instructions:
        is_valid = True
        for i, page in enumerate(updates):
            for page_rule in rules[page]:
                if page_rule in updates[:i]:
                    is_valid = False
        if is_valid:
            valid_middle_page_sum += updates[len(updates) // 2]

    print(valid_middle_page_sum)

