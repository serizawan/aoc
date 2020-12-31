import sys


if len(sys.argv) != 2:
    print("Missing input file: python {} file".format(sys.argv[0]))
    sys.exit()

with open(sys.argv[1]) as f:
    l = f.read().splitlines()

valid_count = 0
for rule_and_pwd in l:
    rule, pwd = rule_and_pwd.split(':')
    rule = rule.strip()
    pwd = pwd.strip()

    # Parse rule
    letter = rule[-1]
    mini, maxi = rule.split(' ')[0].split('-')
    mini, maxi = int(mini), int(maxi)

    if pwd.count(letter) >= mini and pwd.count(letter) <= maxi:
        valid_count += 1

print(valid_count)
