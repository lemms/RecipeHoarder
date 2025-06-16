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
        self.unit_of_measure_list = ListView(ListItem(Label("lbs"), id="unit_lbs"),
                                             ListItem(Label("oz"), id="unit_oz"),
                                             ListItem(Label("fl oz"), id="unit_fl_oz"),
                                             ListItem(Label("cans"), id="unit_cans"),
                                             ListItem(Label("bottles"), id="unit_bottles"),
                                             ListItem(Label("boxes"), id="unit_boxes"),
                                             ListItem(Label("jars"), id="unit_jars"),
                                             ListItem(Label("bags"), id="unit_bags"),
                                             ListItem(Label("cartons"), id="unit_cartons"),
                                             ListItem(Label("packages"), id="unit_packages"),
                                             ListItem(Label("pieces"), id="unit_pieces"),
                                             ListItem(Label("cups"), id="unit_cups"),
                                             ListItem(Label("tsp"), id="unit_tsp"),
                                             ListItem(Label("tbsp"), id="unit_tbsp"),
                                             ListItem(Label("cloves"), id="unit_cloves"),
                                             ListItem(Label("g"), id="unit_g"),
                                             ListItem(Label("kg"), id="unit_kg"),
                                             ListItem(Label("ml"), id="unit_ml"),
                                             ListItem(Label("l"), id="unit_l"),
                                             ListItem(Label("pints"), id="unit_pints"),
                                             ListItem(Label("quarts"), id="unit_quarts"),
                                             ListItem(Label("gallons"), id="unit_gallons"),
                                             ListItem(Label("heads"), id="unit_heads"),
                                             ListItem(Label("bunches"), id="unit_bunches"),
                                             ListItem(Label("bulbs"), id="unit_bulbs"),
                                             id="unit_of_measure_list")
        yield self.unit_of_measure_list
        yield Label("Category")
        self.category_list = ListView(ListItem(Label("Produce"), id="category_produce"),
                                      ListItem(Label("Dairy"), id="category_dairy"),
                                      ListItem(Label("Meat"), id="category_meat"),
                                      ListItem(Label("Seafood"), id="category_seafood"),
                                      ListItem(Label("Bakery"), id="category_bakery"),
                                      ListItem(Label("Frozen"), id="category_frozen"),
                                      ListItem(Label("Pantry"), id="category_pantry"),
                                      ListItem(Label("Other"), id="category_other"))
        yield self.category_list
        yield Button("Submit", id="add_ingredient")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_ingredient":
            unit_of_measure = self.unit_of_measure_list.children[self.unit_of_measure_list.index].id[5:]
            category = self.category_list.children[self.category_list.index].id[9:]
            max_id = find_max_ingredient_id()

            ingredients.append({"id": max_id + 1, "name": self.query_one("#ingredient_name").value, "unit_of_measure": unit_of_measure, "deleted": False, "category": category})

            self.clear_ingredient_form()

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
        ingredient_category = None
        for ingredient in ingredients:
            if int(ingredient["id"]) == int(self.view_ingredient_id):
                ingredient_name = ingredient["name"]
                ingredient_unit_of_measure = ingredient["unit_of_measure"]
                ingredient_category = ingredient["category"]

        yield Label(f"Ingredient Name: {ingredient_name}")
        yield Label(f"Unit of Measure: {ingredient_unit_of_measure}")
        yield Label(f"Category: {ingredient_category}")
        yield Button("Delete Ingredient", id="delete_ingredient")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete_ingredient":
            for ingredient_idx, ingredient in enumerate(ingredients):
                if int(ingredient["id"]) == int(self.view_ingredient_id):
                    ingredient["deleted"] = True

            self.view_ingredient_id = None

            self.dismiss(None)

class ListIngredientsScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    list_view = None

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for ingredient_idx, ingredient in enumerate(ingredients):
            if not ingredient["deleted"]:
                self.list_view.append(ListItem(Label(f'{ingredient["name"]} ({ingredient["unit_of_measure"]}) ({ingredient["category"]})'), id=f'ingredient_{ingredient_idx}'))

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
        ingredient_idx = int(event.item.id[11:])
        ingredient_id = ingredients[ingredient_idx]["id"]

        self.app.push_screen(ViewIngredientScreen(ingredient_id))

    @on(ScreenResume)
    async def handle_list_ingredients_screen_resumed(self) -> None:
        await self.refresh_list_view()

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