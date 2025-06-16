from textual import on
from textual.app import ComposeResult
from textual.events import ScreenResume
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button
from textual.containers import HorizontalGroup

ingredients = []

def find_max_ingredient_id() -> int:
    max_id = 0

    for ingredient in ingredients:
        if int(ingredient["id"]) > max_id:
            max_id = int(ingredient["id"])

    return max_id

class AddIngredientScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Add Ingredient", id="title")
        yield Input(placeholder="Ingredient Name", id="ingredient_name", type="text")
        yield Label("Unit of Measure")
        yield ListView(ListItem(Label("lbs"), id="unit_lbs"),
                       ListItem(Label("oz"), id="unit_oz"),
                       ListItem(Label("g"), id="unit_g"),
                       ListItem(Label("kg"), id="unit_kg"),
                       ListItem(Label("ml"), id="unit_ml"),
                       ListItem(Label("l"), id="unit_l"),
                       ListItem(Label("cups"), id="unit_cups"),
                       ListItem(Label("tsp"), id="unit_tsp"),
                       ListItem(Label("tbsp"), id="unit_tbsp"),
                       ListItem(Label("fl oz"), id="unit_fl_oz"),
                       ListItem(Label("pints"), id="unit_pints"),
                       ListItem(Label("quarts"), id="unit_quarts"),
                       ListItem(Label("gallons"), id="unit_gallons"),
                       ListItem(Label("pieces"), id="pieces"),
                       id="unit_of_measure_list")
        yield Button("Submit", id="add_ingredient")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_ingredient":
            unit_of_measure_list = self.query_one("#unit_of_measure_list")
            unit_of_measure = unit_of_measure_list.children[unit_of_measure_list.index].id[5:]
            max_id = find_max_ingredient_id()
            ingredients.append({"id": max_id + 1, "name": self.query_one("#ingredient_name").value, "unit_of_measure": unit_of_measure, "deleted": False})
            self.app.pop_screen()

class ViewIngredientScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    view_ingredient_id = None

    def __init__(self, view_ingredient_id: int):
        self.view_ingredient_id = view_ingredient_id
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("View Ingredient", id="title")

        ingredient_name = None
        ingredient_unit_of_measure = None
        for ingredient in ingredients:
            if int(ingredient["id"]) == int(self.view_ingredient_id):
                ingredient_name = ingredient["name"]
                ingredient_unit_of_measure = ingredient["unit_of_measure"]

        yield Label(f"Ingredient Name: {ingredient_name}")
        yield Label(f"Unit of Measure: {ingredient_unit_of_measure}")
        yield Button("Delete Ingredient", id="delete_ingredient")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete_ingredient":
            for ingredient_idx, ingredient in enumerate(ingredients):
                if int(ingredient["id"]) == int(self.view_ingredient_id):
                    ingredient["deleted"] = True

            self.dismiss(None)

class ListIngredientsScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    list_view = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("List Ingredients", id="title")
        list_items = []
        for ingredient_idx, ingredient in enumerate(ingredients):
            if not ingredient["deleted"]:
                list_items.append(ListItem(Label(ingredient["name"]), id=f'ingredient_{ingredient_idx}'))
        self.list_view = ListView(*list_items)
        yield self.list_view
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        ingredient_id = event.item.id[11:]

        self.app.push_screen(ViewIngredientScreen(ingredient_id))

    @on(ScreenResume)
    async def handle_list_ingredients_screen_resumed(self) -> None:
        await self.list_view.clear()

        for ingredient_idx, ingredient in enumerate(ingredients):
            if not ingredient["deleted"]:
                self.list_view.append(ListItem(Label(ingredient["name"]), id=f'ingredient_{ingredient_idx}'))

class IngredientsScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Ingredients", id="title")
        yield ListView(ListItem(Label("Add Ingredient"), id="add_ingredient"),
                       ListItem(Label("List Ingredients"), id="list_ingredients"))
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id == "add_ingredient":
            self.app.push_screen("add_ingredient")
        elif event.item.id == "list_ingredients":
            self.app.push_screen("list_ingredients")