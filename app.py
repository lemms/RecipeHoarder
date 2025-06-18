#! /bin/python3

import argparse
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListView, ListItem 

import add_ingredient
import add_recipe
import add_menu
import generate_grocery_list
import ingredients
import list_ingredients
import list_recipes
import list_menus
import menu_recipe_search
import menus
import recipe_ingredient_search
import recipes
import util
import view_ingredient
import view_menu
import view_recipe


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
        util.save_data()
        self.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=str, help="Data directory")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    args = parser.parse_args()

    util.data_path = args.data
    util.debug = args.debug

    util.load_data()

    app = RecipeHoarder()
    app.run()