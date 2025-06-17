from fuzzywuzzy import process

from textual import on
from textual.app import ComposeResult
from textual.events import ScreenResume
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button
from textual.containers import HorizontalGroup

import ingredients
import recipes

menus = []

def find_max_menu_id() -> int:
    max_id = 0

    for menu in menus:
        if int(menu["id"]) > max_id:
            max_id = int(menu["id"])

    return max_id

def search_recipe(recipe_name: str, match_limit: int = 50) -> list:
    recipe_names = [recipe["name"] for recipe in recipes.recipes]
    string_matches = process.extract(recipe_name, recipe_names, limit=match_limit)

    name_matches = [string_match[0] for string_match in string_matches]
    id_matches = []
    for name_match in name_matches:
        for recipe in recipes.recipes:
            if recipe["name"] == name_match:
                id_matches.append(recipe["id"])
                break

    return name_matches, id_matches

class MenuRecipeSearchScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    name_matches = []
    id_matches = []

    recipe_name_input = None
    list_view = None

    async def clear_menu_recipe_search(self) -> None:
        self.name_matches = []
        self.id_matches = []
        self.recipe_name_input.value = ""
        await self.list_view.clear()

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for name_match_idx, name_match in enumerate(self.name_matches):
            recipe_time = None
            recipe_servings = None
            recipe_stars = None

            for recipe in recipes.recipes:
                if int(recipe["id"]) == int(self.id_matches[name_match_idx]):
                    recipe_time = recipe["time"]
                    recipe_servings = recipe["servings"]
                    recipe_stars = recipe["stars"]
                    break

            self.list_view.append(ListItem(Label(f'{name_match} ({recipe_servings} servings) ({recipe_time}) {recipe_stars} stars'), id=f'search_recipe_{name_match_idx}'))

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Recipe Search", id="title")
        self.recipe_name_input = Input(placeholder="Recipe Name", id="recipe_name", type="text")
        yield self.recipe_name_input
        yield Button("Search", id="search_recipe")
        yield Label("Select Recipe")
        self.list_view = ListView()
        yield self.list_view
        yield Button("Add Recipe", id="add_recipe")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search_recipe":
            self.name_matches = []
            self.id_matches = []

            self.name_matches, self.id_matches = search_recipe(self.query_one("#recipe_name").value)

            await self.refresh_list_view()
        elif event.button.id == "add_recipe":
            if self.list_view.index is None:
                await self.clear_menu_recipe_search()

                self.dismiss(None)
            else:
                recipe_id = self.id_matches[self.list_view.index]

                await self.clear_menu_recipe_search()

                self.dismiss(recipe_id)

class AddMenuScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    menu_recipes = []
    menu_name_input = None
    menu_total_servings_label = None
    menu_recipe_list = None
    menu_servings = 0

    async def clear_menu_form(self) -> None:
        self.menu_recipes = []
        self.menu_name_input.value = ""
        self.menu_servings = 0
        await self.menu_recipe_list.clear()

    async def refresh_list_view(self) -> None:
        await self.menu_recipe_list.clear()

        self.menu_servings = 0

        for menu_recipe_idx, menu_recipe in enumerate(self.menu_recipes):
            menu_recipe_name = None
            menu_recipe_time = None
            menu_recipe_servings = None
            menu_recipe_stars = None
            for recipe in recipes.recipes:
                if int(recipe["id"]) == int(menu_recipe):
                    menu_recipe_name = recipe["name"]
                    menu_recipe_time = recipe["time"]
                    menu_recipe_servings = int(recipe["servings"])
                    menu_recipe_stars = recipe["stars"]

                    self.menu_servings += menu_recipe_servings

            self.menu_recipe_list.append(ListItem(Label(f'{menu_recipe_name} ({menu_recipe_servings} servings) ({menu_recipe_time}) {menu_recipe_stars} stars'), id=f'menu_recipe_{menu_recipe_idx}'))

        self.menu_total_servings_label.update(f"Total Servings: {self.menu_servings}")
        self.menu_total_servings_label.refresh()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Add Menu", id="title")
        self.menu_name_input = Input(placeholder="Menu Name", id="menu_name", type="text")
        yield self.menu_name_input
        yield Button("Add Recipe", id="add_menu_recipe")
        yield Label("Recipes")
        self.menu_recipe_list = ListView()
        yield self.menu_recipe_list
        self.menu_total_servings_label = Label(f"Total Servings: {self.menu_servings}")
        yield self.menu_total_servings_label
        yield Button("Submit", id="add_menu")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_menu_recipe":
            async def add_menu_recipe(recipe_id) -> None:
                if recipe_id is not None:
                    self.menu_recipes.append(recipe_id)

                    if len(self.menu_recipes) > 0:
                        await self.refresh_list_view()

            self.app.push_screen("menu_recipe_search", add_menu_recipe)
        elif event.button.id == "add_menu":
            menu_name = self.query_one("#menu_name").value

            if menu_name is None or menu_name == "":
                await self.clear_menu_form()
                self.app.pop_screen()
            else:
                max_id = find_max_menu_id()

                menus.append({"id": max_id + 1, "name": menu_name, "deleted": False, "recipes": self.menu_recipes})

                await self.clear_menu_form()
                self.app.pop_screen()

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        del self.menu_recipes[int(event.item.id[12:])]

        await self.refresh_list_view()

class GenerateGroceryListScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    grocery_list_menu_id = None

    def __init__(self, grocery_list_menu_id: int) -> None:
        self.grocery_list_menu_id = grocery_list_menu_id
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Grocery List", id="title")

        grocery_list_ingredients = []
        grocery_list_amounts = []

        menu_recipes = []
        for menu in menus:
            if int(menu["id"]) == int(self.grocery_list_menu_id):
                menu_recipes = menu["recipes"]
                break

        for menu_recipe in menu_recipes:
            for recipe in recipes.recipes:
                if int(recipe["id"]) == int(menu_recipe):
                    for recipe_ingredient_idx, recipe_ingredient in enumerate(recipe["ingredients"]):
                        try:
                            ingredient_idx = grocery_list_ingredients.index(recipe_ingredient)
                            grocery_list_amounts[ingredient_idx] += float(recipe["amounts"][recipe_ingredient_idx])
                        except ValueError:
                            grocery_list_ingredients.append(recipe_ingredient)
                            grocery_list_amounts.append(float(recipe["amounts"][recipe_ingredient_idx]))

        grocery_list_ingredient_names = []
        grocery_list_ingredient_units_of_measure = []
        grocery_list_ingredient_categories = []
        for grocery_list_ingredient_idx, grocery_list_ingredient_id in enumerate(grocery_list_ingredients):
            for ingredient in ingredients.ingredients:
                if int(ingredient["id"]) == int(grocery_list_ingredient_id):
                    grocery_list_ingredient_names.append(ingredient["name"])
                    grocery_list_ingredient_units_of_measure.append(ingredient["unit_of_measure"])
                    grocery_list_ingredient_categories.append(ingredient["category"])
                    break

        produce_ingredients = []
        dairy_ingredients = []
        meat_ingredients = []
        seafood_ingredients = []
        bakery_ingredients = []
        frozen_ingredients = []
        pantry_ingredients = []
        other_ingredients = []

        for grocery_list_ingredient_idx, grocery_list_ingredient_id in enumerate(grocery_list_ingredients):
            ingredient_category = None

            for ingredient in ingredients.ingredients:
                if int(ingredient["id"]) == int(grocery_list_ingredient_id):
                    ingredient_category = ingredient["category"]
                    break

            if ingredient_category == "produce":
                produce_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "dairy":
                dairy_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "meat":
                meat_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "seafood":
                seafood_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "bakery":
                bakery_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "frozen":
                frozen_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "pantry":
                pantry_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "other":
                other_ingredients.append(grocery_list_ingredient_idx)
            else:
                raise Exception(f'Invalid ingredient category: {ingredient_category}')

        if len(produce_ingredients) > 0:
            yield Label("Produce")
            for produce_ingredient_idx, produce_ingredient in enumerate(produce_ingredients):
                produce_ingredient_name = grocery_list_ingredient_names[produce_ingredient]
                produce_ingredient_amount = grocery_list_amounts[produce_ingredient]
                produce_ingredient_unit_of_measure = grocery_list_ingredient_units_of_measure[produce_ingredient]
                yield Label(f"{produce_ingredient_name} ({produce_ingredient_amount} {produce_ingredient_unit_of_measure})")

        if len(dairy_ingredients) > 0:
            yield Label("Dairy")
            for dairy_ingredient_idx, dairy_ingredient in enumerate(dairy_ingredients):
                dairy_ingredient_name = grocery_list_ingredient_names[dairy_ingredient]
                dairy_ingredient_amount = grocery_list_amounts[dairy_ingredient]
                dairy_ingredient_unit_of_measure = grocery_list_ingredient_units_of_measure[dairy_ingredient]
                yield Label(f"{dairy_ingredient_name} ({dairy_ingredient_amount} {dairy_ingredient_unit_of_measure})")

        if len(meat_ingredients) > 0:
            yield Label("Meat")
            for meat_ingredient_idx, meat_ingredient in enumerate(meat_ingredients):
                meat_ingredient_name = grocery_list_ingredient_names[meat_ingredient]
                meat_ingredient_amount = grocery_list_amounts[meat_ingredient]
                meat_ingredient_unit_of_measure = grocery_list_ingredient_units_of_measure[meat_ingredient]
                yield Label(f"{meat_ingredient_name} ({meat_ingredient_amount} {meat_ingredient_unit_of_measure})")

        if len(seafood_ingredients) > 0:
            yield Label("Seafood")
            for seafood_ingredient_idx, seafood_ingredient in enumerate(seafood_ingredients):
                seafood_ingredient_name = grocery_list_ingredient_names[seafood_ingredient]
                seafood_ingredient_amount = grocery_list_amounts[seafood_ingredient]
                seafood_ingredient_unit_of_measure = grocery_list_ingredient_units_of_measure[seafood_ingredient]
                yield Label(f"{seafood_ingredient_name} ({seafood_ingredient_amount} {seafood_ingredient_unit_of_measure})")

        if len(bakery_ingredients) > 0:
            yield Label("Bakery")
            for bakery_ingredient_idx, bakery_ingredient in enumerate(bakery_ingredients):
                bakery_ingredient_name = grocery_list_ingredient_names[bakery_ingredient]
                bakery_ingredient_amount = grocery_list_amounts[bakery_ingredient]
                bakery_ingredient_unit_of_measure = grocery_list_ingredient_units_of_measure[bakery_ingredient]
                yield Label(f"{bakery_ingredient_name} ({bakery_ingredient_amount} {bakery_ingredient_unit_of_measure})")

        if len(frozen_ingredients) > 0:
            yield Label("Frozen")
            for frozen_ingredient_idx, frozen_ingredient in enumerate(frozen_ingredients):
                frozen_ingredient_name = grocery_list_ingredient_names[frozen_ingredient]
                frozen_ingredient_amount = grocery_list_amounts[frozen_ingredient]
                frozen_ingredient_unit_of_measure = grocery_list_ingredient_units_of_measure[frozen_ingredient]
                yield Label(f"{frozen_ingredient_name} ({frozen_ingredient_amount} {frozen_ingredient_unit_of_measure})")

        if len(pantry_ingredients) > 0:
            yield Label("Pantry")
            for pantry_ingredient_idx, pantry_ingredient in enumerate(pantry_ingredients):
                pantry_ingredient_name = grocery_list_ingredient_names[pantry_ingredient]
                pantry_ingredient_amount = grocery_list_amounts[pantry_ingredient]
                pantry_ingredient_unit_of_measure = grocery_list_ingredient_units_of_measure[pantry_ingredient]
                yield Label(f"{pantry_ingredient_name} ({pantry_ingredient_amount} {pantry_ingredient_unit_of_measure})")

        if len(other_ingredients) > 0:
            yield Label("Other")
            for other_ingredient_idx, other_ingredient in enumerate(other_ingredients):
                other_ingredient_name = grocery_list_ingredient_names[other_ingredient]
                other_ingredient_amount = grocery_list_amounts[other_ingredient]
                other_ingredient_unit_of_measure = grocery_list_ingredient_units_of_measure[other_ingredient]
                yield Label(f"{other_ingredient_name} ({other_ingredient_amount} {other_ingredient_unit_of_measure})")

        yield Footer()

class ViewMenuScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    view_menu_id = None
    menu_total_servings_label = None

    def __init__(self, view_menu_id: int) -> None:
        self.view_menu_id = view_menu_id
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("View Menu", id="title")

        menu_name = None
        menu_recipes = None
        for menu in menus:
            if int(menu["id"]) == int(self.view_menu_id):
                menu_name = menu["name"]
                menu_recipes = menu["recipes"]
                break

        yield Label(f"Menu Name: {menu_name}")

        yield Label("Recipes")
        menu_total_servings = 0
        for menu_recipe_idx, menu_recipe in enumerate(menu_recipes):
            recipe_name = None
            recipe_servings = None
            recipe_time = None
            recipe_stars = None
            recipe_source = None

            for recipe in recipes.recipes:
                if int(recipe["id"]) == int(menu_recipe):
                    recipe_name = recipe["name"]
                    recipe_servings = int(recipe["servings"])
                    recipe_time = recipe["time"]
                    recipe_stars = recipe["stars"]
                    menu_total_servings += recipe_servings
                    recipe_source = recipe["source"]
                    break

            if recipe_source is not None and recipe_source != "":
                yield Label(f"{recipe_name} ({recipe_servings} servings) ({recipe_time}) {recipe_stars} stars ({recipe_source})")
            else:
                yield Label(f"{recipe_name} ({recipe_servings} servings) ({recipe_time}) {recipe_stars} stars")

        self.menu_total_servings_label = Label(f"Total Servings: {menu_total_servings}")
        yield self.menu_total_servings_label

        yield Button("Generate Grocery List", id="generate_grocery_list")

        yield Button("Delete Menu", id="delete_menu")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete_menu":
            for menu_idx, menu in enumerate(menus):
                if int(menu["id"]) == int(self.view_menu_id):
                    menu["deleted"] = True
            self.view_menu_id = None
            self.dismiss(None)
        elif event.button.id == "generate_grocery_list":
            grocery_list_menu_id = self.view_menu_id
            self.app.push_screen(GenerateGroceryListScreen(grocery_list_menu_id))

class ListMenusScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    list_view = None

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for menu_idx, menu in enumerate(menus):
            if not menu["deleted"]:
                self.list_view.append(ListItem(Label(menu["name"]), id=f'menu_{menu_idx}'))

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("List Menus", id="title")
        list_items = []
        for menu_idx, menu in enumerate(menus):
            if not menu["deleted"]:
                list_items.append(ListItem(Label(menu["name"]), id=f'menu_{menu_idx}'))
        self.list_view = ListView(*list_items)
        yield self.list_view
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        menu_idx = int(event.item.id[5:])
        menu_id = menus[menu_idx]["id"]

        self.app.push_screen(ViewMenuScreen(menu_id))

    @on(ScreenResume)
    async def handle_list_menus_screen_resumed(self) -> None:
        await self.refresh_list_view()

class MenusScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Menus", id="title")
        yield ListView(ListItem(Label("Add Menu"), id="add_menu"),
                       ListItem(Label("List Menus"), id="list_menus"))
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id == "add_menu":
            self.app.push_screen("add_menu")
        elif event.item.id == "list_menus":
            self.app.push_screen("list_menus")