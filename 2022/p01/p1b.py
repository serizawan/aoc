import sys


if __name__ == "__main__":
    elves_calories = []

    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    for elf_calories in " ".join(lines).split("  "):
        elf_calories_total = sum(map(int, elf_calories.split(" ")))
        elves_calories.append(elf_calories_total)

    print(sum(sorted(elves_calories)[-3:]))
