from fuzzywuzzy import process

import recipes_util

menus = []

def find_max_menu_id() -> int:
    max_id = 0

    for menu in menus:
        if int(menu["id"]) > max_id:
            max_id = int(menu["id"])

    return max_id

def search_recipe(recipe_name: str, match_limit: int = 50) -> list:
    recipe_names = [recipe["name"] for recipe in recipes_util.recipes]
    string_matches = process.extract(recipe_name, recipe_names, limit=match_limit)

    name_matches = [string_match[0] for string_match in string_matches]
    id_matches = []
    for name_match in name_matches:
        for recipe in recipes_util.recipes:
            if recipe["name"] == name_match:
                id_matches.append(recipe["id"])
                break

    return name_matches, id_matches