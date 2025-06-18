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

def search_ingredient(ingredient_name: str, match_limit: int = 50) -> list:
    ingredient_names = [ingredient["name"] for ingredient in ingredients.ingredients]
    string_matches = process.extract(ingredient_name, ingredient_names, limit=match_limit)

    ingredients_matched = [False] * len(ingredients.ingredients)

    name_matches = [string_match[0] for string_match in string_matches]
    id_matches = []
    for name_match in name_matches:
        for ingredient_idx, ingredient in enumerate(ingredients.ingredients):
            if not ingredients_matched[ingredient_idx]:
                if ingredient["name"] == name_match:
                    id_matches.append(ingredient["id"])
                    ingredients_matched[ingredient_idx] = True
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
        self.name_matches = []
        self.id_matches = []
        self.ingredient_name_input.value = ""
        await self.list_view.clear()
        self.ingredient_amount_input.value = "0"

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for name_match_idx, name_match in enumerate(self.name_matches):
            id_match = self.id_matches[name_match_idx]
            ingredient_unit_of_measure = None
            ingredient_category = None
            for ingredient in ingredients.ingredients:
                if int(ingredient["id"]) == int(id_match):
                    ingredient_unit_of_measure = ingredient["unit_of_measure"]
                    ingredient_category = ingredient["category"]

            self.list_view.append(ListItem(Label(f'{name_match} ({ingredient_unit_of_measure}) ({ingredient_category})'), id=f'search_ingredient_{name_match_idx}'))

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Ingredient Search", id="title")
        self.ingredient_name_input = Input(placeholder="Ingredient Name", id="ingredient_name", type="text")
        yield self.ingredient_name_input
        yield Button("Search", id="search_ingredient")
        yield Label("Select Ingredient")
        self.list_view = ListView()
        yield self.list_view
        yield Label("Amount")
        self.ingredient_amount_input = Input(placeholder="Ingredient Amount", id="ingredient_amount", type="number", value="0")
        yield self.ingredient_amount_input
        yield Button("Add Ingredient", id="add_ingredient")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search_ingredient":
            self.name_matches = []
            self.id_matches = []

            self.name_matches, self.id_matches = search_ingredient(self.query_one("#ingredient_name").value)

            await self.refresh_list_view()
        elif event.button.id == "add_ingredient":
            if self.list_view.index is None:
                self.dismiss(None)
            else:
                ingredient_id = self.id_matches[self.list_view.index]
                ingredient_amount = float(self.query_one("#ingredient_amount").value)

                await self.clear_ingredient_search()

                self.dismiss((ingredient_id, ingredient_amount))

class AddRecipeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    recipe_ingredients = []
    recipe_amounts = []
    recipe_name_input = None
    recipe_servings_input = None
    recipe_time_input = None
    recipe_stars_input = None
    recipe_instructions_text_area = None
    list_view = None
    recipe_tags_text_area = None
    recipe_source_input = None

    async def clear_recipe(self) -> None:
        self.recipe_ingredients = []
        self.recipe_amounts = []
        self.recipe_name_input.value = ""
        await self.list_view.clear()
        self.recipe_servings_input.value = "1"
        self.recipe_time_input.value = ""
        self.recipe_stars_input.value = "5"
        self.recipe_instructions_text_area.text = ""
        self.recipe_tags_text_area.text = ""
        self.recipe_source_input.value = ""

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for ingredient_idx, recipe_ingredient in enumerate(self.recipe_ingredients):
            ingredient_name = None
            ingredient_unit_of_measure = None

            for ingredient in ingredients.ingredients:
                if int(ingredient["id"]) == int(recipe_ingredient):
                    ingredient_name = ingredient["name"]
                    ingredient_unit_of_measure = ingredient["unit_of_measure"]

            ingredient_amount = float(self.recipe_amounts[ingredient_idx])

            self.list_view.append(ListItem(Label(f'{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure})'), id=f'ingredient_{ingredient_idx}'))

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
        self.recipe_instructions_text_area = TextArea(id="recipe_instructions")
        yield self.recipe_instructions_text_area
        yield Label("Star Rating")
        self.recipe_stars_input = Input(placeholder="Star Rating", id="recipe_stars", type="number", value="5")
        yield self.recipe_stars_input
        yield Label("Tags")
        self.recipe_tags_text_area = TextArea(id="recipe_tags")
        yield self.recipe_tags_text_area
        yield Label("Source (Book/Website)")
        self.recipe_source_input = Input(placeholder="Source (Book/Website)", id="recipe_source", type="text")
        yield self.recipe_source_input
        yield Button("Submit", id="add_recipe")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_ingredient":
            async def add_recipe_ingredient(ingredient_tuple) -> None:
                if ingredient_tuple is not None:
                    ingredient_id, ingredient_amount = ingredient_tuple

                    if ingredient_id is not None:
                        self.recipe_ingredients.append(ingredient_id)
                        self.recipe_amounts.append(float(ingredient_amount))

                    if len(self.recipe_ingredients) > 0:
                        await self.refresh_list_view()

            self.app.push_screen("recipe_ingredient_search", add_recipe_ingredient)
        elif event.button.id == "add_recipe":
            recipe_name = self.query_one("#recipe_name").value
            if recipe_name is None or recipe_name == "":
                self.app.pop_screen()
            else:
                max_id = find_max_recipe_id()
                if self.recipe_tags_text_area.text is not None and self.recipe_tags_text_area.text != "":
                    recipe_tags = self.recipe_tags_text_area.text.split("\n")
                else:
                    recipe_tags = []

                recipe = {"id": max_id + 1,
                          "name": recipe_name,
                          "servings": self.recipe_servings_input.value,
                          "time": self.recipe_time_input.value,
                          "ingredients": self.recipe_ingredients,
                          "amounts": self.recipe_amounts,
                          "deleted": False,
                          "instructions": self.recipe_instructions_text_area.text,
                          "stars": self.recipe_stars_input.value,
                          "tags": recipe_tags,
                          "source": self.recipe_source_input.value}

                recipes.append(recipe)

                await self.clear_recipe()
                self.app.pop_screen()

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        del self.recipe_ingredients[int(event.item.id[11:])]
        del self.recipe_amounts[int(event.item.id[11:])]

        await self.refresh_list_view()

class EditRecipeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    edit_recipe_id = None

    recipe_ingredients = []
    recipe_amounts = []
    recipe_name_input = None
    recipe_servings_input = None
    recipe_time_input = None
    recipe_stars_input = None
    recipe_instructions_text_area = None
    list_view = None
    recipe_tags_text_area = None
    recipe_source_input = None

    def __init__(self, edit_recipe_id: int) -> None:
        self.edit_recipe_id = edit_recipe_id
        super().__init__()

    async def clear_recipe(self) -> None:
        self.edit_recipe_id = None
        self.recipe_ingredients = []
        self.recipe_amounts = []
        self.recipe_name_input.value = ""
        await self.list_view.clear()
        self.recipe_servings_input.value = "1"
        self.recipe_time_input.value = ""
        self.recipe_stars_input.value = "5"
        self.recipe_instructions_text_area.text = ""
        self.recipe_tags_text_area.text = ""
        self.recipe_source_input.value = ""

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for ingredient_idx, recipe_ingredient in enumerate(self.recipe_ingredients):
            ingredient_name = None
            ingredient_unit_of_measure = None

            for ingredient in ingredients.ingredients:
                if int(ingredient["id"]) == int(recipe_ingredient):
                    ingredient_name = ingredient["name"]
                    ingredient_unit_of_measure = ingredient["unit_of_measure"]

            ingredient_amount = float(self.recipe_amounts[ingredient_idx])

            self.list_view.append(ListItem(Label(f'{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure})'), id=f'ingredient_{ingredient_idx}'))

    def compose(self) -> ComposeResult:
        recipe_name = None
        recipe_servings = None
        recipe_time = None
        recipe_ingredients = None
        recipe_amounts = None
        recipe_instructions = None
        recipe_stars = None
        recipe_tags = None
        recipe_source = None

        for recipe in recipes:
            if int(recipe["id"]) == int(self.edit_recipe_id):
                recipe_name = recipe["name"]
                recipe_servings = recipe["servings"]
                recipe_time = recipe["time"]
                recipe_ingredients = recipe["ingredients"]
                recipe_amounts = recipe["amounts"]
                recipe_instructions = recipe["instructions"]
                recipe_stars = recipe["stars"]
                recipe_tags = recipe["tags"]
                recipe_source = recipe["source"]
                break

        self.recipe_ingredients = recipe_ingredients
        self.recipe_amounts = recipe_amounts

        ingredient_list_items = []
        for ingredient_idx, recipe_ingredient in enumerate(self.recipe_ingredients):
            ingredient_name = None
            ingredient_unit_of_measure = None

            for ingredient in ingredients.ingredients:
                if int(ingredient["id"]) == int(recipe_ingredient):
                    ingredient_name = ingredient["name"]
                    ingredient_unit_of_measure = ingredient["unit_of_measure"]

            ingredient_amount = float(self.recipe_amounts[ingredient_idx])

            ingredient_list_items.append(ListItem(Label(f'{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure})'), id=f'ingredient_{ingredient_idx}'))

        yield Header()
        yield Static("Edit Recipe", id="title")
        self.recipe_name_input = Input(placeholder="Recipe Name", id="recipe_name", type="text", value=recipe_name)
        yield self.recipe_name_input
        yield Label("Servings")
        self.recipe_servings_input = Input(placeholder="Servings", id="recipe_servings", type="number", value=recipe_servings)
        yield self.recipe_servings_input
        yield Label("Time")
        self.recipe_time_input = Input(placeholder="Time", id="recipe_time", type="text", value=recipe_time)
        yield self.recipe_time_input
        yield Button("Add Ingredient", id="add_ingredient")
        self.list_view = ListView(*ingredient_list_items)
        yield self.list_view
        yield Label("Instructions")
        self.recipe_instructions_text_area = TextArea(id="recipe_instructions", text=recipe_instructions)
        yield self.recipe_instructions_text_area
        yield Label("Star Rating")
        self.recipe_stars_input = Input(placeholder="Star Rating", id="recipe_stars", type="number", value=recipe_stars)
        yield self.recipe_stars_input
        yield Label("Tags")
        self.recipe_tags_text_area = TextArea(id="recipe_tags", text="\n".join(recipe_tags))
        yield self.recipe_tags_text_area
        yield Label("Source (Book/Website)")
        self.recipe_source_input = Input(placeholder="Source (Book/Website)", id="recipe_source", type="text", value=recipe_source)
        yield self.recipe_source_input
        yield Button("Submit", id="add_recipe")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_ingredient":
            async def add_recipe_ingredient(ingredient_tuple) -> None:
                if ingredient_tuple is not None:
                    ingredient_id, ingredient_amount = ingredient_tuple

                    if ingredient_id is not None:
                        self.recipe_ingredients.append(ingredient_id)
                        self.recipe_amounts.append(float(ingredient_amount))

                    if len(self.recipe_ingredients) > 0:
                        await self.refresh_list_view()

            self.app.push_screen("recipe_ingredient_search", add_recipe_ingredient)
        elif event.button.id == "add_recipe":
            recipe_name = self.query_one("#recipe_name").value
            if recipe_name is None or recipe_name == "":
                self.app.pop_screen()
            else:
                if self.recipe_tags_text_area.text is not None and self.recipe_tags_text_area.text != "":
                    recipe_tags = self.recipe_tags_text_area.text.split("\n")
                else:
                    recipe_tags = []

                for recipe_idx, recipe in enumerate(recipes):
                    if int(recipe["id"]) == int(self.edit_recipe_id):
                        recipe["name"] = recipe_name
                        recipe["servings"] = self.recipe_servings_input.value
                        recipe["time"] = self.recipe_time_input.value
                        recipe["ingredients"] = self.recipe_ingredients
                        recipe["amounts"] = self.recipe_amounts
                        recipe["deleted"] = False
                        recipe["instructions"] = self.recipe_instructions_text_area.text
                        recipe["stars"] = self.recipe_stars_input.value
                        recipe["tags"] = recipe_tags
                        recipe["source"] = self.recipe_source_input.value

                await self.clear_recipe()

                self.dismiss(self.edit_recipe_id)

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        del self.recipe_ingredients[int(event.item.id[11:])]
        del self.recipe_amounts[int(event.item.id[11:])]

        await self.refresh_list_view()

class ViewRecipeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    view_recipe_id = None
    recipe_name_label = None
    recipe_time_label = None
    recipe_servings_label = None
    recipe_ingredients_list_view = None
    recipe_instructions_label = None
    recipe_tags_label = None
    recipe_stars_label = None
    recipe_source_label = None

    def __init__(self, view_recipe_id: int) -> None:
        self.view_recipe_id = view_recipe_id
        super().__init__()

    async def refresh_recipe_form(self) -> None:
        recipe_name = None
        recipe_instructions = None
        recipe_time = None
        recipe_servings = None
        recipe_ingredients = None
        recipe_amounts = None
        recipe_tags = None
        recipe_stars = None
        recipe_source = None
        for recipe in recipes:
            if int(recipe["id"]) == int(self.view_recipe_id):
                recipe_name = recipe["name"]
                recipe_instructions = recipe["instructions"]
                recipe_time = recipe["time"]
                recipe_servings = recipe["servings"]
                recipe_ingredients = recipe["ingredients"]
                recipe_amounts = recipe["amounts"]
                recipe_tags = recipe["tags"]
                recipe_stars = recipe["stars"]
                recipe_source = recipe["source"]
                break

        self.recipe_name_label.update(f"Recipe Name: {recipe_name}")
        self.recipe_time_label.update(f"Time: {recipe_time}")
        self.recipe_servings_label.update(f"Servings: {recipe_servings}")

        await self.recipe_ingredients_list_view.clear()
        recipe_ingredients_list_items = []
        for recipe_ingredient_idx, recipe_ingredient in enumerate(recipe_ingredients):
            ingredient_name = None
            ingredient_unit_of_measure = None
            ingredient_amount = float(recipe_amounts[recipe_ingredient_idx])

            for ingredient in ingredients.ingredients:
                if int(ingredient["id"]) == int(recipe_ingredient):
                    ingredient_name = ingredient["name"]
                    ingredient_unit_of_measure = ingredient["unit_of_measure"]
                    break

            self.recipe_ingredients_list_view.append(ListItem(Label(f"{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure})"), id=f'ingredient_{recipe_ingredient_idx}'))

        self.recipe_instructions_label.update(recipe_instructions)
        self.recipe_tags_label.update(", ".join(recipe_tags))
        self.recipe_stars_label.update(f'Star Rating: {recipe_stars}')
        self.recipe_source_label.update(f'Source: {recipe_source}')

    def compose(self) -> ComposeResult:
        recipe_name = None
        recipe_instructions = None
        recipe_time = None
        recipe_servings = None
        recipe_ingredients = None
        recipe_amounts = None
        recipe_tags = None
        recipe_stars = None
        recipe_source = None
        for recipe in recipes:
            if int(recipe["id"]) == int(self.view_recipe_id):
                recipe_name = recipe["name"]
                recipe_instructions = recipe["instructions"]
                recipe_time = recipe["time"]
                recipe_servings = recipe["servings"]
                recipe_ingredients = recipe["ingredients"]
                recipe_amounts = recipe["amounts"]
                recipe_tags = recipe["tags"]
                recipe_stars = recipe["stars"]
                recipe_source = recipe["source"]
                break

        recipe_ingredients_list_items = []

        for recipe_ingredient_idx, recipe_ingredient in enumerate(recipe_ingredients):
            ingredient_name = None
            ingredient_unit_of_measure = None
            ingredient_amount = float(recipe_amounts[recipe_ingredient_idx])

            for ingredient in ingredients.ingredients:
                if int(ingredient["id"]) == int(recipe_ingredient):
                    ingredient_name = ingredient["name"]
                    ingredient_unit_of_measure = ingredient["unit_of_measure"]
                    break

            recipe_ingredients_list_items.append(ListItem(Label(f"{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure})"), id=f'ingredient_{recipe_ingredient_idx}'))

        yield Header()
        yield Static("View Recipe", id="title")
        self.recipe_name_label = Label(f"Recipe Name: {recipe_name}")
        yield self.recipe_name_label
        self.recipe_time_label = Label(f"Time: {recipe_time}")
        yield self.recipe_time_label
        self.recipe_servings_label = Label(f"Servings: {recipe_servings}")
        yield self.recipe_servings_label
        yield Label("Ingredients")
        self.recipe_ingredients_list_view = ListView(*recipe_ingredients_list_items)
        yield self.recipe_ingredients_list_view
        yield Label("Instructions")
        self.recipe_instructions_label = Label(recipe_instructions)
        yield self.recipe_instructions_label
        yield Label("Tags")
        self.recipe_tags_label = Label(", ".join(recipe_tags))
        yield self.recipe_tags_label
        self.recipe_stars_label = Label(f'Star Rating: {recipe_stars}')
        yield self.recipe_stars_label
        self.recipe_source_label = Label(f'Source: {recipe_source}')
        yield self.recipe_source_label
        yield Button("Edit Recipe", id="edit_recipe")
        yield Button("Delete Recipe", id="delete_recipe")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete_recipe":
            for recipe_idx, recipe in enumerate(recipes):
                if int(recipe["id"]) == int(self.view_recipe_id):
                    recipe["deleted"] = True

            self.view_recipe_id = None

            self.dismiss(None)
        elif event.button.id == "edit_recipe":
            recipe_screen = self

            async def edit_recipe(recipe_id) -> None:
                await recipe_screen.refresh_recipe_form()

            self.app.push_screen(EditRecipeScreen(self.view_recipe_id), edit_recipe)

class ListRecipesScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    list_view = None

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for recipe_idx, recipe in enumerate(recipes):
            if not recipe["deleted"]:
                self.list_view.append(ListItem(Label(f'{recipe["name"]} ({recipe["servings"]} servings) ({recipe["time"]}) {recipe["stars"]} stars'), id=f'recipe_{recipe_idx}'))

    def compose(self) -> ComposeResult:
        list_items = []
        for recipe_idx, recipe in enumerate(recipes):
            if not recipe["deleted"]:
                list_items.append(ListItem(Label(f'{recipe["name"]} ({recipe["servings"]} servings) ({recipe["time"]}) {recipe["stars"]} stars'), id=f'recipe_{recipe_idx}'))

        yield Header()
        yield Static("List Recipes", id="title")
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