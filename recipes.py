from fuzzywuzzy import process

from textual import on
from textual.app import ComposeResult
from textual.events import ScreenResume
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button, TextArea
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

class RecipeIngredientSearchScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    name_matches = []
    id_matches = []

    ingredient_name_input = None
    list_view = None
    ingredient_amount_input = None

    async def clear_ingredient_search(self) -> None:
        self.name_matches.clear()
        self.id_matches.clear()
        self.ingredient_name_input.value = ""
        await self.list_view.clear()
        self.ingredient_amount_input.value = "0"

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for name_match_idx, name_match in enumerate(self.name_matches):
            self.list_view.append(ListItem(Label(name_match), id=f'search_ingredient_{name_match_idx}'))

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Ingredient Search", id="title")
        self.ingredient_name_input = Input(placeholder="Ingredient Name", id="ingredient_name", type="text")
        yield self.ingredient_name_input
        yield Button("Search", id="search_ingredient")
        yield Label("Select Ingredient")
        self.list_view = ListView()
        yield self.list_view
        self.ingredient_amount_input = Input(placeholder="Ingredient Amount", id="ingredient_amount", type="number", value="0")
        yield self.ingredient_amount_input
        yield Button("Add Ingredient", id="add_ingredient")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search_ingredient":
            self.name_matches.clear()
            self.id_matches.clear()

            self.name_matches, self.id_matches = search_ingredient(self.query_one("#ingredient_name").value)

            await self.refresh_list_view()
        elif event.button.id == "add_ingredient":
            if self.list_view.index is None:
                self.dismiss(None)
            else:
                ingredient_id = self.id_matches[self.list_view.index]
                ingredient_amount = self.query_one("#ingredient_amount").value

                await self.clear_ingredient_search()

                self.dismiss((ingredient_id, ingredient_amount))

class AddRecipeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    recipe_ingredients = []
    recipe_amounts = []
    recipe_name_input = None
    list_view = None
    text_area = None

    async def clear_recipe(self) -> None:
        self.recipe_ingredients.clear()
        self.recipe_amounts.clear()
        self.recipe_name_input.value = ""
        await self.list_view.clear()
        self.text_area.text = ""

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for ingredient_idx, recipe_ingredient in enumerate(self.recipe_ingredients):
            ingredient_name = None
            ingredient_unit_of_measure = None

            for ingredient in ingredients.ingredients:
                if int(ingredient["id"]) == int(recipe_ingredient):
                    ingredient_name = ingredient["name"]
                    ingredient_unit_of_measure = ingredient["unit_of_measure"]

            ingredient_amount = self.recipe_amounts[ingredient_idx]

            self.list_view.append(ListItem(Label(f'{ingredient_name} ({ingredient_amount})'), id=f'ingredient_{ingredient_idx}'))

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Add Recipe", id="title")
        self.recipe_name_input = Input(placeholder="Recipe Name", id="recipe_name", type="text")
        yield self.recipe_name_input
        yield Label("Servings")
        self.recipe_servings_input = Input(placeholder="Servings", id="recipe_servings", type="number", value="1")
        yield self.recipe_servings_input
        yield Label("Time")
        self.recipe_time_input = Input(placeholder="Time", id="recipe_time", type="text")
        yield self.recipe_time_input
        yield Button("Add Ingredient", id="add_ingredient")
        self.list_view = ListView()
        yield self.list_view
        yield Label("Instructions")
        self.text_area = TextArea(id="recipe_instructions")
        yield self.text_area
        yield Button("Submit", id="add_recipe")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_ingredient":
            async def add_recipe_ingredient(ingredient_tuple) -> None:
                if ingredient_tuple is not None:
                    ingredient_id, ingredient_amount = ingredient_tuple

                    if ingredient_id is not None:
                        self.recipe_ingredients.append(ingredient_id)
                        self.recipe_amounts.append(ingredient_amount)

                    if len(self.recipe_ingredients) > 0:
                        await self.refresh_list_view()

            self.app.push_screen("recipe_ingredient_search", add_recipe_ingredient)
        elif event.button.id == "add_recipe":
            recipe_name = self.query_one("#recipe_name").value
            if recipe_name is None or recipe_name == "":
                self.app.pop_screen()
            else:
                max_id = find_max_recipe_id()
                recipes.append({"id": max_id + 1, "name": recipe_name, "servings": self.query_one("#recipe_servings").value, "time": self.query_one("#recipe_time").value, "ingredients": self.recipe_ingredients, "amounts": self.recipe_amounts, "deleted": False, "instructions": self.query_one("#recipe_instructions").text})
                await self.clear_recipe()
                self.app.pop_screen()

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        del self.recipe_ingredients[int(event.item.id[11:])]
        del self.recipe_amounts[int(event.item.id[11:])]

        await self.refresh_list_view()

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
        recipe_time = None
        recipe_servings = None
        for recipe in recipes:
            if int(recipe["id"]) == int(self.view_recipe_id):
                recipe_name = recipe["name"]
                recipe_instructions = recipe["instructions"]
                recipe_time = recipe["time"]
                recipe_servings = recipe["servings"]
                break

        yield Label(f"Recipe Name: {recipe_name}")
        yield Label(f"Time: {recipe_time}")
        yield Label(f"Servings: {recipe_servings}")

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

            self.view_recipe_id = None

            self.dismiss(None)

class ListRecipesScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    list_view = None

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for recipe_idx, recipe in enumerate(recipes):
            if not recipe["deleted"]:
                self.list_view.append(ListItem(Label(f'{recipe["name"]} ({recipe["servings"]} servings) ({recipe["time"]})'), id=f'recipe_{recipe_idx}'))

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("List Recipes", id="title")
        list_items = []
        for recipe_idx, recipe in enumerate(recipes):
            if not recipe["deleted"]:
                list_items.append(ListItem(Label(f'{recipe["name"]} ({recipe["servings"]} servings) ({recipe["time"]})'), id=f'recipe_{recipe_idx}'))
        self.list_view = ListView(*list_items, id="list_recipes")
        yield self.list_view
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        recipe_idx = int(event.item.id[7:])
        recipe_id = recipes[recipe_idx]["id"]

        self.app.push_screen(ViewRecipeScreen(recipe_id))

    @on(ScreenResume)
    async def handle_list_recipes_screen_resumed(self) -> None:
        await self.refresh_list_view()

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