import re

if __name__ == "__main__":
    L, C = 103, 101
    # L, C = 7, 11
    S = 100
    robots = open(0).read().splitlines()
    robots = [[int(i) for i in re.findall(r'[-]?\d+', robot)] for robot in robots]
    top_left_c, top_right_c, bottom_left_c, bottom_right_c = 0, 0, 0, 0
    for robot in robots:
        robot[0], robot[1] = (robot[0] + S * robot[2]) % C, (robot[1] + S * robot[3]) % L
        if 0 <= robot[1] < L // 2 and 0 <= robot[0] < C // 2:
            top_left_c += 1
        elif 0 <= robot[1] < L // 2 and C // 2 + 1 <= robot[0] < C:
            top_right_c += 1
        elif L // 2 + 1 <= robot[1] < L and 0 <= robot[0] < C // 2:
            bottom_left_c += 1
        elif L // 2 + 1 <= robot[1] < L and C // 2 + 1 <= robot[0] < C:
            bottom_right_c += 1

    print(top_left_c * top_right_c * bottom_left_c * bottom_right_c)




