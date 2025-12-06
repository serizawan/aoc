if __name__ == "__main__":
    banks = open(0).read().splitlines()
    total_output_joltage = 0
    n_to_lit = 12
    for bank in banks:
        joltage = 0
        batteries = [int(battery) for battery in bank]
        to_lit = max(batteries[:-n_to_lit + 1])
        idx_to_lit = batteries.index(to_lit)
        joltage = joltage * 10 + to_lit
        for i in range(1, n_to_lit):
            batteries = batteries[idx_to_lit + 1:]
            to_lit = max(batteries[:len(batteries) -n_to_lit + i + 1])
            idx_to_lit = batteries.index(to_lit)
            joltage = joltage * 10 + to_lit
        total_output_joltage += joltage

    print(total_output_joltage)