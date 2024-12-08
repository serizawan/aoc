def is_solvable(equation):
    result = equation[0]
    operands = equation[1]
    _is_solvable = False

    if len(operands) == 1:
        return result == eval(operands[0])

    for operator in ["+", "*"]:
        operated = "(" + equation[1][0] + " " + operator + " " + equation[1][1] + ")"
        if is_solvable([equation[0], [operated, *equation[:][1][2:]]]):
            return True
    return False

if __name__ == "__main__":
    equations = open(0).read().splitlines()
    equations = [equation.split(": ") for equation in equations]
    equations = [[int(equation[0]), equation[1].split(" ")] for equation in equations]

    total_solvable_results = 0
    for equation in equations:
        if is_solvable(equation):
            total_solvable_results += equation[0]

    print(total_solvable_results)