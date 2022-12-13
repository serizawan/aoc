import operator
import re
import sys


N_ROUNDS = 10000
MONKEY_DESC_N_LINES = 6
OPS = {"+": operator.add, "*": operator.mul}


class Item:
    def __init__(self, worry_level_mods):
        # Note that here we stored the worry_level modulo each monkey.div attribute.
        # We may have improved code simplicity by storing only worry_level modulo the monkey.divs product.
        self.worry_level_mods = worry_level_mods


class Operator:
    def __init__(self, op, right_value):
        self.op = op
        self.right_value = right_value

    def apply(self, left_value):
        if self.right_value == "left_value":
            return OPS[self.op](left_value, left_value)
        return OPS[self.op](left_value, self.right_value)
        # Using eval slows down by a 15 to 20 factor (4s vs 70s total runtime)
        # Requires an additional eval because eval("3 * 'left_value'") with left_value = 2 can be interpreted as: 222
        # return eval(f"{left_value} {self.op} {eval(str(self.right_value))}")


class Monkeys:
    def __init__(self, monkey_list):
        self.monkey_list = monkey_list

    @property
    def divs(self):
        return [monkey.div for monkey in self.monkey_list]


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
        wlms = self.current_item.worry_level_mods
        divs = monkeys.divs
        self.current_item.worry_level_mods = [self.operator.apply(wlm) % divs[i] for i, wlm in enumerate(wlms)]

    def test(self):
        if self.current_item.worry_level_mods[self.monkey_id] == 0:
            self.to = self.true_monkey
        else:
            self.to = self.false_monkey

    def throw(self):
        monkeys.monkey_list[self.to].items.append(self.current_item)
        self.current_item = None
        self.to = None

    def run(self):
        while self.items:
            self.inspect()
            self.operate()
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
    monkey_list = []
    for i in range(n_monkeys):
        lines_id = [(MONKEY_DESC_N_LINES + 1) * i + j for j in range(MONKEY_DESC_N_LINES)]
        monkey_id = int(re.search(r'\d+', lines[lines_id[0]]).group())
        # It is ok not to store mods value here as the first operate will take responsibility for it.
        items = [Item([int(j) for _ in range(n_monkeys)]) for j in re.findall(r'\d+', lines[lines_id[1]])]
        capture_right_value_if_number = re.search(r'\d+', lines[lines_id[2]])
        right_value = int(capture_right_value_if_number.group()) if capture_right_value_if_number else "left_value"
        op = re.search(r'[\+\*]', lines[lines_id[2]]).group()
        operator = Operator(op, right_value)
        div = int(re.search(r'\d+', lines[lines_id[3]]).group())
        true_monkey = int(re.search(r'\d+', lines[lines_id[4]]).group())
        false_monkey = int(re.search(r'\d+', lines[lines_id[5]]).group())
        monkey_list.append(Monkey(monkey_id, items, operator, div, true_monkey, false_monkey))

    monkeys = Monkeys(monkey_list)
    for r in range(N_ROUNDS):
        for monkey in monkeys.monkey_list:
            monkey.run()

    sorted_monkey_list = sorted(monkeys.monkey_list, key=lambda m: m.inspect_count, reverse=True)
    print(sorted_monkey_list[0].inspect_count * sorted_monkey_list[1].inspect_count)
