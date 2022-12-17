import math
import re
import sys


X = 2000000
# For sample input
# X = 10


def compute_manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def compute_coverage(sensor, beacon, x):
    sensor_beacon_dist = compute_manhattan_dist(sensor, beacon)
    left_on_x = sensor[1] - (sensor_beacon_dist - abs(sensor[0] - x))
    right_on_x = sensor[1] + (sensor_beacon_dist - abs(sensor[0] - x))
    # Would be too greedy if we need to do that for million of lines.
    return set(range(left_on_x, right_on_x + 1))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    covered_positions = set()
    beacon_positions = set()
    for line in lines:
        sensor_and_beacon = tuple(int(i) for i in re.findall(r"-?\d+", line))
        sensor, beacon = sensor_and_beacon[:2], sensor_and_beacon[2:]
        # We use X ([0]) for rows and Y ([1]) for columns
        sensor, beacon = sensor[::-1], beacon[::-1]
        if beacon[0] == X:
            beacon_positions.add(beacon[1])
        covered_positions = covered_positions.union(compute_coverage(sensor, beacon, X))

    # The problem statement requires to remove occupied beacon_positions from the result.
    print(len(covered_positions - beacon_positions))
