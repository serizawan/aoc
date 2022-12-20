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


def explore(from_v1, from_v2, t1, t2, opened):
    max_pressure = 0
    if (len(opened) == len(set(valves_to_rates.keys()))) or (t1 < 3 and t2 < 3):
        return max_pressure

    if t1 < 3:
        pressure = 0
        for to_v2 in set(valves_to_rates.keys()) - opened - {from_v1, from_v2}:
            remaining_t2 = t2 - valve_to_shortest_paths[from_v2][to_v2] - 1
            opened_copy = opened.copy()
            opened_copy.add(to_v2)
            pressure_inc_2 = remaining_t2 * valves_to_rates[to_v2]
            pressure = explore(from_v1, to_v2, t1, remaining_t2, opened_copy) + pressure_inc_2
        return max(max_pressure, pressure)

    if t2 < 3:
        pressure = 0
        for to_v1 in set(valves_to_rates.keys()) - opened - {from_v1}:
            remaining_t1 = t1 - valve_to_shortest_paths[from_v1][to_v1] - 1
            opened_copy = opened.copy()
            opened_copy.add(to_v1)
            pressure_inc_1 = remaining_t1 * valves_to_rates[to_v1]
            pressure = explore(to_v1, from_v2, remaining_t1, t2, opened_copy) + pressure_inc_1
        return max(max_pressure, pressure)

    # Move only to an unopened valve which has a > 0 rate. Try all permutations even though there are 14! since we will
    # run out of time before we reach the last valve.
    # This code is quite greedy and takes around an hour for the input.txt but it works fine!
    for to_v1 in set(valves_to_rates.keys()) - opened - {from_v1}:
        for to_v2 in set(valves_to_rates.keys()) - opened - {to_v1, from_v2}:
            remaining_t1 = t1 - valve_to_shortest_paths[from_v1][to_v1] - 1
            remaining_t2 = t2 - valve_to_shortest_paths[from_v2][to_v2] - 1
            opened_copy = opened.copy()
            opened_copy.add(to_v1)
            opened_copy.add(to_v2)
            pressure_inc_1 = remaining_t1 * valves_to_rates[to_v1]
            pressure_inc_2 = remaining_t2 * valves_to_rates[to_v2]
            pressure = explore(to_v1, to_v2, remaining_t1, remaining_t2, opened_copy) + pressure_inc_1 + pressure_inc_2
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
    for line in lines:
        captured_values = re.search(r"Valve ([A-Z]{2}) has flow rate=(\d+);", line)
        from_valve, rate = captured_values[1], int(captured_values[2])
        if rate:
            valves_to_rates[from_valve] = rate

    graph = {}
    for line in lines:
        captured_values = re.search(r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line)
        from_valve, rate, to_valve = captured_values[1], captured_values[2], captured_values[3].split(", ")
        graph[from_valve] = [(v, valves_to_rates[v]) if v in valves_to_rates else (v, 0) for v in to_valve]

    v1 = v2 = "AA"
    valve_to_shortest_paths = {valve: compute_dijkstra_shortest_paths(graph, valve) for valve in set(valves_to_rates.keys())}
    valve_to_shortest_paths[v1] = compute_dijkstra_shortest_paths(graph, v1)

    t1 = t2 = 26
    opened = set()
    max_pressure = explore(v1, v2, t1, t2, opened)
    print(max_pressure)

