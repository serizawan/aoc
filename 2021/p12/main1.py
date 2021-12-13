from __future__ import annotations
import sys


class Cave:
    def __init__(self, id: str, neighbors: set[Cave]) -> None:
        self.id = id
        self.neighbors = neighbors

    @property
    def is_big(self) -> bool:
        return self.id.upper() == self.id

    def __str__(self):
        return self.id + ' (' + ', '.join([n.id for n in self.neighbors]) + ')'


class CaveMap:
    START = 'start'
    END = 'end'

    def __init__(self, caves: dict[str, Cave]) -> None:
        self.caves = caves

    @property
    def start_cave(self) -> Cave:
        return self.caves['start']

    def explore(self, cave: Cave, visited: list[Cave], path_count: int) -> int:
        if cave.id == 'end':
            return path_count + 1
        elif not (visitable := cave.neighbors - set([v for v in visited if not v.is_big])):
            return path_count
        else:
            while visitable:
                next_cave = visitable.pop()
                visited.append(next_cave)
                path_count = self.explore(next_cave, visited, path_count)
                visited.pop()
            return path_count


def parse(filename) -> CaveMap:
    with open(filename) as f:
        lines = f.read().splitlines()

    cave_map = CaveMap({})
    for line in lines:
        id1, id2 = line.split('-')
        cave1 = cave_map.caves.get(id1)
        cave2 = cave_map.caves.get(id2)
        if not cave1:
            cave1 = Cave(id1, set())
            cave_map.caves[id1] = cave1
        if not cave2:
            cave2 = Cave(id2, set())
            cave_map.caves[id2] = cave2
        cave1.neighbors.add(cave2)
        cave2.neighbors.add(cave1)
    return cave_map


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    cave_map = parse(sys.argv[1])

    path_count = cave_map.explore(cave_map.start_cave, [cave_map.start_cave], 0)
    print(path_count)


if __name__ == "__main__":
    run()
