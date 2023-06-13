from collections import defaultdict
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


class Droplet:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return isinstance(other, Droplet) and self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    @property
    def neighbors(self):
        _neighbors = set()
        for direction in Directions:
            droplet = Droplet(self.x + direction.value[0], self.y + direction.value[1], self.z + direction.value[2])
            _neighbors.add(droplet)

        return _neighbors


class Border:
    def __init__(self, droplets_to_counts):
        self.inside_droplets = set()
        self.droplets_to_counts = droplets_to_counts

    def update(self, droplet):
        self.inside_droplets.add(droplet)
        # Droplet is always in droplets_to_counts at this point since we accessed it as droplets_to_counts[droplet] on
        # a defaultdict!
        self.droplets_to_counts.pop(droplet)
        for neighbor in droplet.neighbors:
            if neighbor not in self.inside_droplets:
                self.droplets_to_counts[neighbor] += 1


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

    surface_area = 0
    border = Border(defaultdict(lambda: 0))
    for droplet in droplets:
        # Remove border.droplets_to_counts[droplet] twice (once for the current droplet and once for the neighbors).
        surface_area += CUBE_FACES - 2 * border.droplets_to_counts[droplet]
        border.update(droplet)

    print(surface_area)



