from textual import on
from textual.app import ComposeResult
from textual.events import ScreenResume
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem

import ingredients_util
import view_ingredient

class ListIngredientsScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    list_view = None
    ingredient_data = []

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        self.ingredient_data = []

        for ingredient_idx, ingredient in enumerate(ingredients_util.ingredients):
            if not ingredient["deleted"]:
                self.ingredient_data.append({"index": ingredient_idx,
                                             "name": ingredient["name"],
                                             "unit_of_measure": ingredient["unit_of_measure"],
                                             "category": ingredient["category"]})

        self.ingredient_data.sort(key=lambda x: x["name"])

        for ingredient_datum_idx, ingredient_datum in enumerate(self.ingredient_data):
            self.list_view.append(ListItem(Label(f'{ingredient_datum["name"]} ({ingredient_datum["unit_of_measure"]}) ({ingredient_datum["category"]})'), id=f'ingredient_{ingredient_datum_idx}'))

    def compose(self) -> ComposeResult:
        self.ingredient_data = []

        for ingredient_idx, ingredient in enumerate(ingredients_util.ingredients):
            if not ingredient["deleted"]:
                self.ingredient_data.append({"index": ingredient_idx,
                                        "name": ingredient["name"],
                                        "unit_of_measure": ingredient["unit_of_measure"],
                                        "category": ingredient["category"]})

        self.ingredient_data.sort(key=lambda x: x["name"])

        list_items = []
        for ingredient_datum_idx, ingredient_datum in enumerate(self.ingredient_data):
            list_items.append(ListItem(Label(f'{ingredient_datum["name"]} ({ingredient_datum["unit_of_measure"]}) ({ingredient_datum["category"]})'), id=f'ingredient_{ingredient_datum_idx}'))

        yield Header()
        yield Static("List Ingredients", id="title")
        self.list_view = ListView(*list_items)
        yield self.list_view
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        ingredient_data_idx = int(event.item.id[11:])
        ingredient_idx = self.ingredient_data[ingredient_data_idx]["index"]

        ingredient_id = ingredients_util.ingredients[ingredient_idx]["id"]

        self.app.push_screen(view_ingredient.ViewIngredientScreen(ingredient_id))

    @on(ScreenResume)
    async def handle_list_ingredients_screen_resumed(self) -> None:
        await self.refresh_list_view()
