from fuzzywuzzy import process

from textual import on
from textual.app import ComposeResult
from textual.events import ScreenResume
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button, Digits, TextArea
from textual.containers import HorizontalGroup
from textual.css.query import NoMatches

import ingredients

recipes = []

def find_max_recipe_id() -> int:
    max_id = 0

    for recipe in recipes:
        if int(recipe["id"]) > max_id:
            max_id = int(recipe["id"])

    return max_id

def search_ingredient(ingredient_name: str, match_limit: int = 10) -> list:
    ingredient_names = [ingredient["name"] for ingredient in ingredients.ingredients]
    string_matches = process.extract(ingredient_name, ingredient_names, limit=match_limit)

    name_matches = [string_match[0] for string_match in string_matches]
    id_matches = []
    for name_match in name_matches:
        for ingredient in ingredients.ingredients:
            if ingredient["name"] == name_match:
                id_matches.append(ingredient["id"])
                break

    return name_matches, id_matches

class RecipeAddIngredientScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    ingredient_name = ""
    ingredient_id = None
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Add Ingredient", id="title")
        yield Label(f"Ingredient Name: {self.ingredient_name}")
        yield Input(placeholder="Ingredient Amount", id="ingredient_amount", type="number")
        yield Button("Submit", id="submit")

class RecipeIngredientSearchScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    name_matches = []
    id_matches = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Ingredient Search", id="title")
        yield Input(placeholder="Ingredient Name", id="ingredient_name", type="text")
        yield Button("Search", id="search_ingredient")
        yield Label("Select Ingredient")
        yield ListView()
        yield Input(placeholder="Ingredient Amount", id="ingredient_amount", type="number", value="0")
        yield Button("Add Ingredient", id="add_ingredient")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search_ingredient":
            self.name_matches, self.id_matches = search_ingredient(self.query_one("#ingredient_name").value)

            list_view = self.query_one("ListView")
            list_view.clear()
            for name_match_idx, name_match in enumerate(self.name_matches):
                list_view.append(ListItem(Label(name_match), id=f'search_ingredient_{self.id_matches[name_match_idx]}'))
            list_view.refresh()
        elif event.button.id == "add_ingredient":
            list_view = self.query_one("ListView")
            if list_view.index is None:
                self.dismiss(None)
            else:
                ingredient_id = self.id_matches[list_view.index]
                ingredient_amount = self.query_one("#ingredient_amount").value
                self.dismiss((ingredient_id, ingredient_amount))

class IngredientAmount(HorizontalGroup):
    ingredient_name = ""
    ingredient_amount = 0

    def __init__(self, ingredient_name: str, ingredient_amount: int, id: str) -> None:
        super().__init__(id=id)
        self.ingredient_name = ingredient_name
        self.ingredient_amount = ingredient_amount

    def compose(self) -> ComposeResult:
        yield Label(f'{self.ingredient_name}')
        yield Digits(f'{self.ingredient_amount}')

class AddRecipeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    recipe_ingredients = []
    recipe_amounts = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Add Recipe", id="title")
        yield Input(placeholder="Recipe Name", id="recipe_name", type="text")
        yield Button("Add Ingredient", id="add_ingredient")
        yield ListView()
        yield Label("Instructions")
        yield TextArea(id="recipe_instructions")
        yield Button("Submit", id="add_recipe")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_ingredient":
            async def add_recipe_ingredient(ingredient_tuple) -> None:
                if ingredient_tuple is not None:
                    ingredient_id, ingredient_amount = ingredient_tuple

                    if ingredient_id is not None:
                        self.recipe_ingredients.append(ingredient_id)
                        self.recipe_amounts.append(ingredient_amount)

                    if len(self.recipe_ingredients) > 0:
                        list_view = self.query_one("ListView")
                        await list_view.clear()

                        for ingredient_idx, recipe_ingredient in enumerate(self.recipe_ingredients):
                            ingredient_name = None
                            for ingredient in ingredients.ingredients:
                                if ingredient["id"] == recipe_ingredient:
                                    ingredient_name = ingredient["name"]
                            ingredient_id = recipe_ingredient
                            ingredient_amount = self.recipe_amounts[ingredient_idx]
                            list_view.append(ListItem(IngredientAmount(ingredient_name,
                                                                       ingredient_amount,
                                                                       id=f'ingredient_amount_{ingredient_idx}'),
                                                      id=f'ingredient_{ingredient_idx}'))
                        list_view.refresh()

            self.app.push_screen("recipe_ingredient_search", add_recipe_ingredient)
        elif event.button.id == "add_recipe":
            recipe_name = self.query_one("#recipe_name").value
            if recipe_name is None or recipe_name == "":
                self.app.pop_screen()
            else:
                max_id = find_max_recipe_id()
                recipes.append({"id": max_id + 1, "name": recipe_name, "ingredients": self.recipe_ingredients, "amounts": self.recipe_amounts, "deleted": False, "instructions": self.query_one("#recipe_instructions").text})
                self.app.pop_screen()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        for ingredient in self.recipe_ingredients:
            ingredient_id = ingredients[ingredient]["id"]
            if event.item.id == f'ingredient_{ingredient_id}':
                self.recipe_ingredients.remove(ingredient)
                break

class EditRecipeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Edit Recipe", id="title")
        yield Footer()


class ViewRecipeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    view_recipe_id = None

    def __init__(self, view_recipe_id: int) -> None:
        self.view_recipe_id = view_recipe_id
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("View Recipe", id="title")

        recipe_name = None
        recipe_instructions = None
        for recipe in recipes:
            if int(recipe["id"]) == int(self.view_recipe_id):
                recipe_name = recipe["name"]
                recipe_instructions = recipe["instructions"]
                break

        yield Label(f"Recipe Name: {recipe_name}")

        yield Label("Ingredients")
        for recipe_ingredient_idx, recipe_ingredient in enumerate(recipe["ingredients"]):
            ingredient_name = None
            ingredient_unit_of_measure = None
            ingredient_amount = recipe["amounts"][recipe_ingredient_idx]

            for ingredient in ingredients.ingredients:
                if int(ingredient["id"]) == int(recipe_ingredient):
                    ingredient_name = ingredient["name"]
                    ingredient_unit_of_measure = ingredient["unit_of_measure"]
                    break

            yield Label(f"{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure})")

        yield Label("Instructions")
        yield Label(recipe_instructions)

        yield Button("Delete Recipe", id="delete_recipe")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete_recipe":
            for recipe_idx, recipe in enumerate(recipes):
                if int(recipe["id"]) == int(self.view_recipe_id):
                    recipe["deleted"] = True

            self.dismiss(None)

class ListRecipesScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    list_view = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("List Recipes", id="title")
        list_items = []
        for recipe in recipes:
            if not recipe["deleted"]:
                list_items.append(ListItem(Label(recipe["name"]), id=f'recipe_{recipe["id"]}'))
        self.list_view = ListView(*list_items, id="list_recipes")
        yield self.list_view
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        recipe_id = event.item.id[7:]

        self.app.push_screen(ViewRecipeScreen(recipe_id))

    @on(ScreenResume)
    async def handle_list_recipes_screen_resumed(self) -> None:
        await self.list_view.clear()

        for recipe in recipes:
            if not recipe["deleted"]:
                self.list_view.append(ListItem(Label(recipe["name"]), id=f'recipe_{recipe["id"]}'))

class RecipesScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Recipes", id="title")
        yield ListView(ListItem(Label("Add Recipe"), id="add_recipe"),
                       ListItem(Label("List Recipes"), id="list_recipes"))
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id == "add_recipe":
            self.app.push_screen("add_recipe")
        elif event.item.id == "list_recipes":
            self.app.push_screen("list_recipes")