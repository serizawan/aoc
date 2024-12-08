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

    invalid_middle_page_sum = 0
    for updates in updates_instructions:
        is_valid = True
        for i, page in enumerate(updates):
            min_i_page_rule = i
            for page_rule in rules[page]:
                if page_rule in updates[:i]:
                    is_valid = False
                    i_page_rule = updates.index(page_rule)
                    min_i_page_rule = min(i_page_rule, min_i_page_rule)
            updates.pop(i)
            updates.insert(min_i_page_rule, page)
        if not is_valid:
            invalid_middle_page_sum += updates[len(updates) // 2]

    print(invalid_middle_page_sum)

