def sim(vy: int, y_target: tuple) -> (bool, int):
    y = 0
    alt = 0
    while y > y_target[1]:
        y += vy
        if vy > 0:
            alt = y
        vy -= 1
    return y_target[0] <= y <= y_target[1], alt


def run() -> None:
    y_target = (-248, -194)

    vy = y_target[1]
    max_alt = 0
    while vy <= abs(y_target[0]):
        is_reached, alt = sim(vy, y_target)
        if is_reached and alt > max_alt:
            max_alt = alt
        vy += 1

    print(max_alt)


if __name__ == "__main__":
    run()
