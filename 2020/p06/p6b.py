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

    sum_of_groups_all_yes = 0
    group_answers = pop_next_group_answers(l)
    while group_answers:
        group_all_yes = set(group_answers[0])
        for member_answers in group_answers[1:]:
            group_all_yes = group_all_yes.intersection(set(member_answers))
        sum_of_groups_all_yes += len(group_all_yes)
        group_answers = pop_next_group_answers(l)

    print(sum_of_groups_all_yes)
