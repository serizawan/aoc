import re
import sys


# Explore with BFS
# This implementation works but is too greedy (even for sample input it takes several minutes).
def explore(start_valve, graph, time, opened, from_valve):
    opened_pressure, closed_pressure = 0, 0
    max_pressure = 0
    # Needs at least 3 remaining minute to travel, open a valve and get pressure for it
    if time < 3:
        return max_pressure
    for valve, pressure in graph[start_valve]:
        if valve != from_valve:
            # Move and don't open the valve
            closed_pressure = explore(valve, graph, time - 1, opened, start_valve)
        if valve not in opened:
            opened_copy = opened.copy()
            opened_copy.add(valve)
            # Move and open the valve
            opened_pressure = pressure * (time - 2) + explore(valve, graph, time - 2, opened_copy, from_valve)

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

    start_valve = "AA"
    time = 30
    opened = set()
    from_valve = None
    max_pressure = explore(start_valve, graph, time, opened, from_valve)
    print(max_pressure)

