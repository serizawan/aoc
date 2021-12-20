def sim(vx: int, vy: int, x_target: tuple, y_target: tuple) -> (bool, int):
    x, y = 0, 0
    has_reached = False
    while x < x_target[1] and y > y_target[0]:
        x += vx
        vx = vx - 1 if vx > 0 else 0
        y += vy
        vy -= 1
        has_reached = has_reached or (x_target[0] <= x <= x_target[1] and y_target[0] <= y <= y_target[1])
    return has_reached


def run() -> None:
    # x_target = (20, 30)
    # y_target = (-10, -5)
    x_target = (29, 73)
    y_target = (-248, -194)

    vx = 0
    vy = y_target[0]
    count = 0
    for i in range(x_target[1] + 1):
        for j in range(2 * abs(y_target[0]) + 1):
            has_reached = sim(vx + i, vy + j, x_target, y_target)
            if has_reached:
                count += 1

    print(count)


if __name__ == "__main__":
    run()
