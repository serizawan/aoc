import functools
import operator
import re
import sys


def is_in(value, dashed_range):
    mini, maxi = dashed_range.split('-')
    mini, maxi = int(mini), int(maxi)
    return mini <= value and value <= maxi


def is_in_field_ranges(value, field_ranges):
    return is_in(value, field_ranges[1]) or is_in(value, field_ranges[2])


def is_in_any(value, ranges):
    for field_ranges in ranges:
        if is_in_field_ranges(value, field_ranges):
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
    ranges_regex = re.compile('^(\d*-\d*) or (\d*-\d*)$')
    while lines[idx] != '':
        field_name, field_ranges = lines[idx].split(': ')
        r1 = ranges_regex.match(field_ranges).group(1)
        r2 = ranges_regex.match(field_ranges).group(2)
        ranges.append((field_name, r1, r2))
        idx += 1

    idx += 2
    my_ticket = [int(i) for i in lines[idx].split(',')]

    idx += 3
    ticket_error_rate = 0
    valid_tickets = []
    for line in lines[idx:]:
        ticket = [int(v) for v in line.split(',')]
        ticket_error = compute_ticket_error_rate(ticket, ranges)
        if ticket_error == 0:
            valid_tickets.append(ticket)

    compatible_fields_by_field = []
    n_fields = len(valid_tickets[0])
    for field_idx in range(n_fields):
        compatible_field_ranges = ranges[:]
        for ticket in valid_tickets:
            compatible_field_ranges = [field_ranges for field_ranges in compatible_field_ranges if is_in_field_ranges(ticket[field_idx], field_ranges)]
        compatible_fields_by_field.append([field_ranges[0] for field_ranges in compatible_field_ranges])

    fields = ['' for i in range(n_fields)]
    for i in range(len(fields)):
        for j, compatible_fields in enumerate(compatible_fields_by_field):
            if len(compatible_fields) == i + 1:
               field = (set(compatible_fields) - set(fields)).pop()
               fields[j] = field

    values = [value for idx, value in enumerate(my_ticket) if 'departure' in fields[idx]]
    print(functools.reduce(operator.mul, values))
