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

    def eval(self, nodes_by_id):
        # If value is already known, return it.
        if self.value:
            return self.value

        # Otherwise Compute it.
        if self.operator == "+":
            self.value = nodes_by_id[self.left].eval(nodes_by_id) + nodes_by_id[self.right].eval(nodes_by_id)
        elif self.operator == "-":
            self.value = nodes_by_id[self.left].eval(nodes_by_id) - nodes_by_id[self.right].eval(nodes_by_id)
        if self.operator == "*":
            self.value = nodes_by_id[self.left].eval(nodes_by_id) * nodes_by_id[self.right].eval(nodes_by_id)
        # ZeroDivisionError may hypothetically occur but we don't handle it as it doesn't for the given input.
        if self.operator == "/":
            self.value = nodes_by_id[self.left].eval(nodes_by_id) / nodes_by_id[self.right].eval(nodes_by_id)

        return self.value


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

    # Searching the solution linearly is not reasonable in time as the solution very large.
    # We use a dichotomy to improve performances as the function is monotonic - either f(x) = k * x or k / x).
    nodes_by_id_left, nodes_by_id_right = deepcopy(nodes_by_id), deepcopy(nodes_by_id)
    nodes_by_id_center = deepcopy(nodes_by_id)

    # Pick the bounds enough far so that the solution lies in-between.
    humn_left, humn_right = 0, 1_000_000_000_000_000
    humn_center = (humn_left + humn_right) // 2

    nodes_by_id_left["humn"].value, nodes_by_id_right["humn"].value = humn_left, humn_right
    nodes_by_id_center["humn"].value = humn_center

    root_node_left, root_node_right = nodes_by_id_left["root"], nodes_by_id_right["root"]
    root_node_center = nodes_by_id_center["root"]

    root_node_left.eval(nodes_by_id_left), root_node_right.eval(nodes_by_id_right)
    root_node_center.eval(nodes_by_id_center)
    while nodes_by_id_center[root_node_center.left].value != nodes_by_id_center[root_node_center.right].value:
        if nodes_by_id_center[root_node_center.left].value > nodes_by_id_center[root_node_center.right].value:
            nodes_by_id_left = nodes_by_id_center
            root_node_left = nodes_by_id_left["root"]

        elif nodes_by_id_center[root_node_center.left].value < nodes_by_id_center[root_node_center.right].value:
            nodes_by_id_right = nodes_by_id_center
            root_node_right = nodes_by_id_right["root"]

        nodes_by_id_center = deepcopy(nodes_by_id)
        nodes_by_id_center["humn"].value = (nodes_by_id_left["humn"].value + nodes_by_id_right["humn"].value) // 2
        root_node_center = nodes_by_id_center["root"]
        root_node_center.eval(nodes_by_id_center)

    print(nodes_by_id_center["humn"].value)
