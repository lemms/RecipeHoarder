from fuzzywuzzy import process

import ingredients_util
import recipes_util

menus = []

def find_max_menu_id() -> int:
    max_id = 0

    for menu in menus:
        if int(menu["id"]) > max_id:
            max_id = int(menu["id"])

    return max_id

def search_recipe(recipe_search_string: str, match_limit: int = 50) -> list:
    recipe_metadata_strings = []

    for recipe in recipes_util.recipes:
        recipe_ingredient_strings = []

        for recipe_ingredient in recipe["ingredients"]:
            for ingredient in ingredients_util.ingredients:
                if int(recipe_ingredient) == int(ingredient["id"]):
                    recipe_ingredient_strings.append(ingredient["name"])
                    break

        recipe_metadata_strings.append(f'{recipe["name"]} {recipe["source"]} {recipe["tags"]} {recipe_ingredient_strings}')

    string_matches = process.extract(recipe_search_string, recipe_metadata_strings, limit=match_limit)

    search_matches = [string_match[0] for string_match in string_matches]
    name_matches = []
    id_matches = []

    for search_match in search_matches:
        for recipe in recipes_util.recipes:
            if recipe["name"] == search_match[:len(recipe["name"])]:
                name_matches.append(recipe["name"])
                id_matches.append(recipe["id"])
                break

    return name_matches, id_matches