from functools import reduce

if __name__ == "__main__":
    problems = open(0).read().splitlines()
    problems = [l.split() for l in problems]
    problems = [[int(i) for i in l] for l in problems[:-1]] + [problems[-1]]
    mul_lambda = lambda a, b: a * b
    add_lambda = lambda a, b: a + b
    total = 0
    for j, op in enumerate(problems[-1]):
        if op == "+":
            lmbd = add_lambda
        elif op == "*":
            lmbd = mul_lambda
        total += reduce(lmbd, [problems[i][j] for i in range(len(problems) - 1)])

    print(total)