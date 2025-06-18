from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, Button

import edit_ingredient
import ingredients_util

class ViewIngredientScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    view_ingredient_id = None
    ingredient_name_label = None
    ingredient_unit_of_measure_label = None
    ingredient_category_label = None

    def __init__(self, view_ingredient_id: int):
        self.view_ingredient_id = view_ingredient_id
        super().__init__()

    def refresh_ingredient_form(self) -> None:
        ingredient_name = None
        ingredient_unit_of_measure = None
        ingredient_category = None

        for ingredient in ingredients_util.ingredients:
            if int(ingredient["id"]) == int(self.view_ingredient_id):
                ingredient_name = ingredient["name"]
                ingredient_unit_of_measure = ingredient["unit_of_measure"]
                ingredient_category = ingredient["category"]
                break
        
        self.ingredient_name_label.update(f"Ingredient Name: {ingredient_name}")
        self.ingredient_unit_of_measure_label.update(f"Unit of Measure: {ingredient_unit_of_measure}")
        self.ingredient_category_label.update(f"Category: {ingredient_category}") 

    def compose(self) -> ComposeResult:
        ingredient_name = None
        ingredient_unit_of_measure = None
        ingredient_category = None

        for ingredient in ingredients_util.ingredients:
            if int(ingredient["id"]) == int(self.view_ingredient_id):
                ingredient_name = ingredient["name"]
                ingredient_unit_of_measure = ingredient["unit_of_measure"]
                ingredient_category = ingredient["category"]
                break

        yield Header()
        yield Static("View Ingredient", id="title")
        self.ingredient_name_label = Label(f"Ingredient Name: {ingredient_name}")
        yield self.ingredient_name_label
        self.ingredient_unit_of_measure_label = Label(f"Unit of Measure: {ingredient_unit_of_measure}")
        yield self.ingredient_unit_of_measure_label
        self.ingredient_category_label = Label(f"Category: {ingredient_category}")
        yield self.ingredient_category_label
        yield Button("Edit Ingredient", id="edit_ingredient")
        yield Button("Delete Ingredient", id="delete_ingredient")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete_ingredient":
            for ingredient_idx, ingredient in enumerate(ingredients_util.ingredients):
                if int(ingredient["id"]) == int(self.view_ingredient_id):
                    ingredient["deleted"] = True

            self.view_ingredient_id = None

            self.dismiss(None)
        elif event.button.id == "edit_ingredient":
            ingredient_screen = self

            async def edit_ingredient_callback(ingredient_id) -> None:
                ingredient_screen.refresh_ingredient_form()

            self.app.push_screen(edit_ingredient.EditIngredientScreen(self.view_ingredient_id), edit_ingredient_callback)