from __future__ import annotations
from copy import deepcopy
import logging
import sys


def minus(v):
    return [-x_i for x_i in v]


def vect(u, v):
    return (
        + (u[1] * v[2] - v[1] * u[2]),
        - (u[0] * v[2] - v[0] * u[2]),
        + (u[0] * v[1] - v[0] * u[1]),
    )


def scal(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def _rotate(p, u, v, w):
    return scal(p, u), scal(p, v), scal(p, w)


def taxicab(vec):
    return sum(abs(x_i) for x_i in vec)


class Base:
    U = [1, 0, 0]
    V = [0, 1, 0]
    W = [0, 0, 1]

    VEC_U_V = [
        (U, V), (U, minus(V)), (minus(U), V), (minus(U), minus(V)),
        (U, W), (U, minus(W)), (minus(U), W), (minus(U), minus(W)),
        (V, U), (V, minus(U)), (minus(V), U), (minus(V), minus(U)),
        (V, W), (V, minus(W)), (minus(V), W), (minus(V), minus(W)),
        (W, U), (W, minus(U)), (minus(W), U), (minus(W), minus(U)),
        (W, V), (W, minus(V)), (minus(W), V), (minus(W), minus(V)),
    ]
    bases = [(u, v, vect(u, v)) for u, v in VEC_U_V]


class Scanner:
    MIN_SCAN_OVERLAP = 12
    RANGE = 1000

    def __init__(self, uid: int, beacons: set[tuple[int]]):
        self.uid = uid
        self.beacons = beacons

    def rotate(self, base):
        self.beacons = {_rotate(beacon, *base) for beacon in self.beacons}

    def translate(self, u, v, w, x, y, z):
        self.beacons = {(beacon[0] - u + x, beacon[1] - v + y, beacon[2] - w + z) for beacon in self.beacons}

    def does_overlap(self, scanner) -> bool:
        overlap_len = len(self.beacons.intersection(scanner.beacons))
        return overlap_len >= Scanner.MIN_SCAN_OVERLAP

    def does_overlap_in_any_position(self, scanner):
        for base in Base.bases:
            scanner_copy = deepcopy(scanner)
            scanner_copy.rotate(base)
            for beacon in self.beacons:
                for _beacon in scanner_copy.beacons:
                    scanner_copy_copy = deepcopy(scanner_copy)
                    scanner_copy_copy.translate(*_beacon, *beacon)
                    translation = [b - _beacon[i] for i, b in enumerate(beacon)]
                    if self.does_overlap(scanner_copy_copy):
                        logging.debug("Scanner %d overlaps with scanner %d", self.uid, scanner_copy_copy.uid)
                        return translation, scanner_copy_copy, True
        return None, None, False


def parse(filename: str) -> list[Scanner]:
    with open(filename) as f:
        lines = f.read().splitlines()
    scanners = []
    uid = 0
    while lines:
        lines = lines[1:]
        beacons = set()
        line = lines.pop(0)
        while line:
            beacons.add(tuple(int(i) for i in line.split(",")))
            line = lines.pop(0) if lines else None
        scanners.append(Scanner(uid, beacons))
        uid += 1
    return scanners


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    scanners = parse(sys.argv[1])

    translation = None
    translations = []
    while len(scanners) > 1:
        overlap = False
        i = 0
        scanner = None
        while not overlap:
            i += 1
            translation, scanner, overlap = scanners[0].does_overlap_in_any_position(scanners[i])
        scanners[0].beacons = scanners[0].beacons.union(scanner.beacons)
        translations.append(translation)
        scanners.pop(i)

    max_taxicab = max(taxicab(t) for t in translations)
    for v in translations:
        for w in translations:
            v_minus_w = [v[i] - w_i for i, w_i in enumerate(w)]
            max_taxicab = max(max_taxicab, taxicab(v_minus_w))

    print(max_taxicab)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
