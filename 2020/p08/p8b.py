from enum import Enum
import re
import sys


class Operation(Enum):
    acc = 0
    jmp = 1
    nop = 2


def parse_instruction(instruction):
    op_and_arg = instruction.split(' ')
    return [Operation[op_and_arg[0]], int(op_and_arg[1])]


def run(parsed_l):
    acc = 0
    instruction_idx = 0
    visited_instructions = set()
    while instruction_idx < len(parsed_l) and instruction_idx not in visited_instructions:
        instruction = parsed_l[instruction_idx]
        operation, value = instruction
        visited_instructions.add(instruction_idx)
        if operation == Operation.acc:
            acc += value
            instruction_idx += 1
        elif operation == Operation.jmp:
            instruction_idx += value
        else:
            instruction_idx += 1
    return instruction_idx, acc


def next_nop_or_jmp(parsed_l, i):
    while parsed_l[i][0] != Operation.nop and parsed_l[i][0] != Operation.jmp:
        i += 1
    return i


def switch_instruction(l, idx):
    if l[idx][0] == Operation.jmp:
        l[idx][0] = Operation.nop
    elif l[idx][0] == Operation.nop:
        l[idx][0] = Operation.jmp
    else:
        raise Exception("switch_instruction shall only be used for nop or jmp instructions (used on {})".format(l[idx][0]))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    parsed_l = [parse_instruction(r) for r in l]
    stopped_idx, acc = run(parsed_l)
    next_idx = 0
    while stopped_idx < len(parsed_l):
        next_idx = next_nop_or_jmp(parsed_l, next_idx)
        switch_instruction(parsed_l, next_idx)
        stopped_idx, acc = run(parsed_l)
        # switch back
        switch_instruction(parsed_l, next_idx)
        next_idx += 1

    print(acc)
