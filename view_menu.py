import pyperclip

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Button

import edit_menu
import generate_grocery_list
import menus_util
import recipes_util

class ViewMenuScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    view_menu_id = None
    menu_name_label = None
    menu_recipe_list = None
    menu_total_servings_label = None
    menu_average_stars_label = None

    def __init__(self, view_menu_id: int) -> None:
        self.view_menu_id = view_menu_id
        super().__init__()

    async def refresh_menu_form(self) -> None:
        menu_name = None
        menu_recipes = None
        for menu in menus_util.menus:
            if int(menu["id"]) == int(self.view_menu_id):
                menu_name = menu["name"]
                menu_recipes = menu["recipes"]
                break

        self.menu_name_label.update(f"Menu Name: {menu_name}")

        menu_total_servings = 0
        menu_total_stars = 0
        await self.menu_recipe_list.clear()
        for menu_recipe_idx, menu_recipe in enumerate(menu_recipes):
            recipe_name = None
            recipe_servings = None
            recipe_time = None
            recipe_stars = None
            recipe_source = None

            for recipe in recipes_util.recipes:
                if int(recipe["id"]) == int(menu_recipe):
                    recipe_name = recipe["name"]
                    recipe_servings = int(recipe["servings"])
                    recipe_time = recipe["time"]
                    recipe_stars = float(recipe["stars"])
                    menu_total_servings += recipe_servings
                    menu_total_stars += recipe_stars
                    recipe_source = recipe["source"]
                    break

            if recipe_source is not None and recipe_source != "":
                self.menu_recipe_list.append(ListItem(Label(f"{recipe_name} ({recipe_servings} servings) ({recipe_time}) {recipe_stars} stars ({recipe_source})"), id=f'menu_recipe_{menu_recipe_idx}'))
            else:
                self.menu_recipe_list.append(ListItem(Label(f"{recipe_name} ({recipe_servings} servings) ({recipe_time}) {recipe_stars} stars"), id=f'menu_recipe_{menu_recipe_idx}'))

        menu_average_stars = menu_total_stars / len(menu_recipes)

        self.menu_total_servings_label.update(f"Total Servings: {menu_total_servings}")
        self.menu_average_stars_label.update(f"Stars: {menu_average_stars:2.1f}")

    def compose(self) -> ComposeResult:
        menu_name = None
        menu_recipes = None
        for menu in menus_util.menus:
            if int(menu["id"]) == int(self.view_menu_id):
                menu_name = menu["name"]
                menu_recipes = menu["recipes"]
                break

        menu_total_servings = 0
        menu_total_stars = 0
        menu_recipe_list_items = []
        for menu_recipe_idx, menu_recipe in enumerate(menu_recipes):
            recipe_name = None
            recipe_servings = None
            recipe_time = None
            recipe_stars = None
            recipe_source = None

            for recipe in recipes_util.recipes:
                if int(recipe["id"]) == int(menu_recipe):
                    recipe_name = recipe["name"]
                    recipe_servings = int(recipe["servings"])
                    recipe_time = recipe["time"]
                    recipe_stars = float(recipe["stars"])
                    menu_total_servings += recipe_servings
                    menu_total_stars += recipe_stars
                    recipe_source = recipe["source"]
                    break

            if recipe_source is not None and recipe_source != "":
                menu_recipe_list_items.append(ListItem(Label(f"{recipe_name} ({recipe_servings} servings) ({recipe_time}) {recipe_stars} stars ({recipe_source})"), id=f'menu_recipe_{menu_recipe_idx}'))
            else:
                menu_recipe_list_items.append(ListItem(Label(f"{recipe_name} ({recipe_servings} servings) ({recipe_time}) {recipe_stars} stars"), id=f'menu_recipe_{menu_recipe_idx}'))

        menu_average_stars = menu_total_stars / len(menu_recipes)

        yield Header()
        yield Static("View Menu", id="title")
        self.menu_name_label = Label(f"Menu Name: {menu_name}")
        yield self.menu_name_label
        yield Label("Recipes")
        self.menu_recipe_list = ListView(*menu_recipe_list_items)
        yield self.menu_recipe_list
        self.menu_total_servings_label = Label(f"Total Servings: {menu_total_servings}")
        yield self.menu_total_servings_label
        self.menu_average_stars_label = Label(f"Stars: {menu_average_stars:2.1f}")
        yield self.menu_average_stars_label
        yield Button("Copy to Clipboard", id="copy_to_clipboard")
        yield Button("Generate Grocery List", id="generate_grocery_list")
        yield Button("Edit Menu", id="edit_menu")
        yield Button("Delete Menu", id="delete_menu")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete_menu":
            for menu_idx, menu in enumerate(menus_util.menus):
                if int(menu["id"]) == int(self.view_menu_id):
                    menu["deleted"] = True
            self.view_menu_id = None
            self.dismiss(None)
        elif event.button.id == "edit_menu":
            menu_screen = self

            async def edit_menu_callback(menu_id) -> None:
                await menu_screen.refresh_menu_form()

            self.app.push_screen(edit_menu.EditMenuScreen(self.view_menu_id), edit_menu_callback)
        elif event.button.id == "generate_grocery_list":
            grocery_list_menu_id = self.view_menu_id
            self.app.push_screen(generate_grocery_list.GenerateGroceryListScreen(grocery_list_menu_id))
        elif event.button.id == "copy_to_clipboard":
            menu_name = None
            menu_recipes = None
            for menu in menus_util.menus:
                if int(menu["id"]) == int(self.view_menu_id):
                    menu_name = menu["name"]
                    menu_recipes = menu["recipes"]
                    break

            menu_text = f"Menu: {menu_name}\n"
            menu_text += "\n"

            menu_total_servings = 0
            menu_total_stars = 0
            menu_recipe_list_items = []
            for menu_recipe_idx, menu_recipe in enumerate(menu_recipes):
                recipe_name = None
                recipe_servings = None
                recipe_time = None
                recipe_stars = None
                recipe_source = None

                for recipe in recipes_util.recipes:
                    if int(recipe["id"]) == int(menu_recipe):
                        recipe_name = recipe["name"]
                        recipe_servings = int(recipe["servings"])
                        recipe_time = recipe["time"]
                        recipe_stars = float(recipe["stars"])
                        menu_total_servings += recipe_servings
                        menu_total_stars += recipe_stars
                        recipe_source = recipe["source"]
                        break

                if recipe_source is not None and recipe_source != "":
                    menu_text += f"{recipe_name} ({recipe_servings} servings) ({recipe_time}) {recipe_stars} stars ({recipe_source})\n"
                else:
                    menu_text += f"{recipe_name} ({recipe_servings} servings) ({recipe_time}) {recipe_stars} stars\n"

            menu_average_stars = menu_total_stars / len(menu_recipes)

            menu_text += "\n"
            menu_text += f"Total Servings: {menu_total_servings}\n"
            menu_text += f"Stars: {menu_average_stars:2.1f}\n"

            pyperclip.copy(menu_text)