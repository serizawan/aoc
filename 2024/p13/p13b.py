import re


if __name__ == "__main__":
    claws_machines = open(0).read().splitlines()
    p_button = r"X\+(\d+), Y\+(\d+)"
    p_prize = r"X=(\d+), Y=(\d+)"
    total_cost = 0
    shift = 10_000_000_000_000
    for i in range(len(claws_machines) // 4 + 1):
        a_match = re.search(p_button, claws_machines[4 * i])
        a = int(a_match.group(1)), int(a_match.group(2))
        b_match = re.search(p_button, claws_machines[4 * i + 1])
        b = int(b_match.group(1)), int(b_match.group(2))
        p_match = re.search(p_prize, claws_machines[4 * i + 2])
        p = int(p_match.group(1)) + shift, int(p_match.group(2)) + shift

        s_a = (p[0] * b[1] - p[1] * b[0]) / (a[0] * b[1] - a[1] * b[0])
        s_b = (p[0] - a[0] * s_a) / b[0]

        if s_a >= 0 and s_a == int(s_a) and s_b >= 0 and s_b == int(s_b):
            total_cost += 3 * s_a + s_b

    print(int(total_cost))