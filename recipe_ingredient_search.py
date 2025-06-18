from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button, Checkbox

import ingredients_util
import recipes_util

class RecipeIngredientSearchScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    name_matches = []
    id_matches = []

    ingredient_name_input = None
    list_view = None
    ingredient_amount_input = None
    ingredient_optional_checkbox = None

    async def clear_ingredient_search(self) -> None:
        self.name_matches = []
        self.id_matches = []
        self.ingredient_name_input.value = ""
        await self.list_view.clear()
        self.ingredient_amount_input.value = "0"
        self.ingredient_optional_checkbox.value = False

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for name_match_idx, name_match in enumerate(self.name_matches):
            id_match = self.id_matches[name_match_idx]
            ingredient_unit_of_measure = None
            ingredient_category = None
            for ingredient in ingredients_util.ingredients:
                if int(ingredient["id"]) == int(id_match):
                    ingredient_unit_of_measure = ingredient["unit_of_measure"].replace("_", " ")
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
        yield Label("Optional")
        self.ingredient_optional_checkbox = Checkbox(id="ingredient_optional_checkbox", value=False)
        yield self.ingredient_optional_checkbox
        yield Button("Add Ingredient", id="add_ingredient")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search_ingredient":
            self.name_matches = []
            self.id_matches = []

            self.name_matches, self.id_matches = recipes_util.search_ingredient(self.query_one("#ingredient_name").value)

            await self.refresh_list_view()
        elif event.button.id == "add_ingredient":
            if self.list_view.index is None:
                self.dismiss(None)
            else:
                ingredient_id = self.id_matches[self.list_view.index]
                ingredient_amount = float(self.query_one("#ingredient_amount").value)
                ingredient_optional_flag = self.ingredient_optional_checkbox.value

                await self.clear_ingredient_search()
                self.dismiss((ingredient_id, ingredient_amount, ingredient_optional_flag))