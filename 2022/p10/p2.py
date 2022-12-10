import sys

H = 6
L = 40


def draw(cycle, x_register, screen):
    l_crt, c_crt = cycle // L, cycle % L
    if c_crt in (x_register - 1, x_register, x_register + 1):
        screen[l_crt][c_crt] = "#"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input Error: Wrong number of input parameters.", file=sys.stderr)
        print(f"Run with: python {sys.argv[0]} [INPUT_DATA_FILENAME].", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    cycle = 0
    x_register = 1
    screen = [["." for l in range(L)] for h in range(H)]
    screen[0][0] = "#"
    for line in lines:
        cycle += 1
        draw(cycle, x_register, screen)
        if line.startswith("addx"):
            cycle += 1
            v = int(line.split(" ")[1])
            x_register += v
            draw(cycle, x_register, screen)

    for screen_line in screen:
        print("".join(screen_line))
