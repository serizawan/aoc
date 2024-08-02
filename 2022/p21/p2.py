from copy import deepcopy


class Node:
    def __init__(self, id, operator, left, right, value):
        self.id = id
        self.operator = operator
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        return f"{self.id}: {self.left} {self.operator} {self.right} = {self.value}"


class BinaryTree:
    def __init__(self):
        self.nodes = {}

    @property
    def root(self):
        return self.nodes["root"]

    def add(self, node):
        self.nodes[node.id] = node

    def get_humn(self):
        return self.nodes["humn"]

    def set_humn(self, v):
        self.nodes["humn"].value = v

    def get_node(self, id):
        return self.nodes[id]

    def get_node_left(self, id):
        return self.get_node(self.get_node(id).left)

    def get_node_right(self, id):
        return self.get_node(self.get_node(id).right)

    def eval(self, node):
        # If value is already known, return it.
        if node.value:
            return node.value

        # Otherwise Compute it.
        if node.operator == "+":
            node.value = self.eval(self.get_node(node.left)) + self.eval(self.get_node(node.right))
        elif node.operator == "-":
            node.value = self.eval(self.get_node(node.left)) - self.eval(self.get_node(node.right))
        elif node.operator == "*":
            node.value = self.eval(self.get_node(node.left)) * self.eval(self.get_node(node.right))
        # ZeroDivisionError may hypothetically occur but we don't handle it as it doesn't for the given input.
        elif node.operator == "/":
            node.value = self.eval(self.get_node(node.left)) / self.eval(self.get_node(node.right))

        return node.value


if __name__ == "__main__":
    op_tree = BinaryTree()
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
        op_tree.add(node)

    # Searching the solution linearly is not reasonable in time as the solution very large.
    # We use a dichotomy to improve performances as the function is monotonic - either f(x) = k * x or k / x).
    op_tree_cp = deepcopy(op_tree)

    # Pick the bounds enough far so that the solution lies in-between.
    humn_left, humn_right = 0, 1_000_000_000_000_000

    op_tree_cp.set_humn((humn_left + humn_left) // 2)
    op_tree_cp.eval(op_tree_cp.root)

    while op_tree_cp.get_node_left(op_tree_cp.root.id).value != op_tree_cp.get_node_right(op_tree_cp.root.id).value:
        if op_tree_cp.get_node_left(op_tree_cp.root.id).value > op_tree_cp.get_node_right(op_tree_cp.root.id).value:
            humn_left = op_tree_cp.get_humn().value
        else:
            humn_right = op_tree_cp.get_humn().value

        op_tree_cp = deepcopy(op_tree)
        op_tree_cp.set_humn((humn_left + humn_right) // 2)
        op_tree_cp.eval(op_tree_cp.root)

    print(op_tree_cp.get_humn().value)
