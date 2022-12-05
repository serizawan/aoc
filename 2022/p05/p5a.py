import re
import sys


def split_input_file(lines):
    i = 0
    while '1' not in lines[i]:
        i += 1
    return lines[:i], [int(j) for j in lines[i].split(' ') if j != ''], lines[i+2:]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Missing input file. Run with: python {sys.argv[0]} [FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    stacks_lines, ids, instructions = split_input_file(lines)

    stacks = [[] for i in range(ids[-1])]
    for stack_line in stacks_lines:
        for i in range((len(stack_line) + 1) // 4):
            crate = stack_line[4 * i:4 * (i + 1) - 1]
            if crate.strip() != "":
                stacks[i].append(crate[1])

    pattern = "move (\d*) from (\d*) to (\d*)"
    prog = re.compile(pattern)
    for instruction in instructions:
        result = re.match(pattern, instruction)
        n, _from, _to = int(result[1]), int(result[2]) - 1, int(result[3]) - 1
        loaded = stacks[_from][:n][::-1]
        stacks[_from] = stacks[_from][n:]
        stacks[_to] = loaded + stacks[_to]

    print("".join([stack[0] for stack in stacks]))


