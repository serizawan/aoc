import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    ingredients_and_allergens = []
    allergens_set = set()
    ingredients_set = set()
    for line in lines:
        splitted_lines = line.split(' (contains ')
        ingredients = splitted_lines[0].split(' ')
        allergens = splitted_lines[1][:-1].split(', ')
        for allergen in allergens:
            allergens_set.add(allergen)
        for ingredient in ingredients:
            ingredients_set.add(ingredient)
        ingredients_and_allergens.append([ingredients, allergens])

    all_suspect_ingredients = set()
    for allergen in allergens_set:
        suspect_ingredients = ingredients_set.copy()
        for item in ingredients_and_allergens:
            if allergen in item[1]:
                suspect_ingredients = suspect_ingredients.intersection(set(item[0]))
        all_suspect_ingredients = all_suspect_ingredients.union(suspect_ingredients)

    count_non_suspect_occurences = 0
    for item in ingredients_and_allergens:
        count_non_suspect_occurences += len((set(item[0]) - all_suspect_ingredients))
    print(count_non_suspect_occurences)
