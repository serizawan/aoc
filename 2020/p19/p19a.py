import re
import sys


def compute_rule_rgx(rule, rules):
    if rule == '"a"' or rule == '"b"':
        return rule.replace('"', '')

    if len(rule.split(' ')) == 1:
        return compute_rule_rgx(rules[rule], rules)

    if '|' in rule:
        or_rules = rule.split(' | ')
        or_rules_rgx = [compute_rule_rgx(or_rule, rules) for or_rule in or_rules]
        return '({})'.format('|'.join(or_rules_rgx))

    return ''.join([compute_rule_rgx(rule, rules) for rule in rule.split(' ')])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    i = 0
    rules = {}
    while lines[i] != '':
        rule_id, rule = lines[i].split(': ')
        rules[rule_id] = rule
        i += 1

    rule0 = rules['0']
    rule0_rgx = '^' + compute_rule_rgx(rule0, rules) + '$'

    rule0_rgx_compiled = re.compile(rule0_rgx)

    matching_messages_count = 0
    for line in lines[i+1:]:
        if rule0_rgx_compiled.match(line):
            matching_messages_count += 1

    print(matching_messages_count)
