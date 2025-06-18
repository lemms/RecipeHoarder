#! /bin/python3

import argparse
import json
import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListView, ListItem 

import add_ingredient
import add_recipe
import add_menu
import generate_grocery_list
import ingredients
import ingredients_util
import list_ingredients
import list_recipes
import list_menus
import menu_recipe_search
import menus
import menus_util
import recipe_ingredient_search
import recipes
import recipes_util
import view_ingredient
import view_menu
import view_recipe

data_path = ""

class RecipeHoarder(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "quit", "Quit")]
    SCREENS = {"recipes": recipes.RecipesScreen,
               "ingredients": ingredients.IngredientsScreen,
               "menus": menus.MenusScreen,
               "add_recipe": add_recipe.AddRecipeScreen,
               "list_recipes": list_recipes.ListRecipesScreen,
               "view_recipe": view_recipe.ViewRecipeScreen,
               "add_ingredient": add_ingredient.AddIngredientScreen,
               "list_ingredients": list_ingredients.ListIngredientsScreen,
               "view_ingredient": view_ingredient.ViewIngredientScreen,
               "add_menu": add_menu.AddMenuScreen,
               "list_menus": list_menus.ListMenusScreen,
               "view_menu": view_menu.ViewMenuScreen,
               "recipe_ingredient_search": recipe_ingredient_search.RecipeIngredientSearchScreen,
               "menu_recipe_search": menu_recipe_search.MenuRecipeSearchScreen,
               "generate_grocery_list": generate_grocery_list.GenerateGroceryListScreen}

    def compose(self) -> ComposeResult:
        yield Header()
        yield ListView(ListItem(Label("Ingredients"), id="ingredients"),
                       ListItem(Label("Recipes"), id="recipes"),
                       ListItem(Label("Menus"), id="menus"),
                       ListItem(Label("Quit"), id="quit"),
                       id="main_list")
        yield Footer()
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id == "ingredients":
            self.app.push_screen("ingredients")
        elif event.item.id == "recipes":
            self.app.push_screen("recipes")
        elif event.item.id == "menus":
            self.app.push_screen("menus")
        elif event.item.id == "quit":
            self.action_quit()
    
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_quit(self) -> None:
        """An action to quit the app."""
        with open(data_path + "/ingredients.json", "w") as f:
            json.dump(ingredients_util.ingredients, f)
        with open(data_path + "/recipes.json", "w") as f:
            json.dump(recipes_util.recipes, f)
        with open(data_path + "/menus.json", "w") as f:
            json.dump(menus_util.menus, f)
        self.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=str, help="Data directory")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    args = parser.parse_args()

    data_path = args.data

    if os.path.exists(data_path + "/ingredients.json") and os.path.isfile(data_path + "/ingredients.json"):
        with open(data_path + "/ingredients.json", "r") as f:
            ingredients_util.ingredients = json.load(f)
    if os.path.exists(data_path + "/recipes.json") and os.path.isfile(data_path + "/recipes.json"):
        with open(data_path + "/recipes.json", "r") as f:
            recipes_util.recipes = json.load(f)
    if os.path.exists(data_path + "/menus.json") and os.path.isfile(data_path + "/menus.json"):
        with open(data_path + "/menus.json", "r") as f:
            menus_util.menus = json.load(f)

    if args.debug:
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

    app = RecipeHoarder()
    app.run()