import sys


def pull_next_passport(l):
    passport = []
    while l:
        # l.pop() pops the last item of a list
        passport_line = l.pop(0)
        if passport_line == '':
            break
        passport.append(passport_line)
    return ' '.join(passport)


def check_passport(passport):
    mandatory_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    for field in mandatory_fields:
        if field not in passport:
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
