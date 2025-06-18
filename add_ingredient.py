from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, Input, Button

import ingredients_util
import util

class AddIngredientScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    ingredient_name_input = None
    unit_of_measure_list = None
    category_list = None

    def clear_ingredient_form(self) -> None:
        self.ingredient_name_input.value = ""
        self.unit_of_measure_list.index = 0
        self.category_list.index = 0

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Add Ingredient", id="title")
        self.ingredient_name_input = Input(placeholder="Ingredient Name", id="ingredient_name", type="text")
        yield self.ingredient_name_input
        yield Label("Unit of Measure")
        self.unit_of_measure_list = ingredients_util.create_unit_of_measure_list_view()
        yield self.unit_of_measure_list
        yield Label("Category")
        self.category_list = ingredients_util.create_category_list_view()
        yield self.category_list
        yield Button("Submit", id="add_ingredient")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_ingredient":
            unit_of_measure = self.unit_of_measure_list.children[self.unit_of_measure_list.index].id[5:]
            category = self.category_list.children[self.category_list.index].id[9:]
            max_id = ingredients_util.find_max_ingredient_id()

            ingredients_util.ingredients.append({"id": max_id + 1, "name": self.query_one("#ingredient_name").value, "unit_of_measure": unit_of_measure, "deleted": False, "category": category})
            util.save_data()

            self.clear_ingredient_form()

            self.app.pop_screen()
