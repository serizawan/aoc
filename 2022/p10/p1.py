import sys


H = 6
CYCLES = tuple(20 + 40 * x for x in range(H))


def update_signal_strengths_sum(cycle, x_register, signal_strengths_sum):
    if cycle in CYCLES:
        signal_strengths_sum += cycle * x_register
    return signal_strengths_sum


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    cycle = 0
    signal_strengths_sum = 0
    x_register = 1
    for line in lines:
        cycle += 1
        signal_strengths_sum = update_signal_strengths_sum(cycle, x_register, signal_strengths_sum)
        if line.startswith("addx"):
            cycle += 1
            signal_strengths_sum = update_signal_strengths_sum(cycle, x_register, signal_strengths_sum)
            v = int(line.split(" ")[1])
            x_register += v

    print(signal_strengths_sum)
