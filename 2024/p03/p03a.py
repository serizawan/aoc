import re


if __name__ == "__main__":
    corrupted_instructions = open(0).read()

    mul_instruction_pattern = r"mul\(\d+,\d+\)"
    matches = re.findall(mul_instruction_pattern, corrupted_instructions)
    operand_instruction_pattern = r"\d+"
    instructions_results = 0
    for match in matches:
        operands = re.findall(operand_instruction_pattern, match)
        instructions_results += int(operands[0]) * int(operands[1])

    print(instructions_results)