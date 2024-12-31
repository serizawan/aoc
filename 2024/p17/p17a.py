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
        outs.append(str(combo(operand) % 8))
        return
    if operator == 6:
        registers[1] = registers[0] // (2 ** combo(operand))
        return
    if operator == 7:
        registers[2] = registers[0] // (2 ** combo(operand))
        return


if __name__ == "__main__":
    program = open(0).read().splitlines()
    registers = [int(register.split(": ")[1]) for register in program[:3]]
    instructions = [int(instr) for instr in program[4].split(": ")[1].split(",")]
    ptr = 0
    outs = []
    while ptr < len(instructions):
        operator, operand = instructions[ptr], instructions[ptr + 1]
        r = operate(operator, operand)
        ptr = r if r is not None else ptr + 2

    print(",".join(outs))