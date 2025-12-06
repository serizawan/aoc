if __name__ == "__main__":
    my_in = open(0).read().splitlines()
    sep = my_in.index("")
    ranges = [[int(i) for i in r.split("-")] for r in my_in[:sep]]
    ingredients = [int(i) for i in my_in[sep + 1:]]
    fresh_count = 0
    for ingredient in ingredients:
        is_fresh = False
        for r in ranges:
            if r[0] <= ingredient <= r[1]:
                is_fresh = True
        if is_fresh:
            fresh_count += 1
    print(fresh_count)