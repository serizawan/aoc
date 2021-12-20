def run() -> None:
    y_target = (-248, -194)

    # Whatever the initial positive vy velocity, the probe will get back to alt 0 with the opposite vy velocity
    # The velocity can't go over abs(y_target[0]) if not the probe would go beyond the target after it gets back
    # to alt 0.
    # With a max speed of vy, the highest reached alt is vy + vy-1 + vy-2 + ... + 2 + 1 which is vy*(vy+1)/2
    print(abs(y_target[0]) * (abs(y_target[0]) - 1) // 2)


if __name__ == "__main__":
    run()
