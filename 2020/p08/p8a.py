from enum import Enum
import re
import sys


class Operation(Enum):
    acc = 0
    jmp = 1
    nop = 2


def parse_instruction(instruction):
    op_and_arg = instruction.split(' ')
    return Operation[op_and_arg[0]], int(op_and_arg[1])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    acc = 0
    instruction_idx = 0
    visited_instructions = set()
    while instruction_idx not in visited_instructions:
        instruction = l[instruction_idx]
        operation, value = parse_instruction(instruction)
        visited_instructions.add(instruction_idx)
        if operation == Operation.acc:
            acc += value
            instruction_idx += 1
        elif operation == Operation.jmp:
            instruction_idx += value
        else:
            instruction_idx += 1

    print(acc)
