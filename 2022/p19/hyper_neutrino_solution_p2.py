import re

"""
This script source is: https://github.com/hyper-neutrino/advent-of-code/blob/main/2022/day19p2.py

Note that even without cache, this algorithm completes in a reasonable time (a couple of minutes).
With in.txt:
When cache is enabled and amount optimization is enabled: DFS is invoked 11M.
When cache is enabled but amount optimization is disabled: DFS is invoked 41M.
When cache is disabled: DFS is invoked 350M.
"""

def dfs(bp, maxspend, cache, time, bots, amt):
    if time == 0:
        return amt[3]

    key = tuple([time, *bots, *amt])
    if key in cache:
        return cache[key]

    maxval = amt[3] + bots[3] * time

    for btype, recipe in enumerate(bp):
        if btype != 3 and bots[btype] >= maxspend[btype]:
            continue

        wait = 0
        for ramt, rtype in recipe:
            if bots[rtype] == 0:
                break
            wait = max(wait, -(-(ramt - amt[rtype]) // bots[rtype]))
        else:
            remtime = time - wait - 1
            if remtime <= 0:
                continue
            bots_ = bots[:]
            amt_ = [x + y * (wait + 1) for x, y in zip(amt, bots)]
            for ramt, rtype in recipe:
                amt_[rtype] -= ramt
            bots_[btype] += 1
            # We can "throw" extra stock of a given resource when we have "too much" ("too much" means more
            # than we would need if we had to spend the maximum resource cost on each time tick). This stock
            # adjustement doesn't affect production (as we spoil only unspendable stock) but improve cache hitting
            # and hence performance. We named this strategy "amount optimization".
            for i in range(3):
                amt_[i] = min(amt_[i], maxspend[i] * remtime)
            maxval = max(maxval, dfs(bp, maxspend, cache, remtime, bots_, amt_))

    cache[key] = maxval
    return maxval


total = 1

for line in list(open(0))[:3]:
    bp = []
    maxspend = [0, 0, 0]
    for section in line.split(": ")[1].split(". "):
        recipe = []
        for x, y in re.findall(r"(\d+) (\w+)", section):
            x = int(x)
            y = ["ore", "clay", "obsidian"].index(y)
            recipe.append((x, y))
            maxspend[y] = max(maxspend[y], x)
        bp.append(recipe)
    v = dfs(bp, maxspend, {}, 32, [1, 0, 0, 0], [0, 0, 0, 0])
    total *= v

print(total)