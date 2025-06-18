from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button

import menus_util
import recipes_util
import util

class EditMenuScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    edit_menu_id = None

    menu_recipes = []
    menu_name_input = None
    menu_total_servings_label = None
    menu_average_stars_label = None
    menu_recipe_list = None
    menu_servings = 0
    menu_total_stars = 0

    def __init__(self, edit_menu_id: int) -> None:
        self.edit_menu_id = edit_menu_id
        super().__init__()

    async def clear_menu_form(self) -> None:
        self.edit_menu_id = None
        self.menu_recipes = []
        self.menu_servings = 0
        self.menu_total_stars = 0
        self.menu_total_servings_label.update(f"Total Servings: {self.menu_servings}")
        self.menu_average_stars_label.update(f"Stars: 5.0")
        self.menu_name_input.value = ""

    async def refresh_list_view(self) -> None:
        await self.menu_recipe_list.clear()

        self.menu_servings = 0
        self.menu_total_stars = 0

        for menu_recipe_idx, menu_recipe in enumerate(self.menu_recipes):
            menu_recipe_name = None
            menu_recipe_time = None
            menu_recipe_servings = None
            menu_recipe_stars = None
            for recipe in recipes_util.recipes:
                if int(recipe["id"]) == int(menu_recipe):
                    menu_recipe_name = recipe["name"]
                    menu_recipe_time = recipe["time"]
                    menu_recipe_servings = int(recipe["servings"])
                    menu_recipe_stars = float(recipe["stars"])

                    self.menu_servings += menu_recipe_servings
                    self.menu_total_stars += menu_recipe_stars

            self.menu_recipe_list.append(ListItem(Label(f'{menu_recipe_name} ({menu_recipe_servings} servings) ({menu_recipe_time}) {menu_recipe_stars} stars'), id=f'menu_recipe_{menu_recipe_idx}'))

        menu_average_stars = self.menu_total_stars / len(self.menu_recipes)

        self.menu_total_servings_label.update(f"Total Servings: {self.menu_servings}")
        self.menu_total_servings_label.refresh()
        self.menu_average_stars_label.update(f"Stars: {menu_average_stars:2.1f}")
        self.menu_average_stars_label.refresh()

    def compose(self) -> ComposeResult:
        menu_name = None
        self.menu_recipes = None
        for menu in menus_util.menus:
            if int(menu["id"]) == int(self.edit_menu_id):
                menu_name = menu["name"]
                self.menu_recipes = menu["recipes"]
                break

        self.menu_servings = 0
        self.menu_total_stars = 0
        menu_recipe_list_items = []

        for menu_recipe_idx, menu_recipe in enumerate(self.menu_recipes):
            menu_recipe_name = None
            menu_recipe_time = None
            menu_recipe_servings = None
            menu_recipe_stars = None
            for recipe in recipes_util.recipes:
                if int(recipe["id"]) == int(menu_recipe):
                    menu_recipe_name = recipe["name"]
                    menu_recipe_time = recipe["time"]
                    menu_recipe_servings = int(recipe["servings"])
                    menu_recipe_stars = float(recipe["stars"])

                    self.menu_servings += menu_recipe_servings
                    self.menu_total_stars += menu_recipe_stars

                    menu_recipe_list_items.append(ListItem(Label(f'{menu_recipe_name} ({menu_recipe_servings} servings) ({menu_recipe_time}) {menu_recipe_stars} stars'), id=f'menu_recipe_{menu_recipe_idx}'))

        menu_average_stars = self.menu_total_stars / len(self.menu_recipes)

        yield Header()
        yield Static("Add Menu", id="title")
        self.menu_name_input = Input(placeholder="Menu Name", id="menu_name", type="text", value=menu_name)
        yield self.menu_name_input
        yield Button("Add Recipe", id="add_menu_recipe")
        yield Label("Recipes")
        self.menu_recipe_list = ListView(*menu_recipe_list_items)
        yield self.menu_recipe_list
        self.menu_total_servings_label = Label(f"Total Servings: {self.menu_servings}")
        yield self.menu_total_servings_label
        self.menu_average_stars_label = Label(f"Stars: {menu_average_stars:2.1f}")
        yield self.menu_average_stars_label
        yield Button("Submit", id="edit_menu")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_menu_recipe":
            async def add_menu_recipe(recipe_id) -> None:
                if recipe_id is not None:
                    self.menu_recipes.append(recipe_id)

                    if len(self.menu_recipes) > 0:
                        await self.refresh_list_view()

            self.app.push_screen("menu_recipe_search", add_menu_recipe)
        elif event.button.id == "edit_menu":
            menu_name = self.query_one("#menu_name").value

            if menu_name is None or menu_name == "":
                await self.clear_menu_form()
                self.app.pop_screen()
            else:
                for menu in menus_util.menus:
                    if int(menu["id"]) == int(self.edit_menu_id):
                        menu["name"] = menu_name
                        menu["recipes"] = self.menu_recipes
                        break

                util.save_data()

                await self.clear_menu_form()

                self.dismiss(self.edit_menu_id)

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        del self.menu_recipes[int(event.item.id[12:])]

        await self.refresh_list_view()