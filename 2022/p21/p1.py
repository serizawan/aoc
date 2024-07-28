class Node:
    def __init__(self, id, operator, left, right, value):
        self.id = id
        self.operator = operator
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        return f"{self.id}: {self.left} {self.operator} {self.right} = {self.value}"


    def eval(self):
        if self.value:
            return self.value
        if self.operator == "+":
            return nodes_by_id[self.left].eval() + nodes_by_id[self.right].eval()
        if self.operator == "-":
            return nodes_by_id[self.left].eval() - nodes_by_id[self.right].eval()
        if self.operator == "*":
            return nodes_by_id[self.left].eval() * nodes_by_id[self.right].eval()
        # ZeroDivisionError may hypothetically occur but we don't handle it as it doesn't for the given input.
        if self.operator == "/":
            return nodes_by_id[self.left].eval() // nodes_by_id[self.right].eval()


if __name__ == "__main__":
    nodes_by_id= {}
    for line in open(0).read().splitlines():
        id, expr = line.split(":")
        expr = expr.replace(" ", "")
        left, right, operator, value = None, None, None, None
        try:
            value = int(expr)
        except ValueError:
            left = expr[:4]
            operator = expr[4]
            right = expr[5:]
        node = Node(id, operator, left, right, value)
        nodes_by_id[id] = node

    print(nodes_by_id["root"].eval())