import math
import re


if __name__ == "__main__":
    claws_machines = open(0).read().splitlines()
    p_button = r"X\+(\d+), Y\+(\d+)"
    p_prize = r"X=(\d+), Y=(\d+)"
    total_cost = 0
    for i in range(len(claws_machines) // 4 + 1):
        a_match = re.search(p_button, claws_machines[4 * i])
        a = int(a_match.group(1)), int(a_match.group(2))
        b_match = re.search(p_button, claws_machines[4 * i + 1])
        b = int(b_match.group(1)), int(b_match.group(2))
        p_match = re.search(p_prize, claws_machines[4 * i + 2])
        p = int(p_match.group(1)), int(p_match.group(2))

        min_cost = math.inf
        for u in range(100):
            for v in range(100):
                if a[0] * u + b[0] * v == p[0] and a[1] * u + b[1] * v == p[1]:
                    min_cost = min(min_cost, 3 * u + v)

        total_cost += min_cost if min_cost != math.inf else 0

    print(total_cost)