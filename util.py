import json
import os

import ingredients_util
import recipes_util
import menus_util

data_path = ""
debug = False

def load_data():
    if os.path.exists(data_path + "/ingredients.json") and os.path.isfile(data_path + "/ingredients.json"):
        with open(data_path + "/ingredients.json", "r") as f:
            ingredients_util.ingredients = json.load(f)
    if os.path.exists(data_path + "/recipes.json") and os.path.isfile(data_path + "/recipes.json"):
        with open(data_path + "/recipes.json", "r") as f:
            recipes_util.recipes = json.load(f)
    if os.path.exists(data_path + "/menus.json") and os.path.isfile(data_path + "/menus.json"):
        with open(data_path + "/menus.json", "r") as f:
            menus_util.menus = json.load(f)

    if debug:
        print(ingredients_util.ingredients)
        print(recipes_util.recipes)
        print(menus_util.menus)

        with open(data_path + "/ingredients_backup.json", "w") as f:
            f.write(json.dumps(ingredients_util.ingredients, indent=4))
        with open(data_path + "/recipes_backup.json", "w") as f:
            f.write(json.dumps(recipes_util.recipes, indent=4))
        with open(data_path + "/menus_backup.json", "w") as f:
            f.write(json.dumps(menus_util.menus, indent=4))
    else:
        with open(data_path + "/ingredients_backup.json", "w") as f:
            json.dump(ingredients_util.ingredients, f)
        with open(data_path + "/recipes_backup.json", "w") as f:
            json.dump(recipes_util.recipes, f)
        with open(data_path + "/menus_backup.json", "w") as f:
            json.dump(menus_util.menus, f)

def save_data():
    with open(data_path + "/ingredients.json", "w") as f:
        json.dump(ingredients_util.ingredients, f)
    with open(data_path + "/recipes.json", "w") as f:
        json.dump(recipes_util.recipes, f)
    with open(data_path + "/menus.json", "w") as f:
        json.dump(menus_util.menus, f)