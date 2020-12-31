import sys


class Node:
    def __init__(self, value, next_node):
        self.value = value
        self.next_node = next_node


if __name__ == "__main__":
    # Sample:
    # cups = [int(i) for i in list('389125467')]
    cups = [int(i) for i in list('364289715')]
    cups += [i for i in range(10, 1000000 + 1)]

    # Build linked list
    node = Node(cups[0], None)
    nodes = {cups[0]: node}
    for cup in cups[1:]:
        node.next_node = Node(cup, None)
        node = node.next_node
        nodes[cup] = node

    # Link last node to first node
    node.next_node = nodes[cups[0]]

    node = nodes[cups[0]]

    n_moves = 10000000
    node = nodes[cups[0]]
    for i in range(n_moves):
        # Print linked list
        # n = nodes[1]
        # for j in range(8):
        #     print(n.value, '-> ' , end='')
        #     n = n.next_node
        # print(n.value)
        # print("Move:", i + 1)
        # print("Current:", node.value)
        next_3_nodes = (
            node.next_node, node.next_node.next_node, node.next_node.next_node.next_node
        )
        # print("Picked:", next_3_nodes[0].value, next_3_nodes[1].value, next_3_nodes[2].value)
        # Link node to 4th next node
        node.next_node = next_3_nodes[2].next_node
        dest_value = node.value - 1 if node.value > 1 else max(cups)
        while dest_value in (next_3_nodes[0].value, next_3_nodes[1].value, next_3_nodes[2].value):
            dest_value = dest_value - 1 if dest_value > 1 else max(cups)
        dest_node = nodes[dest_value]
        # print("Dest:", dest_node.value)
        next_dest_node = dest_node.next_node
        dest_node.next_node = next_3_nodes[0]
        next_3_nodes[2].next_node = next_dest_node
        node = node.next_node
        # print()

    node_one = nodes[1]
    next_node_one_value = node_one.next_node.value
    next_next_node_one_value = node_one.next_node.next_node.value
    print(next_node_one_value)
    print(next_next_node_one_value)
    print(next_node_one_value * next_next_node_one_value)
