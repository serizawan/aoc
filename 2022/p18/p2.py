from collections import defaultdict
from copy import deepcopy
from enum import Enum
import sys


CUBE_FACES = 6


class Directions(Enum):
    FRONT = (1, 0, 0)
    BACK = (-1, 0, 0)
    LEFT = (0, -1, 0)
    RIGHT = (0, 1, 0)
    UP = (0, 0, 1)
    DOWN = (0, 0, -1)


class Item:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    @property
    def neighbors(self):
        _neighbors = set()
        for direction in Directions:
            droplet = Droplet(self.x + direction.value[0], self.y + direction.value[1], self.z + direction.value[2])
            _neighbors.add(droplet)

        return _neighbors

    def inside(self, region):
        return region[0] <= self.x <= region[1] and region[2] <= self.y <= region[3] and region[4] <= self.z <= region[5]


class Air(Item):
    pass


class Droplet(Item):
    pass


class Border:
    def __init__(self, droplets_to_counts):
        self.inside_droplets = set()
        self.droplets_to_counts = droplets_to_counts
        self.free_air = set()
        self.trapped_air = set()

    def update(self, droplet):
        self.inside_droplets.add(droplet)
        # Droplet is always in droplets_to_counts at this point since we accessed it as droplets_to_counts[droplet] on
        # a defaultdict!
        self.droplets_to_counts.pop(droplet)
        for neighbor in droplet.neighbors:
            if neighbor not in self.inside_droplets:
                self.droplets_to_counts[neighbor] += 1

    def expand(self, airs, region):
        airs_copy = deepcopy(airs)
        for air in airs_copy:
            for neighbor in air.neighbors:
                if neighbor.inside(region) and neighbor not in self.inside_droplets:
                    airs.add(neighbor)

        if len(airs) == len(airs_copy):
            return

        self.expand(airs, region)

    def compute_trapped_air(self):
        _inside_droplets = self.inside_droplets
        min_x, max_x = min(droplet.x for droplet in _inside_droplets), max(droplet.x for droplet in _inside_droplets)
        min_y, max_y = min(droplet.y for droplet in _inside_droplets), max(droplet.y for droplet in _inside_droplets)
        min_z, max_z = min(droplet.z for droplet in _inside_droplets), max(droplet.z for droplet in _inside_droplets)
        region = (min_x - 1, max_x + 1, min_y - 1, max_y + 1, min_z - 1, max_z + 1)
        region_items = set(Item(i, j, k) for i in range(region[0], region[1] + 1) for j in range(region[2], region[3] + 1) for k in range(region[4], region[5] + 1))
        self.free_air = {Air(max_x + 1, max_y + 1, max_z + 1)}
        self.expand(self.free_air, region)
        self.trapped_air = region_items - self.inside_droplets - self.free_air


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    droplets = []
    for line in lines:
        droplets.append(Droplet(*(int(i) for i in line.split(","))))

    # Compute the total droplets surface area.
    surface_area = 0
    border = Border(defaultdict(lambda: 0))
    for droplet in droplets:
        # Remove border.droplets_to_counts[droplet] twice (once for the current droplet and once for the neighbors).
        surface_area += CUBE_FACES - 2 * border.droplets_to_counts[droplet]
        border.update(droplet)

    # Compute the trapped air surface area.
    border.compute_trapped_air()
    air_surface_area = 0
    air_border = Border(defaultdict(lambda: 0))
    for air in border.trapped_air:
        air_surface_area += CUBE_FACES - 2 * air_border.droplets_to_counts[air]
        air_border.update(air)

    # The external surface area is given by the difference between total droplets surface area and trapped air surface
    # area.
    print(surface_area - air_surface_area)



