from __future__ import annotations
from copy import deepcopy
import logging
import sys


def add_frame(img: list[list[str]], pxl: str) -> list[list[str]]:
    img = [[pxl] + line + [pxl] for line in img]
    top_or_bottom_line = [pxl] * len(img[0])
    img.insert(0, top_or_bottom_line)
    img.append(top_or_bottom_line)
    return img


def switch_frame(img: list[list[str]]) -> list[list[str]]:
    c = "#" if img[0][0] == "." else "."
    top_or_bottom_line = [c] * len(img[0])
    img[0] = top_or_bottom_line
    img[-1] = top_or_bottom_line
    for line in img[1:-1]:
        line[0] = c
        line[-1] = c
    return img


def apply(iea, img, surrounding_pxl):
    img = add_frame(img, surrounding_pxl)
    img_copy = deepcopy(img)
    for i, line in enumerate(img[1:-1]):
        for j, _ in enumerate(line[1:-1]):
            area = "".join(img[i][j:j + 3] + img[i + 1][j:j + 3] + img[i + 2][j:j + 3])
            idx = to_idx(area)
            img_copy[i + 1][j + 1] = iea[idx]

    if iea[0] == "#":
        return switch_frame(img_copy)
    return img_copy


def to_idx(area: str) -> int:
    bin_repr = ["0" if c == "." else "1" for c in area]
    bin_repr = "".join(bin_repr)
    return int(bin_repr, 2)


def parse(filename: str) -> tuple[str, list[list]]:
    with open(filename) as f:
        lines = f.read().splitlines()

    iea = lines[0]
    img = [list(line) for line in lines[2:]]
    return iea, img


def print_img(img):
    for line in img:
        print("".join(line))
    print()


def run() -> None:
    if len(sys.argv) != 2:
        logging.error("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]))
        sys.exit()

    iea, img = parse(sys.argv[1])
    img = add_frame(img, ".")

    n_rounds = 50
    surrounding_pxl = "."
    for i in range(n_rounds):
        img = apply(iea, img, surrounding_pxl)
        surrounding_pxl = "#" if surrounding_pxl == "." and iea[0] == "#" else "."

    print("".join(["".join(line) for line in img]).count("#"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
