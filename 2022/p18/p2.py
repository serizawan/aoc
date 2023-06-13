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


class Region:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1, self.x2 = x1, x2
        self.y1, self.y2 = y1, y2
        self.z1, self.z2 = z1, z2


class Item:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # Note that an air instance and a droplet instance are equal if they occupy the same position in space.
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    @property
    def neighbors(self):
        _neighbors = set()
        for direction in Directions:
            item = Item(self.x + direction.value[0], self.y + direction.value[1], self.z + direction.value[2])
            _neighbors.add(item)

        return _neighbors

    def is_in(self, region):
        return (region.x1 <= self.x <= region.x2 and
                region.y1 <= self.y <= region.y2 and
                region.z1 <= self.z <= region.z2)

    def __str__(self):
        return f"{self.x=}, {self.y=}, {self.z=}"


class Air(Item):
    pass


class Droplet(Item):
    pass


class ItemsCloud:
    def __init__(self, items):
        self.items = set(items)

    def update(self, item, border):
        # Item is always in border at this point since we accessed it as border[item] on a defaultdict!
        border.pop(item)
        for neighbor in item.neighbors:
            border[neighbor] += 1

    def expand(self, items, region):
        items_copy = deepcopy(items)
        for item in items_copy:
            for neighbor in item.neighbors:
                if neighbor.is_in(region) and neighbor not in self.items:
                    items.add(neighbor)

        if len(items) == len(items_copy):
            return

        self.expand(items, region)

    """
    Compute trapped items.
    Trapped items are identified by:
    1) Taking a region larger (by 1 in all directions) than the items occupied space
    2) Computing non-trapped items (pick a region border item which is free and expand it inside the region until it 
    remains identical. The expanded item set captures all "free" (outer) items within the region.
    3) Subtract given items and free items from region. The remaining set gathers the trapped items.
    
    Note: Expanding the item until it cannot anymore is the costly operation of this problem.
    There is space to optimize the behavior by expanding only non-yet expanded items at each round ("border" items).
    Example: https://github.com/hyper-neutrino/advent-of-code/blob/main/2022/day18p2.py#L41
    """
    def compute_trapped(self):
        _items = self.items
        min_x, max_x = min(item.x for item in _items), max(item.x for item in _items)
        min_y, max_y = min(item.y for item in _items), max(item.y for item in _items)
        min_z, max_z = min(item.z for item in _items), max(item.z for item in _items)
        region = Region(min_x - 1, max_x + 1, min_y - 1, max_y + 1, min_z - 1, max_z + 1)
        region_items = set()
        for i in range(region.x1, region.x2 + 1):
            for j in range(region.y1, region.y2 + 1):
                for k in range(region.z1, region.z2 + 1):
                    region_items.add(Item(i, j, k))
        # To identify the o
        outside = {Item(max_x + 1, max_y + 1, max_z + 1)}
        self.expand(outside, region)
        return region_items - self.items - outside

    def compute_surface_area(self):
        surface_area = 0
        border = defaultdict(lambda: 0)
        for item in self.items:
            # Subtract self.border[item] twice (once for the current item hidden faces and once for the neighbors
            # hidden faces).
            surface_area += CUBE_FACES - 2 * border[item]
            self.update(item, border)
        return surface_area


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
    droplet_items_cloud = ItemsCloud(droplets)
    droplet_surface_area = droplet_items_cloud.compute_surface_area()

    # Compute the trapped air surface area.
    air_items_cloud = ItemsCloud(droplet_items_cloud.compute_trapped())
    air_surface_area = air_items_cloud.compute_surface_area()

    # The droplets outside surface area is given by the difference between droplets surface area and trapped air surface
    # area.
    print(droplet_surface_area - air_surface_area)
