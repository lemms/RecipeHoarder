from textual import on
from textual.app import ComposeResult
from textual.events import ScreenResume
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button
from textual.containers import HorizontalGroup

import ingredients_util

class EditIngredientScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    ingredient_name_input = None
    unit_of_measure_list = None
    category_list = None

    edit_ingredient_id = None

    def __init__(self, edit_ingredient_id: int):
        self.edit_ingredient_id = edit_ingredient_id
        super().__init__()

    def clear_ingredient_form(self) -> None:
        self.edit_ingredient_id = None
        self.ingredient_name_input.value = ""
        self.unit_of_measure_list.index = 0
        self.category_list.index = 0

    def compose(self) -> ComposeResult:
        ingredient_name = None
        unit_of_measure = None
        category = None

        for ingredient in ingredients_util.ingredients:
            if int(ingredient["id"]) == int(self.edit_ingredient_id):
                ingredient_name = ingredient["name"]
                unit_of_measure = ingredient["unit_of_measure"] 
                category = ingredient["category"]
                break

        yield Header()
        yield Static("Edit Ingredient", id="title")
        self.ingredient_name_input = Input(placeholder="Ingredient Name", id="ingredient_name", type="text", value=ingredient_name)
        yield self.ingredient_name_input
        yield Label("Unit of Measure")
        self.unit_of_measure_list = ingredients_util.create_unit_of_measure_list_view()
        self.unit_of_measure_list._initial_index = ingredients_util.unit_of_measure_list_index(unit_of_measure)
        yield self.unit_of_measure_list
        yield Label("Category")
        self.category_list = ingredients_util.create_category_list_view()
        self.category_list._initial_index = ingredients_util.category_list_index(category)
        yield self.category_list
        yield Button("Submit", id="edit_ingredient")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "edit_ingredient":
            unit_of_measure = self.unit_of_measure_list.children[self.unit_of_measure_list.index].id[5:]
            category = self.category_list.children[self.category_list.index].id[9:]

            for ingredient in ingredients_util.ingredients:
                if int(ingredient["id"]) == int(self.edit_ingredient_id):
                    ingredient["name"] = self.query_one("#ingredient_name").value
                    ingredient["unit_of_measure"] = unit_of_measure
                    ingredient["deleted"] = False
                    ingredient["category"] = category
                    break

            self.clear_ingredient_form()

            self.dismiss(self.edit_ingredient_id)