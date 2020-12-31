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
        # print(allergen, ':', suspect_ingredients)

    # The above loop would print if corresponding statement is un-commented:
    # wheat : {'ltbj', 'jqnhd'}
    # soy : {'zzkq', 'nrfmm', 'jqnhd'}
    # dairy : {'chpdjkf', 'ltbj'}
    # shellfish : {'pvhcsn', 'jtqt', 'jqnhd', 'jxbnb'}
    # nuts : {'pvhcsn', 'ltbj'}
    # peanuts : {'pvhcsn', 'jxbnb'}
    # sesame : {'chpdjkf'}
    # fish : {'nrfmm', 'jqnhd'}

    # Starting from sesame, we can infer the result by hand.
    # Note:
    # Can be done algorithmically by building a dict with the above printed elements (key: allergen, value: suspect ingredients) and
    # getting the single-item ingredient set, coupling it with its allergen and removing it from every other set (and removing also
    # the allergen from the dict) then iterate the described instructions over and over until there is no allergen left in the dict.
    ingredients_to_allergens = {
        'chpdjkf': 'sesame',
        'ltbj': 'dairy',
        'pvhcsn': 'nuts',
        'jxbnb': 'peanuts',
        'jqnhd': 'wheat',
        'nrfmm': 'fish',
        'zzkq': 'soy',
        'jtqt': 'shellfish',
    }
    print(','.join([item[0] for item in sorted(ingredients_to_allergens.items(), key=lambda item: item[1])]))
