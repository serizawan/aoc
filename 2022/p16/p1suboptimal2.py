from collections import defaultdict
import heapq
import math
import re
import sys


DEFAULT_COST = 1


def compute_dijkstra_shortest_paths(graph, start_node):
    visited = defaultdict(lambda: math.inf)
    unvisited = defaultdict(lambda: math.inf)
    unvisited[start_node] = 0
    heap = [(0, start_node)]
    while heap:
        current_distance, node = heapq.heappop(heap)
        if node not in visited:
            for neighbour, _ in graph[node]:
                # Replace DEFAULT_COST by _ if nodes are carrying their distance to start_node.
                # Here they store pressure rate (not related to Dijkstra computation).
                node_distance = current_distance + DEFAULT_COST
                if neighbour not in visited and node_distance < unvisited[neighbour]:
                    unvisited[neighbour] = node_distance
                    heapq.heappush(heap, (node_distance, neighbour))
            visited[node] = current_distance
            unvisited.pop(node)
    return visited


# Another sub-optimal algorithm where we go the closest neighbors and either open or let it close it before we move on.
# We also don't come back from a closed neighbor but it is not legit to ignore this situation.
def explore(start_valve, graph, time, opened, from_closed):
    max_pressure = 0
    # Needs at least 3 remaining minute to travel, open a valve and get pressure for it
    # Also return if there are no more valves to open.
    if time < 3 or len(opened) == len(valves_with_non_zero_rate):
        return max_pressure
    shortest_paths = compute_dijkstra_shortest_paths(graph, start_valve)
    targeted_valves = list(valves_with_non_zero_rate - opened - {start_valve} - {from_closed})
    if targeted_valves:
        closest_valves = [valve for valve in targeted_valves if shortest_paths[valve] == min([shortest_paths[v] for v in targeted_valves])]
        for valve in closest_valves:
            opened_copy = opened.copy()
            opened_copy.add(valve)
            opened_pressure = explore(valve, graph, time - shortest_paths[valve] - 1, opened_copy, None) + valves_to_rates[valve] * (time - shortest_paths[valve] - 1)
            closed_pressure = explore(valve, graph, time - shortest_paths[valve], opened, start_valve)
            max_pressure = max(max_pressure, opened_pressure, closed_pressure)
    # There is a single remaining valve and we are on it, so open it.
    else:
        max_pressure = valves_to_rates[start_valve] * (time - 1)
    return max_pressure


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    valves_to_rates = {}
    valves_with_non_zero_rate = set()
    for line in lines:
        captured_values = re.search(r"Valve ([A-Z]{2}) has flow rate=(\d+);", line)
        from_valve, rate = captured_values[1], int(captured_values[2])
        valves_to_rates[from_valve] = rate
        if rate:
            valves_with_non_zero_rate.add(from_valve)

    graph = {}
    for line in lines:
        captured_values = re.search(r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line)
        from_valve, rate, to_valve = captured_values[1], captured_values[2], captured_values[3].split(", ")
        graph[from_valve] = [(v, valves_to_rates[v]) for v in to_valve]

    start_valve = "AA"
    time = 30
    opened = set()
    from_valve = None
    max_pressure = explore(start_valve, graph, time, opened, None)
    print(max_pressure)

