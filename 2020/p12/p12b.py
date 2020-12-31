import math
import sys


class Boat:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, waypoint, value):
        self.x += value * waypoint.x
        self.y += value * waypoint.y


class Waypoint:
    def __init__(self, x=10, y=1):
        self.x = x
        self.y = y

    def move(self, action, value):
        if action == 'N':
            self.y += value
        elif action == 'S':
            self.y -= value
        elif action == 'E':
            self.x += value
        elif action == 'W':
            self.x -= value
        elif action == 'L':
            angle = value / 90 * math.pi / 2
            self.x, self.y = round(self.x * math.cos(angle) - self.y * math.sin(angle)), round(self.x * math.sin(angle) + self.y * math.cos(angle))
        elif action == 'R':
            angle = value / 90 * math.pi / 2
            self.x, self.y = round(self.x * math.cos(angle) + self.y * math.sin(angle)), round(-self.x * math.sin(angle) + self.y * math.cos(angle))
        else:
            raise Exception("Action: {} is not valid.".format(action))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    boat = Boat()
    wp = Waypoint()
    for instruction in l:
        action, value = instruction[0], int(instruction[1:])
        if action == 'F':
            boat.move(wp, int(instruction[1:]))
        else:
            wp.move(action, value)

print(abs(boat.x) + abs(boat.y))
