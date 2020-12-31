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
    capture_color_regex = re.compile("\d (.*) bags?")
    return capture_color_regex.match(in_raw).group(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    ins_outs = {}

    for rule in l:
        out, ins = parse_rule(rule)
        for i in ins:
            ins_outs[i] = ins_outs.get(i, []) + [out]

    bags = set(["shiny gold"])
    colors_result = set()

    while bags:
        new_bags = set()
        for bag in bags:
            colors_result = colors_result.union(set(ins_outs.get(bag, [])))
            new_bags = new_bags.union(set(ins_outs.get(bag, [])))
        bags = new_bags

    print(len(colors_result))
