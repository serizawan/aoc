import re
import sys


TIME_OVER = 24


"""
This version is sub-optimal. Here we try to produce always ore robots first, then clay robots, then obsidian robots and
finally geode ones.

But blueprint 1 provides a counter-example of this strategy since we reach 8 geodes with this implementation while
by making a clay robot after an obsidian we can get up to 9 geodes.
"""


class Cost:
    def __init__(self, ore, clay, obsidian, geode):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode


class RobotTypes:
    ORE_TYPE = 0
    CLAY_TYPE = 1
    OBSIDIAN_TYPE = 2
    GEODE_TYPE = 3


class RobotsTarget:
    MAX_ROBOTS_PER_TYPE = 10

    def __init__(self, ore_robots, clay_robots, obsidian_robots):
        self.ore_robots = ore_robots
        self.clay_robots = clay_robots
        self.obsidian_robots = obsidian_robots

    def next(self, is_reached):
        if self.ore_robots != self.MAX_ROBOTS_PER_TYPE:
            self.ore_robots += 1
            return False
        else:
            if self.clay_robots != self.MAX_ROBOTS_PER_TYPE:
                self.ore_robots = 1
                self.clay_robots += 1
                return False
            elif self.obsidian_robots != self.MAX_ROBOTS_PER_TYPE:
                self.obsidian_robots += 1
                self.ore_robots = 1
                self.clay_robots = 1
                return False
            else:
                return True

        # This version doesn't test all reachable target (such as 1 2 2).
        # if is_reached:
        #     self.ore_robots += 1
        #     return False
        # else:
        #     if self.ore_robots != 1:
        #         self.ore_robots = 1
        #         self.clay_robots += 1
        #         return False
        #     else:
        #         if self.clay_robots != 1:
        #             self.clay_robots = 1
        #             self.obsidian_robots += 1
        #             return False
        #         else:
        #             return True


class RobotFactory:
    def __init__(self, last_robot_id, robots, blueprint_id, resources, ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost):
        self.last_robot_id = last_robot_id
        self.robots = robots
        self.blueprint_id = blueprint_id
        self.resources = resources
        self.ore_robot_cost = ore_robot_cost
        self.clay_robot_cost = clay_robot_cost
        self.obsidian_robot_cost = obsidian_robot_cost
        self.geode_robot_cost = geode_robot_cost

    def make(self, robot_type):
        self.last_robot_id += 1
        if robot_type == RobotTypes.ORE_TYPE:
            self.resources.spend(self.ore_robot_cost)
            robot = OreRobot(self.last_robot_id)
        elif robot_type == RobotTypes.CLAY_TYPE:
            self.resources.spend(self.clay_robot_cost)
            robot = ClayRobot(self.last_robot_id)
        elif robot_type == RobotTypes.OBSIDIAN_TYPE:
            self.resources.spend(self.obsidian_robot_cost)
            robot = ObsidianRobot(self.last_robot_id)
        else:
            self.resources.spend(self.geode_robot_cost)
            robot = GeodeRobot(self.last_robot_id)
        return robot

    def has_enough(self, robot_type):
        if robot_type == RobotTypes.ORE_TYPE:
            return self.resources.ore_stock >= self.ore_robot_cost.ore
        if robot_type == RobotTypes.CLAY_TYPE:
            return self.resources.ore_stock >= self.clay_robot_cost.ore
        if robot_type == RobotTypes.OBSIDIAN_TYPE:
            return self.resources.ore_stock >= self.obsidian_robot_cost.ore and self.resources.clay_stock >= self.obsidian_robot_cost.clay
        if robot_type == RobotTypes.GEODE_TYPE:
            return self.resources.ore_stock >= self.geode_robot_cost.ore and self.resources.obsidian_stock >= self.geode_robot_cost.obsidian
        return False

    def simulate(self, robots_target):
        remaining_time = TIME_OVER
        while remaining_time and robots_target.ore_robots != self.robots.count(RobotTypes.ORE_TYPE):
            robot = None
            if self.has_enough(RobotTypes.ORE_TYPE):
                robot = self.make(RobotTypes.ORE_TYPE)
            self.robots.produce()
            if robot:
                self.robots.robots_set.add(robot)
            remaining_time -= 1

        while remaining_time and robots_target.clay_robots != self.robots.count(RobotTypes.CLAY_TYPE):
            robot = None
            if self.has_enough(RobotTypes.CLAY_TYPE):
                robot = robot_factory.make(RobotTypes.CLAY_TYPE)
            self.robots.produce()
            if robot:
                self.robots.robots_set.add(robot)
            remaining_time -= 1

        while remaining_time and robots_target.obsidian_robots != self.robots.count(RobotTypes.OBSIDIAN_TYPE):
            robot = None
            if self.has_enough(RobotTypes.OBSIDIAN_TYPE):
                robot = self.make(RobotTypes.OBSIDIAN_TYPE)
            self.robots.produce()
            if robot:
                self.robots.robots_set.add(robot)
            remaining_time -= 1

        while remaining_time:
            robot = None
            if self.has_enough(RobotTypes.GEODE_TYPE):
                robot = self.make(RobotTypes.GEODE_TYPE)
            self.robots.produce()
            if robot:
                self.robots.robots_set.add(robot)
            remaining_time -= 1

        return (robots_target.ore_robots == self.robots.count(RobotTypes.ORE_TYPE) and
                robots_target.clay_robots == self.robots.count(RobotTypes.CLAY_TYPE) and
                robots_target.obsidian_robots == self.robots.count(RobotTypes.OBSIDIAN_TYPE)
                )


