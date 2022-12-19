import re
import sys


# DRAFT: This version does not work. Not only it is super slow but it doesn't return the right result (even on sample
# input). Here "I" and "Elephant" are sharing the same clock which is wrong as they don't move/open at the same
# frequency.
# Explore (almost all paths) with BFS (brute-force attempt).
# This implementation works but it is quite greedy (even for sample input it takes several seconds).
# IT takes several (10) minutes for the in.txt input.
def explore(my_valve, elephant_valve, graph, time, opened, from_my_valve, from_elephant_valve):
    opened_pressure, closed_pressure = 0, 0
    max_pressure = 0
    # Needs at least 3 remaining minutes to travel, open a valve and get pressure for it
    if time < 3:
        return max_pressure
    for v1, p1 in graph[my_valve]:
        for v2, p2 in graph[elephant_valve]:
            # Try not to come back (always go forward, it may be suboptimal but would drastically reduce complexity,
            # worth trying).
            # Do not work if next move is an opening valve move.
            if v1 != from_my_valve and v2 != from_elephant_valve:
                # Move and don't open the valve
                closed_pressure = explore(v1, v2, graph, time - 1, opened, my_valve, elephant_valve)
            # Don't open a valve if it doesn't provide pressure, it is certainly a suboptimal move
            if v1 not in opened and p1 and v2 not in opened and p2 and v1 != v2:
                opened_copy = opened.copy()
                opened_copy.add(v1)
                opened_copy.add(v2)
                # Move and open the valve
                opened_pressure = (p1 + p2) * (time - 2) + explore(v1, v2, graph, time - 2, opened_copy, my_valve, elephant_valve)
            elif v1 not in opened and p1:
                opened_copy = opened.copy()
                opened_copy.add(v1)
                # Move and open the valve
                opened_pressure = p1 * (time - 2) + explore(v1, v2, graph, time - 2, opened_copy, my_valve, elephant_valve)
            elif v2 not in opened and p2:
                opened_copy = opened.copy()
                opened_copy.add(v2)
                # Move and open the valve
                opened_pressure = p2 * (time - 2) + explore(v1, v2, graph, time - 2, opened_copy, my_valve, elephant_valve)

            max_pressure = max(max_pressure, opened_pressure, closed_pressure)
    return max_pressure


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    valves_to_rates = {}
    for line in lines:
        captured_values = re.search(r"Valve ([A-Z]{2}) has flow rate=(\d+);", line)
        from_valve, rate = captured_values[1], int(captured_values[2])
        valves_to_rates[from_valve] = rate

    graph = {}
    for line in lines:
        captured_values = re.search(r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line)
        from_valve, rate, to_valve = captured_values[1], captured_values[2], captured_values[3].split(", ")
        graph[from_valve] = [(v, valves_to_rates[v]) for v in to_valve]

    my_valve = "AA"
    elephant_valve = "AA"
    time = 26
    opened = set()
    from_my_valve = None
    from_elephant_valve = None
    max_pressure = explore(my_valve, elephant_valve, graph, time, opened, from_my_valve, from_elephant_valve)
    print(max_pressure)

