import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    ts = int(l[0])
    bus_ids = [int(i) for i in l[1].split(',') if i != 'x']

    min_wait = (bus_ids[0] - (ts % bus_ids[0])) % bus_ids[0]
    min_wait_bus_id = bus_ids[0]
    for bus_id in bus_ids[1:]:
        wait = (bus_id - (ts % bus_id)) % bus_id
        if wait < min_wait:
            min_wait = wait
            min_wait_bus_id = bus_id

    print(min_wait_bus_id * min_wait)
