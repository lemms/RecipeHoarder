from fuzzywuzzy import process

import ingredients_util

recipes = []

def find_max_recipe_id() -> int:
    max_id = 0

    for recipe in recipes:
        if int(recipe["id"]) > max_id:
            max_id = int(recipe["id"])

    return max_id

def search_ingredient(ingredient_name: str, match_limit: int = 50) -> list:
    ingredient_names = [ingredient["name"] for ingredient in ingredients_util.ingredients]
    string_matches = process.extract(ingredient_name, ingredient_names, limit=match_limit)

    ingredients_matched = [False] * len(ingredients_util.ingredients)

    name_matches = [string_match[0] for string_match in string_matches]
    id_matches = []
    for name_match in name_matches:
        for ingredient_idx, ingredient in enumerate(ingredients_util.ingredients):
            if not ingredients_matched[ingredient_idx]:
                if ingredient["name"] == name_match:
                    id_matches.append(ingredient["id"])
                    ingredients_matched[ingredient_idx] = True
                    break

    return name_matches, id_matches