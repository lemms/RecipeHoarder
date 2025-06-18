from textual import on
from textual.app import ComposeResult
from textual.events import ScreenResume
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem

import recipes_util
import view_recipe

class ListRecipesScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    list_view = None
    recipe_data = []

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        self.recipe_data = []

        for recipe_idx, recipe in enumerate(recipes_util.recipes):
            if not recipe["deleted"]:
                self.recipe_data.append({"index": recipe_idx,
                                         "name": recipe["name"],
                                         "servings": recipe["servings"],
                                         "time": recipe["time"],
                                         "stars": recipe["stars"],
                                         "source": recipe["source"]})

        self.recipe_data.sort(key=lambda x: x["name"])

        list_items = []
        for recipe_datum_idx, recipe_datum in enumerate(self.recipe_data):
            if recipe_datum["source"] != "":
                self.list_view.append(ListItem(Label(f'{recipe_datum["name"]} ({recipe_datum["servings"]} servings) ({recipe_datum["time"]}) {recipe_datum["stars"]} stars ({recipe_datum["source"]})'), id=f'recipe_{recipe_datum_idx}'))
            else:
                self.list_view.append(ListItem(Label(f'{recipe_datum["name"]} ({recipe_datum["servings"]} servings) ({recipe_datum["time"]}) {recipe_datum["stars"]} stars'), id=f'recipe_{recipe_datum_idx}'))

    def compose(self) -> ComposeResult:
        self.recipe_data = []

        for recipe_idx, recipe in enumerate(recipes_util.recipes):
            if not recipe["deleted"]:
                self.recipe_data.append({"index": recipe_idx,
                                         "name": recipe["name"],
                                         "servings": recipe["servings"],
                                         "time": recipe["time"],
                                         "stars": recipe["stars"],
                                         "source": recipe["source"]})

        self.recipe_data.sort(key=lambda x: x["name"])

        list_items = []
        for recipe_datum_idx, recipe_datum in enumerate(self.recipe_data):
            if recipe_datum["source"] != "":
                list_items.append(ListItem(Label(f'{recipe_datum["name"]} ({recipe_datum["servings"]} servings) ({recipe_datum["time"]}) {recipe_datum["stars"]} stars ({recipe_datum["source"]})'), id=f'recipe_{recipe_datum_idx}'))
            else:
                list_items.append(ListItem(Label(f'{recipe_datum["name"]} ({recipe_datum["servings"]} servings) ({recipe_datum["time"]}) {recipe_datum["stars"]} stars'), id=f'recipe_{recipe_datum_idx}'))

        yield Header()
        yield Static("List Recipes", id="title")
        self.list_view = ListView(*list_items, id="list_recipes")
        yield self.list_view
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        recipe_data_idx = int(event.item.id[7:])
        recipe_idx = self.recipe_data[recipe_data_idx]["index"]
        recipe_id = recipes_util.recipes[recipe_idx]["id"]

        self.app.push_screen(view_recipe.ViewRecipeScreen(recipe_id))

    @on(ScreenResume)
    async def handle_list_recipes_screen_resumed(self) -> None:
        await self.refresh_list_view()