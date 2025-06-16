#! /bin/python3

import argparse
import json
import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem 

import recipes
import ingredients
import menus
import grocery_lists

data_path = ""

class RecipeApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "quit", "Quit")]
    SCREENS = {"recipes": recipes.RecipesScreen,
               "ingredients": ingredients.IngredientsScreen,
               "menus": menus.MenusScreen,
               "grocery_lists": grocery_lists.GroceryListsScreen,
               "add_recipe": recipes.AddRecipeScreen,
               "edit_recipe": recipes.EditRecipeScreen,
               "list_recipes": recipes.ListRecipesScreen,
               "view_recipe": recipes.ViewRecipeScreen,
               "add_ingredient": ingredients.AddIngredientScreen,
               "edit_ingredient": ingredients.EditIngredientScreen,
               "list_ingredients": ingredients.ListIngredientsScreen,
               "view_ingredient": ingredients.ViewIngredientScreen,
               "add_menu": menus.AddMenuScreen,
               "edit_menu": menus.EditMenuScreen,
               "list_menus": menus.ListMenusScreen,
               "add_grocery_list": grocery_lists.AddGroceryListScreen,
               "edit_grocery_list": grocery_lists.EditGroceryListScreen,
               "list_grocery_lists": grocery_lists.ListGroceryListsScreen,
               "view_grocery_list": grocery_lists.ViewGroceryListScreen,
               "recipe_ingredient_search": recipes.RecipeIngredientSearchScreen,
               "recipe_add_ingredient": recipes.RecipeAddIngredientScreen}

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Recipes App", id="title")
        yield ListView(ListItem(Label("Recipes"), id="recipes"),
                       ListItem(Label("Ingredients"), id="ingredients"),
                       ListItem(Label("Menus"), id="menus"),
                       ListItem(Label("Grocery Lists"), id="grocery_lists"),
                       ListItem(Label("Quit"), id="quit"),
                       id="main_list")
        yield Footer()
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id == "recipes":
            self.app.push_screen("recipes")
        elif event.item.id == "ingredients":
            self.app.push_screen("ingredients")
        elif event.item.id == "menus":
            self.app.push_screen("menus")
        elif event.item.id == "grocery_lists":
            self.app.push_screen("grocery_lists")
        elif event.item.id == "quit":
            self.action_quit()
    
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_quit(self) -> None:
        """An action to quit the app."""
        with open(data_path + "/recipes.json", "w") as f:
            json.dump(recipes.recipes, f)
        with open(data_path + "/ingredients.json", "w") as f:
            json.dump(ingredients.ingredients, f)
        with open(data_path + "/menus.json", "w") as f:
            json.dump(menus.menus, f)
        with open(data_path + "/grocery_lists.json", "w") as f:
            json.dump(grocery_lists.grocery_lists, f)
        self.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=str, help="Data directory")
    args = parser.parse_args()

    data_path = args.data

    if os.path.exists(data_path + "/recipes.json") and os.path.isfile(data_path + "/recipes.json"):
        with open(data_path + "/recipes.json", "r") as f:
            recipes.recipes = json.load(f)
    if os.path.exists(data_path + "/ingredients.json") and os.path.isfile(data_path + "/ingredients.json"):
        with open(data_path + "/ingredients.json", "r") as f:
            ingredients.ingredients = json.load(f)
    if os.path.exists(data_path + "/menus.json") and os.path.isfile(data_path + "/menus.json"):
        with open(data_path + "/menus.json", "r") as f:
            menus.menus = json.load(f)
    if os.path.exists(data_path + "/grocery_lists.json") and os.path.isfile(data_path + "/grocery_lists.json"):
        with open(data_path + "/grocery_lists.json", "r") as f:
            grocery_lists.grocery_lists = json.load(f)

    with open(data_path + "/recipes_backup.json", "w") as f:
        json.dump(recipes.recipes, f)
    with open(data_path + "/ingredients_backup.json", "w") as f:
        json.dump(ingredients.ingredients, f)
    with open(data_path + "/menus_backup.json", "w") as f:
        json.dump(menus.menus, f)
    with open(data_path + "/grocery_lists_backup.json", "w") as f:
        json.dump(grocery_lists.grocery_lists, f)

    # TODO: Remove this
    print(recipes.recipes)
    print(ingredients.ingredients)
    print(menus.menus)
    print(grocery_lists.grocery_lists)

    app = RecipeApp()
    app.run()