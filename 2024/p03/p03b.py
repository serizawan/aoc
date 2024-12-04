import re


if __name__ == "__main__":
    corrupted_instructions = open(0).read()

    instruction_pattern = r"do\(\)|don\'t\(\)|mul\(\d+,\d+\)"
    instructions = re.findall(instruction_pattern, corrupted_instructions)
    operand_instruction_pattern = r"\d+"
    instructions_results = 0
    acc_enabled = True
    for instruction in instructions:
        if instruction == "do()":
            acc_enabled = True
        elif instruction == "don't()":
            acc_enabled = False
        else:
            operands = re.findall(operand_instruction_pattern, instruction)
            instructions_results += int(operands[0]) * int(operands[1]) if acc_enabled else 0

    print(instructions_results)