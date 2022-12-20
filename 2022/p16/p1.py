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


def explore(start_valve, graph, time, opened):
    if time < 3 or len(opened) == len(valves_with_non_zero_rate):
        return 0

    max_pressure = 0
    for valve in valves_with_non_zero_rate - opened - {start_valve}:
        remaining_time = time - valve_to_shortest_paths[start_valve][valve] - 1
        opened_copy = opened.copy()
        opened_copy.add(valve)
        pressure = explore(valve, graph, remaining_time, opened_copy) + remaining_time * valves_to_rates[valve]
        max_pressure = max(max_pressure, pressure)

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
    valve_to_shortest_paths = {valve: compute_dijkstra_shortest_paths(graph, valve) for valve in valves_with_non_zero_rate}
    valve_to_shortest_paths[start_valve] = compute_dijkstra_shortest_paths(graph, start_valve)

    time = 30
    opened = set()
    max_pressure = explore(start_valve, graph, time, opened)
    print(max_pressure)

