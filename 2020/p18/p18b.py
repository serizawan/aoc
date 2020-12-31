import operator
import sys

ops = {
    '+': operator.add,
    '*': operator.mul,
}

def evaluate(expression):
    idx = 0
    if len(expression) == 1:
        return [expression[idx]]

    if '(' not in expression and '+' in expression:
        plus_idx = expression.index('+')
        return evaluate(
                expression[:plus_idx-1] +
                [ops[expression[plus_idx]](expression[plus_idx-1], expression[plus_idx + 1])] + 
                expression[plus_idx + 2:]
        )

    if '(' not in expression and '+' not in expression:
        return evaluate([ops[expression[1]](expression[0], expression[2])] + expression[3:])

    while '(' in expression:
        start_idx = expression.index('(')
        stop_idx = start_idx
        count_parenthesis = 1
        while count_parenthesis != 0:
            stop_idx += 1
            if expression[stop_idx] == '(':
                 count_parenthesis += 1
            elif expression[stop_idx] == ')':
                count_parenthesis -= 1
            else:
                continue
        expression = expression[0:start_idx] + evaluate(expression[start_idx + 1:stop_idx]) + expression[stop_idx + 1:]
    return evaluate(expression)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    results = []
    for line in lines:
        expression = [int(c) if c.isdigit() else c for c in list(line.replace(' ', ''))]
        result = evaluate(expression)[0]
        results.append(result)

    print(sum(results))
