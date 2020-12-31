import sys


class Boat:
    def __init__(self, x=0, y=0, direction='E'):
        self.x = x
        self.y = y
        self.direction = direction

    def apply_instruction(self, instruction):
        clockwise_directions = ('N', 'E', 'S', 'W')
        action, value = instruction[0], int(instruction[1:])
        if action == 'N':
            self.y += value
        elif action == 'S':
            self.y -= value
        elif action == 'E':
            self.x += value
        elif action == 'W':
            self.x -= value
        elif action == 'F':
            self.apply_instruction("{}{}".format(self.direction, value))
        elif action == 'L':
            self.direction = clockwise_directions[(clockwise_directions.index(self.direction) - value // 90) % 4]
        elif action == 'R':
            self.direction = clockwise_directions[(clockwise_directions.index(self.direction) + value // 90) % 4]
        else:
            raise Exception("Action: {} is not valid.".format(action))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        l = f.read().splitlines()

    boat = Boat()
    for instruction in l:
        boat.apply_instruction(instruction)

print(abs(boat.x) + abs(boat.y))
