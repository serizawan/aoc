import re
import sys


def pull_next_passport(l):
    passport = {}
    while l:
        # l.pop() pops the last item of a list
        passport_line = l.pop(0)
        if passport_line == '':
            break
        passport_items = passport_line.split(' ')
        for item in passport_items:
            key, value = item.split(':')
            passport[key] = value
    return passport


def check_passport(passport):
    mandatory_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    # Check mandatory fields are available
    for field in mandatory_fields:
        if field not in passport:
            return False
    # Check data are compliant with rules
    if int(passport['byr']) < 1920 or int(passport['byr']) > 2002:
        return False
    if int(passport['iyr']) < 2010 or int(passport['iyr']) > 2020:
        return False
    if int(passport['eyr']) < 2020 or int(passport['eyr']) > 2030:
        return False
    if 'cm' not in passport['hgt'] and 'in' not in passport['hgt']:
        return False
    elif 'cm' in passport['hgt']:
        hgt_cm = passport['hgt'][:-2]
        if not hgt_cm or int(hgt_cm) < 150 or int(hgt_cm) > 193:
            return False
    elif 'in' in passport['hgt']:
        hgt_in = passport['hgt'][:-2]
        if not hgt_in or int(hgt_in) < 59 or int(hgt_in) > 76:
            return False
    pattern_hcl = re.compile('^#[\da-f]{6}$')
    if not pattern_hcl.match(passport['hcl']):
        return False
    if passport['ecl'] not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return False
    pattern_pid = re.compile('^\d{9}$')
    if not pattern_pid.match(passport['pid']):
        return False
    return True


if len(sys.argv) != 2:
    print("Missing input file: python {} file".format(sys.argv[0]))
    sys.exit()

with open(sys.argv[1]) as f:
    l = f.read().splitlines()

count_valid = 0
while l:
    passport = pull_next_passport(l)
    if check_passport(passport):
        count_valid += 1
print(count_valid)
