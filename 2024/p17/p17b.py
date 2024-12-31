from collections import defaultdict


def combo(operand):
    if operand <= 3:
        return operand
    return registers[operand - 4]


def operate(operator, operand):
    if operator == 0:
        registers[0] = registers[0] // (2 ** combo(operand))
        return
    if operator == 1:
        registers[1] = registers[1] ^ operand
        return
    if operator == 2:
        registers[1] = combo(operand) % 8
        return
    if operator == 3:
        return operand if registers[0] != 0 else None
    if operator == 4:
        registers[1] = registers[1] ^ registers[2]
    if operator == 5:
        outs.append(combo(operand) % 8)
        return
    if operator == 6:
        registers[1] = registers[0] // (2 ** combo(operand))
        return
    if operator == 7:
        registers[2] = registers[0] // (2 ** combo(operand))
        return


def run():
    ptr = 0
    while ptr < len(instructions):
        operator, operand = instructions[ptr], instructions[ptr + 1]
        r = operate(operator, operand)
        ptr = r if r is not None else ptr + 2


def find_a_bin(a_bin):
    for i in range(8):
        outs.clear()
        i_bin = bin(i)[2:].zfill(3)
        registers[0] = int(a_bin + i_bin, 2)
        run()
        if outs == instructions:
            return a_bin + i_bin
        elif outs == instructions[-len(outs):]:
            a_bin_r = find_a_bin(a_bin + bin(i)[2:].zfill(3))
            if a_bin_r:
                return a_bin_r


if __name__ == "__main__":
    program = open(0).read().splitlines()
    instructions = [int(instr) for instr in program[4].split(": ")[1].split(",")]
    registers = [0, 0, 0]
    a_bin = "100"
    i = 0
    outs = []
    a_bin_suffix = ""
    a_bin = find_a_bin(a_bin)

    print(int(a_bin, 2))