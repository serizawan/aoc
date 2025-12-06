from functools import reduce


if __name__ == "__main__":
    problems = open(0).read().splitlines()
    operands_list = problems[:-1]
    operators = problems[-1].split()
    refactored_problems= []
    i = 0
    for operator in operators:
        has_more_operands = True
        refactored_operands = []
        while has_more_operands and i < len(operands_list[0]):
            operand = "".join([operands_line[i] for operands_line in operands_list])
            operand = operand.strip()
            if operand:
                refactored_operands.append(int(operand))
            else:
                has_more_operands = False
            i += 1
        refactored_problems.append((refactored_operands, operator))

    mul_lambda = lambda a, b: a * b
    add_lambda = lambda a, b: a + b

    total = 0
    for problem in refactored_problems:
        if problem[1] == "+":
            lmbd = add_lambda
        elif problem[1] == "*":
            lmbd = mul_lambda
        total += reduce(lmbd, problem[0])

    print(total)