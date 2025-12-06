if __name__ == "__main__":
    banks = open(0).read().splitlines()
    total_output_joltage = 0
    for bank in banks:
        batteries = [int(battery) for battery in bank]
        first = max(batteries[:-1])
        first_idx = batteries.index(first)
        second = max(batteries[first_idx + 1:])
        total_output_joltage += first * 10 + second

    print(total_output_joltage)