class Resources:
    def __init__(self, ore_stock, clay_stock, obsidian_stock, geode_stock):
        self.ore_stock = ore_stock
        self.clay_stock = clay_stock
        self.obsidian_stock = obsidian_stock
        self.geode_stock = geode_stock

    def spend(self, cost):
        self.ore_stock -= cost.ore
        self.clay_stock -= cost.clay
        self.obsidian_stock -= cost.obsidian
        self.geode_stock -= cost.geode


class Robot:
    def __init__(self, robot_id):
        self.robot_id = robot_id

    def __eq__(self, other):
        return self.robot_id == other.robot_id

    def __hash__(self):
        return self.robot_id


class OreRobot(Robot):
    ORE_PRODUCTION = 1

    def produce(self):
        robot_factory.resources.ore_stock += self.ORE_PRODUCTION


class ClayRobot(Robot):
    CLAY_PRODUCTION = 1

    def produce(self):
        robot_factory.resources.clay_stock += self.CLAY_PRODUCTION


class ObsidianRobot(Robot):
    OBSIDIAN_PRODUCTION = 1

    def produce(self):
        robot_factory.resources.obsidian_stock += self.OBSIDIAN_PRODUCTION


class GeodeRobot(Robot):
    GEODE_PRODUCTION = 1

    def produce(self):
        robot_factory.resources.geode_stock += self.GEODE_PRODUCTION


class Robots:
    def __init__(self, robots_set):
        self.robots_set = robots_set

    def count(self, robot_type):
        count = 0
        for robot in self.robots_set:
            if robot_type == RobotTypes.ORE_TYPE and isinstance(robot, OreRobot):
                count += 1
            elif robot_type == RobotTypes.CLAY_TYPE and isinstance(robot, ClayRobot):
                count += 1
            elif robot_type == RobotTypes.OBSIDIAN_TYPE and isinstance(robot, ObsidianRobot):
                count += 1
            elif robot_type == RobotTypes.GEODE_TYPE and isinstance(robot, GeodeRobot):
                count += 1
        return count

    def produce(self):
        for robot in self.robots_set:
            robot.produce()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    result = 0
    for line in lines:
        blueprint_id, *costs = re.findall(r"\d+", line)
        costs = [int(cost) for cost in costs]
        robots_target = RobotsTarget(1, 1, 1)
        is_over = False
        max_geode_stock = 0
        while not is_over:
            robot_factory = RobotFactory(0,
                                         Robots({OreRobot(0)}),
                                         blueprint_id,
                                         Resources(0, 0, 0, 0),
                                         Cost(costs[0], 0, 0, 0),
                                         Cost(costs[1], 0, 0, 0),
                                         Cost(costs[2], costs[3], 0, 0),
                                         Cost(costs[4], 0, costs[5], 0),
                                         )
            is_reached = robot_factory.simulate(robots_target)
            max_geode_stock = max(robot_factory.resources.geode_stock, max_geode_stock)
            is_over = robots_target.next(is_reached)
        result += int(blueprint_id) * max_geode_stock

    print(result)