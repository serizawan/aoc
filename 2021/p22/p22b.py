from __future__ import annotations
import logging
import sys


class Cuboid:
    ON = "on"
    OFF = "off"

    @staticmethod
    def parse_axis(axis_raw):
        axis_min, axis_max = axis_raw.split("..")
        return int(axis_min[2:]), int(axis_max)

    def __init__(self, xs, ys, zs, sign):
        self.xs = xs
        self.ys = ys
        self.zs = zs
        self.sign = sign

    @staticmethod
    def intersect_axis(axis_1, axis_2):
        left, right = max(axis_1[0], axis_2[0]), min(axis_1[1], axis_2[1])
        if left <= right:
            return left, right
        return None

    @staticmethod
    def intersect_sign(sign1, sign2):
        if sign1 == Cuboid.ON and sign2 == Cuboid.ON:
            return Cuboid.OFF
        if sign1 == Cuboid.ON and sign2 == Cuboid.OFF:
            return Cuboid.ON
        if sign1 == Cuboid.OFF and sign2 == Cuboid.ON:
            return Cuboid.OFF
        if sign1 == Cuboid.OFF and sign2 == Cuboid.OFF:
            return Cuboid.ON

    def intersect(self, cuboid):
        in_xs = Cuboid.intersect_axis(self.xs, cuboid.xs)
        in_ys = Cuboid.intersect_axis(self.ys, cuboid.ys)
        in_zs = Cuboid.intersect_axis(self.zs, cuboid.zs)
        if in_xs and in_ys and in_zs:
            return Cuboid(in_xs, in_ys, in_zs, Cuboid.intersect_sign(self.sign, cuboid.sign))
        return None

    def __str__(self):
        return f"{self.xs = }, {self.ys = }, {self.zs = }, {self.sign = }"

    @property
    def vol(self):
        abs_vol = (self.xs[1] - self.xs[0] + 1) * (self.ys[1] - self.ys[0] + 1) * (self.zs[1] - self.zs[0] + 1)
        if self.sign == Cuboid.ON:
            return abs_vol
        return -abs_vol

    def is_in_scope(self):
        is_xs_in = -50 <= self.xs[0] <= 50 and -50 <= self.xs[1] <= 50
        is_ys_in = -50 <= self.ys[0] <= 50 and -50 <= self.ys[1] <= 50
        is_zs_in = -50 <= self.zs[0] <= 50 and -50 <= self.zs[1] <= 50
        return is_xs_in and is_ys_in and is_zs_in


def parse(filename: str):
    with open(filename) as f:
        lines = f.read().splitlines()

    cuboids = []
    for line in lines:
        sign, cuboid_raw = line.split(" ")
        xs_raw, ys_raw, zs_raw = cuboid_raw.split(",")
        xs = Cuboid.parse_axis(xs_raw)
        ys = Cuboid.parse_axis(ys_raw)
        zs = Cuboid.parse_axis(zs_raw)
        cuboid = Cuboid(xs, ys, zs, sign)
        cuboids.append(cuboid)
    return cuboids


def run() -> None:
    if len(sys.argv) != 2:
        logging.error("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]))
        sys.exit()

    cuboids = parse(sys.argv[1])
    processed_cuboids = []
    for cuboid in cuboids:
        cuboids_to_append = []
        if cuboid.sign == Cuboid.ON:
            cuboids_to_append.append(cuboid)
        for processed_cuboid in processed_cuboids:
            if in_cuboid := cuboid.intersect(processed_cuboid):
                cuboids_to_append.append(in_cuboid)
        processed_cuboids += cuboids_to_append

    print(sum(c.vol for c in processed_cuboids))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
