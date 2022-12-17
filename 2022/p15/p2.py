import math
import re
import sys


MIN_X, MAX_X = 0, 4000000
MIN_Y, MAX_Y = 0, 4000000
TUNING_FREQ_MUL = 4000000
# For sample input
# MIN_X, MAX_X = 0, 20
# MIN_Y, MAX_Y = 0, 20


def compute_manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def compute_coverage(sensor, beacon, x):
    left_on_x, right_on_x = compute_bounds(sensor, beacon, x)
    # Note that if left and right does not work as we want to left or right to be possibly both 0
    return set(range(left_on_x, right_on_x + 1)) if left_on_x is not None and right_on_x is not None else set()


def compute_bounds(sensor, beacon, x):
    sensor_beacon_dist = compute_manhattan_dist(sensor, beacon)
    left_on_x = sensor[1] - (sensor_beacon_dist - abs(sensor[0] - x))
    left_on_x = min(max(left_on_x, MIN_Y), MAX_Y)
    right_on_x = sensor[1] + (sensor_beacon_dist - abs(sensor[0] - x))
    right_on_x = max(min(right_on_x, MAX_Y), MIN_Y)
    return (left_on_x, right_on_x) if left_on_x <= right_on_x else (None, None)


# Klee's algorithm implementation
def compute_union_size(bounds):
    size = 0
    counter = 1
    for i in range(1, len(bounds)):
        if counter > 0:
            size += bounds[i][0] - bounds[i - 1][0]

        if bounds[i][1]:
            counter -= 1
        else:
            counter += 1
    return size


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    for x in range(MAX_X + 1):
        bounds = []
        for line in lines:
            sensor_and_beacon = tuple(int(i) for i in re.findall(r"-?\d+", line))
            sensor, beacon = sensor_and_beacon[:2], sensor_and_beacon[2:]
            # We use X ([0]) for rows and Y ([1]) for columns
            sensor, beacon = sensor[::-1], beacon[::-1]
            left, right = compute_bounds(sensor, beacon, x)
            # Note that if left and right does not work as we want to left or right to be possibly both 0
            if left is not None and right is not None:
                bounds.append((left, False))
                bounds.append((right, True))
        # If bounds are equal, put start_bounds left and end_bounds right
        bounds.sort(key=lambda item: (item[0], item[1]))
        union_size = compute_union_size(bounds)
        # Break when there is a remaining space left for a beacon which means that there is a 2-size gap.
        # Luckily it works, but actually this condition may be wrong:
        #   - It may not be triggered if there is an additional 1-size gap on the same line
        #   - It may be triggered on a line where there are two 1-size gaps
        # Also there is probably a faster implementation as for now time python p2.py in.txt is around 9 mins
        if union_size == MAX_X - MIN_Y - 2:
            break

    covered_positions = set()
    beacon_positions = set()
    for line in lines:
        sensor_and_beacon = tuple(int(i) for i in re.findall(r"-?\d+", line))
        sensor, beacon = sensor_and_beacon[:2], sensor_and_beacon[2:]
        sensor, beacon = sensor[::-1], beacon[::-1]
        covered_positions = covered_positions.union(compute_coverage(sensor, beacon, x))

    y = (set(range(MIN_Y, MAX_Y + 1)) - covered_positions).pop()
    print(y * TUNING_FREQ_MUL + x)
