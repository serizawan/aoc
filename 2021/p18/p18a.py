from __future__ import annotations
import logging
import sys


class SFN:
    EXPLODING_DEPTH = 4
    SPLIT_THRESH = 10
    MAGN_LEFT_COEF = 3
    MAGN_RIGHT_COEF = 2

    def __init__(self, left=None, right=None, value=None):
        self.left = left
        self.right = right
        self.value = value

    @property
    def left_magn(self) -> int:
        if self.left.is_int:
            return self.left.value
        return self.left.magnitude

    @property
    def right_magn(self) -> int:
        if self.right.is_int:
            return self.right.value
        return self.right.magnitude

    @property
    def magnitude(self) -> int:
        return SFN.MAGN_LEFT_COEF * self.left_magn + SFN.MAGN_RIGHT_COEF * self.right_magn

    @property
    def is_int(self):
        return type(self.value) == int

    def add(self, sfn: SFN) -> SFN:
        logging.debug("Add: %s + %s", self, sfn)
        wrapped_sfns = SFN(self, sfn)
        # Reduce
        while wrapped_sfns.explode() or wrapped_sfns.split():
            continue
        logging.debug("Add: %s + %s = %s", self, sfn, wrapped_sfns)
        return wrapped_sfns

    @staticmethod
    def sum(sfns: list[SFN]) -> SFN:
        if len(sfns) == 1:
            return sfns[0]
        return SFN.sum([sfns[0].add(sfns[1])] + sfns[2:])

    def explode(self) -> bool:
        return self._explode()[0]

    def _explode(self, depth=0) -> (bool, int, int):
        # if depth == 0:
        #    logging.debug("Looking for explosions in: %s", self)

        if self.is_int:
            return False, None, None

        if self.left.is_int and self.right.is_int and depth >= SFN.EXPLODING_DEPTH:
            logging.debug("Exploding: [%s, %s]", self.left.value, self.right.value)
            left_v, right_v = self.left.value, self.right.value
            self.left, self.right = None, None
            self.value = 0
            return True, left_v, right_v

        has_left_exploded, left_v, right_v = SFN._explode(self.left, depth + 1)

        if has_left_exploded:
            right_neigh = self.right
            while right_neigh.left:
                right_neigh = right_neigh.left
            right_neigh.value += right_v
            return has_left_exploded, left_v, 0

        has_right_exploded, left_v, right_v = SFN._explode(self.right, depth + 1)

        if has_right_exploded:
            left_neigh = self.left
            while left_neigh.right:
                left_neigh = left_neigh.right
            left_neigh.value += left_v
            return has_right_exploded, 0, right_v

        return False, None, None

    def split(self) -> bool:
        if self.is_int:
            if self.value >= SFN.SPLIT_THRESH:
                logging.debug("Splitting: %s", self.value)
                value = self.value
                self.value = None
                self.left = SFN(value=value // 2)
                self.right = SFN(value=value - value // 2)
                return True
            return False
        return SFN.split(self.left) or SFN.split(self.right)


    @staticmethod
    def from_str(as_str) -> int or list[SFN]:
        if ',' not in as_str:
            return SFN(value=int(as_str))

        idx = 0
        is_comma = False
        open_brackets_count = 0
        close_brackets_count = 0
        while not is_comma or open_brackets_count != close_brackets_count:
            idx += 1
            is_comma = (as_str[idx] == ",")
            if as_str[idx] == "[": open_brackets_count += 1
            if as_str[idx] == "]": close_brackets_count += 1

        left = as_str[1:idx]
        right = as_str[idx + 1:-1]
        return SFN(SFN.from_str(left), SFN.from_str(right))

    def __str__(self) -> str:
        if self.is_int:
            return str(self.value)
        return "[" + self.left.__str__() + "," + self.right.__str__() + "]"


def parse(filename) -> list[SFN]:
    sf_numbers = []
    with open(filename) as f:
        lines = f.read().splitlines()

    for line in lines:
        sf_numbers.append(SFN.from_str(line))
    return sf_numbers


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    sf_numbers = parse(sys.argv[1])
    s = SFN.sum(sf_numbers)
    print(s.magnitude)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
