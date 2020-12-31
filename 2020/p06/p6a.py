import sys


def pop_next_group_answers(l):
    if not l:
        return None
    member = None
    group_answers = []
    while l and (member := l.pop(0)) != '':
        group_answers.append(member)
    return group_answers


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    sum_of_groups_yes = 0
    group_answers = pop_next_group_answers(l)
    while group_answers:
        sum_of_groups_yes += len(set(''.join(group_answers)))
        group_answers = pop_next_group_answers(l)

    print(sum_of_groups_yes)
