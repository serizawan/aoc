import re
import sys


N_ROUNDS = 20
MONKEY_DESC_N_LINES = 6


class Item:
    RELIEF_RATIO = 3

    def __init__(self, worry_level):
        self.worry_level = worry_level


class Operator:
    def __init__(self, op, right_value):
        self.op = op
        self.right_value = right_value

    def apply(self, left_value):
        # Requires an additional eval because eval("3 * 'left_value'") with left_value = 2 can be interpreted as: 222
        return eval(f"{left_value} {self.op} {eval(str(self.right_value))}")


class Monkey:
    def __init__(self, monkey_id, items, operator, div, true_monkey, false_monkey):
        self.current_item = None
        self.to = None
        self.monkey_id = monkey_id
        self.items = items
        self.operator = operator
        self.div = div
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspect_count = 0

    def inspect(self):
        self.inspect_count += 1

    def operate(self):
        self.current_item = self.items.pop(0)
        self.current_item.worry_level = self.operator.apply(self.current_item.worry_level)

    def relief(self):
        self.current_item.worry_level = self.current_item.worry_level // Item.RELIEF_RATIO

    def test(self):
        if self.current_item.worry_level % self.div == 0:
            self.to = self.true_monkey
        else:
            self.to = self.false_monkey

    def throw(self):
        monkeys[self.to].items.append(self.current_item)
        self.current_item = None
        self.to = None

    def run(self):
        while self.items:
            self.inspect()
            self.operate()
            self.relief()
            self.test()
            self.throw()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    n_monkeys = int(re.search(r'\d+', lines[-MONKEY_DESC_N_LINES]).group()) + 1
    monkeys = []
    for i in range(n_monkeys):
        lines_id = [(MONKEY_DESC_N_LINES + 1) * i + j for j in range(MONKEY_DESC_N_LINES)]
        monkey_id = int(re.search(r'\d+', lines[lines_id[0]]).group())
        items = [Item(j) for j in re.findall(r'\d+', lines[lines_id[1]])]
        capture_right_value_if_number = re.search(r'\d+', lines[lines_id[2]])
        right_value = int(capture_right_value_if_number.group()) if capture_right_value_if_number else "left_value"
        op = re.search(r'[\+\*]', lines[lines_id[2]]).group()
        operator = Operator(op, right_value)
        div = int(re.search(r'\d+', lines[lines_id[3]]).group())
        true_monkey = int(re.search(r'\d+', lines[lines_id[4]]).group())
        false_monkey = int(re.search(r'\d+', lines[lines_id[5]]).group())
        monkeys.append(Monkey(monkey_id, items, operator, div, true_monkey, false_monkey))

    for r in range(N_ROUNDS):
        for monkey in monkeys:
            monkey.run()

    monkeys = sorted(monkeys, key=lambda m: m.inspect_count, reverse=True)
    print(monkeys[0].inspect_count * monkeys[1].inspect_count)


