import sys


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    count_displayed_1_4_7_8 = 0
    for line in lines:
        raw_signals, raw_displayed_digits = line.split(' | ')
        signals = [set(signal) for signal in raw_signals.split(' ')]
        displayed_digits = [set(digit) for digit in raw_displayed_digits.split(' ')]
        decoder = [''] * 10

        # Map unique length signals: 1, 4, 7 and 8 (Remaining: 0, 2, 3, 5, 6 and 9)
        unmapped_signals = []
        for signal in signals:
            if len(signal) == 2:
                decoder[1] = signal
            elif len(signal) == 3:
                decoder[7] = signal
            elif len(signal) == 4:
                decoder[4] = signal
            elif len(signal) == 7:
                decoder[8] = signal
            else:
                unmapped_signals.append(signal)

        # Map 3 and 9 (Remaining: 0, 2, 5 and 6)
        signals = unmapped_signals[:]
        unmapped_signals = []
        for signal in signals:
            if len(signal) == 5 and decoder[1].issubset(signal):
                decoder[3] = signal
            elif len(signal) == 6 and decoder[4].issubset(signal):
                decoder[9] = signal
            else:
                unmapped_signals.append(signal)

        # Map 0 (Remaining: 2, 5 and 6)
        signals = unmapped_signals[:]
        unmapped_signals = []
        for signal in signals:
            if len(signal) == 6 and decoder[1].issubset(signal):
                decoder[0] = signal
            else:
                unmapped_signals.append(signal)

        # Map 6 (Remaining: 2 and 5)
        signals = unmapped_signals[:]
        unmapped_signals = []
        for signal in signals:
            if len(signal) == 6:
                decoder[6] = signal
            else:
                unmapped_signals.append(signal)

        # Map 5 (Remaining: 2)
        signals = unmapped_signals[:]
        unmapped_signals = []
        for signal in signals:
            if signal.issubset(decoder[6]):
                decoder[5] = signal
            else:
                unmapped_signals.append(signal)

        # Map 2 (Remaining: None)
        decoder[2] = unmapped_signals[0]

        for digit in displayed_digits:
            for i, signal in enumerate(decoder):
                if digit == signal and i in [1, 4, 7, 8]:
                    count_displayed_1_4_7_8 += 1

    print(count_displayed_1_4_7_8)


if __name__ == "__main__":
    run()
