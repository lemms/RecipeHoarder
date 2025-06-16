from fuzzywuzzy import process

from textual import on
from textual.app import ComposeResult
from textual.events import ScreenResume
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button
from textual.containers import HorizontalGroup

import recipes

menus = []

def find_max_menu_id() -> int:
    max_id = 0

    for menu in menus:
        if int(menu["id"]) > max_id:
            max_id = int(menu["id"])

    return max_id

def search_recipe(recipe_name: str, match_limit: int = 10) -> list:
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
        self.name_matches.clear()
        self.id_matches.clear()
        self.recipe_name_input.value = ""
        await self.list_view.clear()

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for name_match_idx, name_match in enumerate(self.name_matches):
            self.list_view.append(ListItem(Label(name_match), id=f'search_recipe_{name_match_idx}'))

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
            self.name_matches.clear()
            self.id_matches.clear()

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
    menu_recipe_list = None

    async def clear_menu_form(self) -> None:
        self.menu_recipes = []
        self.menu_name_input.value = ""
        await self.menu_recipe_list.clear()

    async def refresh_list_view(self) -> None:
        await self.menu_recipe_list.clear()

        for menu_recipe_idx, menu_recipe in enumerate(self.menu_recipes):
            menu_recipe_name = None
            for recipe in recipes.recipes:
                if int(recipe["id"]) == int(menu_recipe):
                    menu_recipe_name = recipe["name"]

            self.menu_recipe_list.append(ListItem(Label(f'{menu_recipe_name}'), id=f'menu_recipe_{menu_recipe_idx}'))

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Add Menu", id="title")
        self.menu_name_input = Input(placeholder="Menu Name", id="menu_name", type="text")
        yield self.menu_name_input
        yield Button("Add Recipe", id="add_menu_recipe")
        yield Label("Recipes")
        self.menu_recipe_list = ListView()
        yield self.menu_recipe_list
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

        self.refresh_list_view()

class ViewMenuScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    view_menu_id = None

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
        for menu_recipe_idx, menu_recipe in enumerate(menu_recipes):
            recipe_name = None
            for recipe in recipes.recipes:
                if int(recipe["id"]) == int(menu_recipe):
                    recipe_name = recipe["name"]
                    break
            yield Label(f"{recipe_name}")

        yield Button("Delete Menu", id="delete_menu")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete_menu":
            for menu_idx, menu in enumerate(menus):
                if int(menu["id"]) == int(self.view_menu_id):
                    menu["deleted"] = True
            self.view_menu_id = None
            self.dismiss(None)

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