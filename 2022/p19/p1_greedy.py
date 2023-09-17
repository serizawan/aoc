from copy import deepcopy
import math
from enum import Enum
import re
import sys


ALLOCATED_TIME = 24


"""
This version simulates geode productions for all possible permutations of buildable robots sets (in the allocated time).
Despite some thresholds have been put on the number of buildable robots per type have been set (example: Considering the
Ore robot costs in the input blueprints, it never makes sense to build more than 4 Ore robots to reach the maximum geode
production as no robots costs more than 4 ores. Having more Ore robots would spoil resources with over-production of 
this metal).

With 4 Ore Robots, 8 Clay Robots, 4 Obsidian Robots and 2 Geode Robots (which is a buildable set for some blueprints),
there are more than 18! / (4! * 8! * 4! * 2!) = 137 837 700 possible permutations which wouldn't be computable in a
reasonable time (maximum a few minutes).
"""


class Cost:
    def __init__(self, ore, clay, obsidian, geode):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode


class RobotTypes(Enum):
    ORE_TYPE = 0
    CLAY_TYPE = 1
    OBSIDIAN_TYPE = 2
    GEODE_TYPE = 3

    @staticmethod
    def get_robot_class_from_robot_type(robot_type):
        if robot_type == RobotTypes.ORE_TYPE:
            return OreRobot
        elif robot_type == RobotTypes.CLAY_TYPE:
            return ClayRobot
        elif robot_type == RobotTypes.OBSIDIAN_TYPE:
            return ObsidianRobot
        elif robot_type == RobotTypes.GEODE_TYPE:
            return GeodeRobot


class BluePrint:
    def __init__(self, blue_print_id, ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost):
        self.blue_print_id = blue_print_id
        self.ore_robot_cost = ore_robot_cost
        self.clay_robot_cost = clay_robot_cost
        self.obsidian_robot_cost = obsidian_robot_cost
        self.geode_robot_cost = geode_robot_cost


class RobotFactory:

    def __init__(self, last_robot_id, robots, blue_print, resources, next_robot_type_to_make):
        self.last_robot_id = last_robot_id
        self.robots = robots
        self.blue_print = blue_print
        self.resources = resources
        self.next_robot_type_to_make = next_robot_type_to_make

    def make(self, robot_type):
        self.last_robot_id += 1
        if robot_type == RobotTypes.ORE_TYPE:
            self.resources.spend(self.blue_print.ore_robot_cost)
            robot = OreRobot(self.last_robot_id)
        elif robot_type == RobotTypes.CLAY_TYPE:
            self.resources.spend(self.blue_print.clay_robot_cost)
            robot = ClayRobot(self.last_robot_id)
        elif robot_type == RobotTypes.OBSIDIAN_TYPE:
            self.resources.spend(self.blue_print.obsidian_robot_cost)
            robot = ObsidianRobot(self.last_robot_id)
        else:
            self.resources.spend(self.blue_print.geode_robot_cost)
            robot = GeodeRobot(self.last_robot_id)
        return robot

    def has_enough(self, robot_type):
        if robot_type == RobotTypes.ORE_TYPE:
            return self.resources.ore_stock >= self.blue_print.ore_robot_cost.ore
        if robot_type == RobotTypes.CLAY_TYPE:
            return self.resources.ore_stock >= self.blue_print.clay_robot_cost.ore
        if robot_type == RobotTypes.OBSIDIAN_TYPE:
            return self.resources.ore_stock >= self.blue_print.obsidian_robot_cost.ore and self.resources.clay_stock >= self.blue_print.obsidian_robot_cost.clay
        if robot_type == RobotTypes.GEODE_TYPE:
            return self.resources.ore_stock >= self.blue_print.geode_robot_cost.ore and self.resources.obsidian_stock >= self.blue_print.geode_robot_cost.obsidian
        return False

    def simulate(self, remaining_time, max_geode_stock):
        if not self.next_robot_type_to_make:
            for robot_type in RobotTypes:
                robot_factory = deepcopy(self)
                robot_factory.next_robot_type_to_make = robot_type
                max_geode_stock = max(robot_factory.simulate(remaining_time, max_geode_stock), max_geode_stock)
            return max_geode_stock

        while remaining_time:
            remaining_time -= 1
            if self.has_enough(self.next_robot_type_to_make):
                robot = self.make(self.next_robot_type_to_make)
                self.resources.add(self.robots.produce())
                self.robots.robots_set.add(robot)
                for robot_type in RobotTypes:
                    if self.robots.count(robot_type) >= RobotTypes.get_robot_class_from_robot_type(robot_type).MAX_ROBOT_COUNT:
                        continue
                    robot_factory = deepcopy(self)
                    robot_factory.next_robot_type_to_make = robot_type
                    max_geode_stock = robot_factory.simulate(remaining_time, max(robot_factory.resources.geode_stock, max_geode_stock))
            else:
                self.resources.add(self.robots.produce())

        return max(self.resources.geode_stock, max_geode_stock)


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

    def add(self, resources):
        self.ore_stock += resources.ore_stock
        self.clay_stock += resources.clay_stock
        self.obsidian_stock += resources.obsidian_stock
        self.geode_stock += resources.geode_stock


class Robot:
    MAX_ROBOT_COUNT = math.inf

    def __init__(self, robot_id):
        self.robot_id = robot_id

    def __eq__(self, other):
        return self.robot_id == other.robot_id

    def __hash__(self):
        return self.robot_id


class OreRobot(Robot):
    ORE_PRODUCTION = 1
    MAX_ROBOT_COUNT = 4

    def produce(self):
        return Resources(self.ORE_PRODUCTION, 0, 0, 0)


class ClayRobot(Robot):
    CLAY_PRODUCTION = 1
    MAX_ROBOT_COUNT = 8

    def produce(self):
        return Resources(0, self.CLAY_PRODUCTION, 0, 0)


class ObsidianRobot(Robot):
    OBSIDIAN_PRODUCTION = 1
    MAX_ROBOT_COUNT = 4

    def produce(self):
        return Resources(0, 0, self.OBSIDIAN_PRODUCTION, 0)


class GeodeRobot(Robot):
    GEODE_PRODUCTION = 1

    def produce(self):
        return Resources(0, 0, 0, self.GEODE_PRODUCTION)


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
        resources = Resources(0, 0, 0, 0)
        for robot in self.robots_set:
            resources.add(robot.produce())
        return resources


if __name__ == "__main__":
    GLOBAL_COUNT = 0

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
        remaining_time = ALLOCATED_TIME
        blue_print = BluePrint(
            blueprint_id,
            Cost(costs[0], 0, 0, 0),
            Cost(costs[1], 0, 0, 0),
            Cost(costs[2], costs[3], 0, 0),
            Cost(costs[4], 0, costs[5], 0),
        )
        robot_factory = RobotFactory(
            0,
            Robots({OreRobot(0)}),
            blue_print,
            Resources(0, 0, 0, 0),
            None,
        )
        max_geode_stock = robot_factory.simulate(ALLOCATED_TIME, 0, 0)
        print(max_geode_stock)
        result += int(blueprint_id) * max_geode_stock

    print(result)
