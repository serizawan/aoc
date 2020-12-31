import re
import sys


def is_in(value, dashed_range):
    mini, maxi = dashed_range.split('-')
    mini, maxi = int(mini), int(maxi)
    return mini <= value and value <= maxi


def is_in_any(value, ranges):
    for dashed_range in ranges:
        if is_in(value, dashed_range):
            return True
    return False


def compute_ticket_error_rate(ticket, ranges):
    errors = [v for v in ticket if not is_in_any(v, ranges)]
    return sum(errors)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    idx = 0
    ranges = []
    ranges_regex = re.compile('^.*: (\d*-\d*) or (\d*-\d*)$')
    while lines[idx] != '':
        ranges.append(ranges_regex.match(lines[idx]).group(1))
        ranges.append(ranges_regex.match(lines[idx]).group(2))
        idx += 1

    # Jump to the first nearby tickets line
    idx += 5

    ticket_error_rate = 0
    for line in lines[idx:]:
        ticket = [int(v) for v in line.split(',')]
        ticket_error_rate += compute_ticket_error_rate(ticket, ranges)

    print(ticket_error_rate)
