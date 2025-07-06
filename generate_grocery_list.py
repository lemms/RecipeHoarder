import pyperclip

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, Button

import ingredients_util
import recipes_util
import menus_util

class GenerateGroceryListScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    grocery_list_menu_id = None

    menu_name = None
    grocery_list_ingredients = []
    grocery_list_amounts = []
    grocery_list_ingredient_names = []
    grocery_list_ingredient_units_of_measure = []
    grocery_list_ingredient_categories = []
    produce_ingredients = []
    dairy_ingredients = []
    meat_ingredients = []
    seafood_ingredients = []
    bakery_ingredients = []
    frozen_ingredients = []
    pantry_ingredients = []
    other_ingredients = []

    def __init__(self, grocery_list_menu_id: int) -> None:
        self.grocery_list_menu_id = grocery_list_menu_id
        super().__init__()

    def clear_grocery_list(self) -> None:
        self.grocery_list_ingredients = []
        self.grocery_list_amounts = []
        self.grocery_list_ingredient_names = []
        self.grocery_list_ingredient_units_of_measure = []
        self.grocery_list_ingredient_categories = []
        self.produce_ingredients = []
        self.dairy_ingredients = []
        self.meat_ingredients = []
        self.seafood_ingredients = []
        self.bakery_ingredients = []
        self.frozen_ingredients = []
        self.pantry_ingredients = []
        self.other_ingredients = []

    def compose(self) -> ComposeResult:
        self.clear_grocery_list()

        menu_recipes = []
        for menu in menus_util.menus:
            if int(menu["id"]) == int(self.grocery_list_menu_id):
                menu_recipes = menu["recipes"]
                self.menu_name = menu["name"]
                break

        for menu_recipe in menu_recipes:
            for recipe in recipes_util.recipes:
                if int(recipe["id"]) == int(menu_recipe):
                    for recipe_ingredient_idx, recipe_ingredient in enumerate(recipe["ingredients"]):
                        try:
                            ingredient_idx = self.grocery_list_ingredients.index(recipe_ingredient)
                            self.grocery_list_amounts[ingredient_idx] += float(recipe["amounts"][recipe_ingredient_idx])
                        except ValueError:
                            self.grocery_list_ingredients.append(recipe_ingredient)
                            self.grocery_list_amounts.append(float(recipe["amounts"][recipe_ingredient_idx]))

        for grocery_list_ingredient_idx, grocery_list_ingredient_id in enumerate(self.grocery_list_ingredients):
            for ingredient in ingredients_util.ingredients:
                if int(ingredient["id"]) == int(grocery_list_ingredient_id):
                    self.grocery_list_ingredient_names.append(ingredient["name"])
                    self.grocery_list_ingredient_units_of_measure.append(ingredient["unit_of_measure"])
                    self.grocery_list_ingredient_categories.append(ingredient["category"])
                    break

        for grocery_list_ingredient_idx, grocery_list_ingredient_id in enumerate(self.grocery_list_ingredients):
            ingredient_category = None

            for ingredient in ingredients_util.ingredients:
                if int(ingredient["id"]) == int(grocery_list_ingredient_id):
                    ingredient_category = ingredient["category"]
                    break

            if ingredient_category == "produce":
                self.produce_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "dairy":
                self.dairy_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "meat":
                self.meat_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "seafood":
                self.seafood_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "bakery":
                self.bakery_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "frozen":
                self.frozen_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "pantry":
                self.pantry_ingredients.append(grocery_list_ingredient_idx)
            elif ingredient_category == "other":
                self.other_ingredients.append(grocery_list_ingredient_idx)
            else:
                raise Exception(f'Invalid ingredient category: {ingredient_category}')

        yield Header()
        yield Static("Grocery List", id="title")
        yield Label(f"Menu: {self.menu_name}")

        if len(self.produce_ingredients) > 0:
            yield Label("Produce")
            for produce_ingredient_idx, produce_ingredient in enumerate(self.produce_ingredients):
                produce_ingredient_name = self.grocery_list_ingredient_names[produce_ingredient]
                produce_ingredient_amount = self.grocery_list_amounts[produce_ingredient]
                produce_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[produce_ingredient]
                yield Label(f"{produce_ingredient_name} ({produce_ingredient_amount} {produce_ingredient_unit_of_measure})")

        if len(self.dairy_ingredients) > 0:
            yield Label("Dairy")
            for dairy_ingredient_idx, dairy_ingredient in enumerate(self.dairy_ingredients):
                dairy_ingredient_name = self.grocery_list_ingredient_names[dairy_ingredient]
                dairy_ingredient_amount = self.grocery_list_amounts[dairy_ingredient]
                dairy_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[dairy_ingredient]
                yield Label(f"{dairy_ingredient_name} ({dairy_ingredient_amount} {dairy_ingredient_unit_of_measure})")

        if len(self.meat_ingredients) > 0:
            yield Label("Meat")
            for meat_ingredient_idx, meat_ingredient in enumerate(self.meat_ingredients):
                meat_ingredient_name = self.grocery_list_ingredient_names[meat_ingredient]
                meat_ingredient_amount = self.grocery_list_amounts[meat_ingredient]
                meat_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[meat_ingredient]
                yield Label(f"{meat_ingredient_name} ({meat_ingredient_amount} {meat_ingredient_unit_of_measure})")

        if len(self.seafood_ingredients) > 0:
            yield Label("Seafood")
            for seafood_ingredient_idx, seafood_ingredient in enumerate(self.seafood_ingredients):
                seafood_ingredient_name = self.grocery_list_ingredient_names[seafood_ingredient]
                seafood_ingredient_amount = self.grocery_list_amounts[seafood_ingredient]
                seafood_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[seafood_ingredient]
                yield Label(f"{seafood_ingredient_name} ({seafood_ingredient_amount} {seafood_ingredient_unit_of_measure})")

        if len(self.bakery_ingredients) > 0:
            yield Label("Bakery")
            for bakery_ingredient_idx, bakery_ingredient in enumerate(self.bakery_ingredients):
                bakery_ingredient_name = self.grocery_list_ingredient_names[bakery_ingredient]
                bakery_ingredient_amount = self.grocery_list_amounts[bakery_ingredient]
                bakery_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[bakery_ingredient]
                yield Label(f"{bakery_ingredient_name} ({bakery_ingredient_amount} {bakery_ingredient_unit_of_measure})")

        if len(self.frozen_ingredients) > 0:
            yield Label("Frozen")
            for frozen_ingredient_idx, frozen_ingredient in enumerate(self.frozen_ingredients):
                frozen_ingredient_name = self.grocery_list_ingredient_names[frozen_ingredient]
                frozen_ingredient_amount = self.grocery_list_amounts[frozen_ingredient]
                frozen_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[frozen_ingredient]
                yield Label(f"{frozen_ingredient_name} ({frozen_ingredient_amount} {frozen_ingredient_unit_of_measure})")

        if len(self.pantry_ingredients) > 0:
            yield Label("Pantry")
            for pantry_ingredient_idx, pantry_ingredient in enumerate(self.pantry_ingredients):
                pantry_ingredient_name = self.grocery_list_ingredient_names[pantry_ingredient]
                pantry_ingredient_amount = self.grocery_list_amounts[pantry_ingredient]
                pantry_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[pantry_ingredient]
                yield Label(f"{pantry_ingredient_name} ({pantry_ingredient_amount} {pantry_ingredient_unit_of_measure})")

        if len(self.other_ingredients) > 0:
            yield Label("Other")
            for other_ingredient_idx, other_ingredient in enumerate(self.other_ingredients):
                other_ingredient_name = self.grocery_list_ingredient_names[other_ingredient]
                other_ingredient_amount = self.grocery_list_amounts[other_ingredient]
                other_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[other_ingredient]
                yield Label(f"{other_ingredient_name} ({other_ingredient_amount} {other_ingredient_unit_of_measure})")

        yield Button("Copy to Clipboard", id="copy_to_clipboard")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "copy_to_clipboard":
            grocery_list_text = ""
            grocery_list_text += f"Grocery List\n"
            grocery_list_text += f"Menu: {self.menu_name}\n"
            grocery_list_text += "\n"

            if len(self.produce_ingredients) > 0:
                grocery_list_text += "Produce\n"
                grocery_list_text += "-------\n"
                for produce_ingredient_idx, produce_ingredient in enumerate(self.produce_ingredients):
                    produce_ingredient_name = self.grocery_list_ingredient_names[produce_ingredient]
                    produce_ingredient_amount = self.grocery_list_amounts[produce_ingredient]
                    produce_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[produce_ingredient]
                    grocery_list_text += f"{produce_ingredient_name} ({produce_ingredient_amount} {produce_ingredient_unit_of_measure})\n"
                grocery_list_text += "\n"

            if len(self.dairy_ingredients) > 0:
                grocery_list_text += "Dairy\n"
                grocery_list_text += "-----\n"
                for dairy_ingredient_idx, dairy_ingredient in enumerate(self.dairy_ingredients):
                    dairy_ingredient_name = self.grocery_list_ingredient_names[dairy_ingredient]
                    dairy_ingredient_amount = self.grocery_list_amounts[dairy_ingredient]
                    dairy_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[dairy_ingredient]
                    grocery_list_text += f"{dairy_ingredient_name} ({dairy_ingredient_amount} {dairy_ingredient_unit_of_measure})\n"
                grocery_list_text += "\n"

            if len(self.meat_ingredients) > 0:
                grocery_list_text += "Meat\n"
                grocery_list_text += "----\n"
                for meat_ingredient_idx, meat_ingredient in enumerate(self.meat_ingredients):
                    meat_ingredient_name = self.grocery_list_ingredient_names[meat_ingredient]
                    meat_ingredient_amount = self.grocery_list_amounts[meat_ingredient]
                    meat_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[meat_ingredient]
                    grocery_list_text += f"{meat_ingredient_name} ({meat_ingredient_amount} {meat_ingredient_unit_of_measure})\n"
                grocery_list_text += "\n"

            if len(self.seafood_ingredients) > 0:
                grocery_list_text += "Seafood\n"
                grocery_list_text += "-------\n"
                for seafood_ingredient_idx, seafood_ingredient in enumerate(self.seafood_ingredients):
                    seafood_ingredient_name = self.grocery_list_ingredient_names[seafood_ingredient]
                    seafood_ingredient_amount = self.grocery_list_amounts[seafood_ingredient]
                    seafood_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[seafood_ingredient]
                    grocery_list_text += f"{seafood_ingredient_name} ({seafood_ingredient_amount} {seafood_ingredient_unit_of_measure})\n"
                grocery_list_text += "\n"

            if len(self.bakery_ingredients) > 0:
                grocery_list_text += "Bakery\n"
                grocery_list_text += "------\n"
                for bakery_ingredient_idx, bakery_ingredient in enumerate(self.bakery_ingredients):
                    bakery_ingredient_name = self.grocery_list_ingredient_names[bakery_ingredient]
                    bakery_ingredient_amount = self.grocery_list_amounts[bakery_ingredient]
                    bakery_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[bakery_ingredient]
                    grocery_list_text += f"{bakery_ingredient_name} ({bakery_ingredient_amount} {bakery_ingredient_unit_of_measure})\n"
                grocery_list_text += "\n"

            if len(self.frozen_ingredients) > 0:
                grocery_list_text += "Frozen\n"
                grocery_list_text += "------\n"
                for frozen_ingredient_idx, frozen_ingredient in enumerate(self.frozen_ingredients):
                    frozen_ingredient_name = self.grocery_list_ingredient_names[frozen_ingredient]
                    frozen_ingredient_amount = self.grocery_list_amounts[frozen_ingredient]
                    frozen_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[frozen_ingredient]
                    grocery_list_text += f"{frozen_ingredient_name} ({frozen_ingredient_amount} {frozen_ingredient_unit_of_measure})\n"
                grocery_list_text += "\n"

            if len(self.pantry_ingredients) > 0:
                grocery_list_text += "Pantry\n"
                grocery_list_text += "------\n"
                for pantry_ingredient_idx, pantry_ingredient in enumerate(self.pantry_ingredients):
                    pantry_ingredient_name = self.grocery_list_ingredient_names[pantry_ingredient]
                    pantry_ingredient_amount = self.grocery_list_amounts[pantry_ingredient]
                    pantry_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[pantry_ingredient]
                    grocery_list_text += f"{pantry_ingredient_name} ({pantry_ingredient_amount} {pantry_ingredient_unit_of_measure})\n"
                grocery_list_text += "\n"

            if len(self.other_ingredients) > 0:
                grocery_list_text += "Other\n"
                grocery_list_text += "-----\n"
                for other_ingredient_idx, other_ingredient in enumerate(self.other_ingredients):
                    other_ingredient_name = self.grocery_list_ingredient_names[other_ingredient]
                    other_ingredient_amount = self.grocery_list_amounts[other_ingredient]
                    other_ingredient_unit_of_measure = self.grocery_list_ingredient_units_of_measure[other_ingredient]
                    grocery_list_text += f"{other_ingredient_name} ({other_ingredient_amount} {other_ingredient_unit_of_measure})\n"
                grocery_list_text += "\n"

            pyperclip.copy(grocery_list_text)