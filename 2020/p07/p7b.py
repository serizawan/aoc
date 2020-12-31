import re
import sys


def parse_rule(rule):
    splitted_rule = rule.split(' bags contain ')
    out = splitted_rule[0]
    ins_raw = splitted_rule[1].split(', ')
    ins = []
    for in_raw in ins_raw:
        c = capture_color(in_raw)
        if c:
            ins.append(c)
    return out, ins


def capture_color(in_raw):
    if in_raw == "no other bags.":
        return
    capture_color_regex = re.compile("(\d) (.*) bags?")
    captured_color = capture_color_regex.match(in_raw)
    return (captured_color.group(2), int(captured_color.group(1)))


def count_bags(bags):
    count = 0
    if not bags:
        return count
    for bag in bags:
        count += bag[1] * (count_bags(out_ins[bag[0]]) + 1)
    return count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    out_ins = {}
    for rule in l:
        out, ins = parse_rule(rule)
        out_ins[out] = ins

    bags = [("shiny gold", 1)]
    bags_count = 0

    # Don't count the "shiny gold" bag
    bags_count = count_bags(bags) - 1
    print(bags_count)
