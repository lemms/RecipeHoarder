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

units_of_measure = ["lbs",
                    "oz",
                    "fl_oz",
                    "tsp",
                    "tbsp",
                    "cups",
                    "pieces",
                    "cans",
                    "bags",
                    "packages",
                    "bottles",
                    "boxes",
                    "jars",
                    "cartons",
                    "containers",
                    "cloves",
                    "loaves",
                    "slices",
                    "g",
                    "kg",
                    "ml",
                    "l",
                    "pints",
                    "quarts",
                    "gallons",
                    "heads",
                    "bunches",
                    "bulbs"]

def create_unit_of_measure_list_view() -> ListView:
    list_items = []
    for unit_of_measure in units_of_measure:
        list_items.append(ListItem(Label(unit_of_measure.replace("_", " ")), id=f"unit_{unit_of_measure}"))

    return ListView(*list_items, id="unit_of_measure_list")

def unit_of_measure_list_index(unit_of_measure: str) -> int:
    return units_of_measure.index(unit_of_measure)

categories = ["Produce",
              "Dairy",
              "Meat",
              "Seafood",
              "Bakery",
              "Frozen",
              "Pantry",
              "Other"]

categories_lower = [category.lower() for category in categories]

def create_category_list_view() -> ListView:
    list_items = []
    for category in categories:
        list_items.append(ListItem(Label(category), id=f"category_{category.lower()}"))

    return ListView(*list_items, id="category_list")

def category_list_index(category: str) -> int:
    return categories_lower.index(category.lower())

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
        self.unit_of_measure_list = create_unit_of_measure_list_view()
        yield self.unit_of_measure_list
        yield Label("Category")
        self.category_list = create_category_list_view()
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

        for ingredient in ingredients:
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
        self.unit_of_measure_list = create_unit_of_measure_list_view()
        self.unit_of_measure_list._initial_index = unit_of_measure_list_index(unit_of_measure)
        yield self.unit_of_measure_list
        yield Label("Category")
        self.category_list = create_category_list_view()
        self.category_list._initial_index = category_list_index(category)
        yield self.category_list
        yield Button("Submit", id="edit_ingredient")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "edit_ingredient":
            unit_of_measure = self.unit_of_measure_list.children[self.unit_of_measure_list.index].id[5:]
            category = self.category_list.children[self.category_list.index].id[9:]

            for ingredient in ingredients:
                if int(ingredient["id"]) == int(self.edit_ingredient_id):
                    ingredient["name"] = self.query_one("#ingredient_name").value
                    ingredient["unit_of_measure"] = unit_of_measure
                    ingredient["deleted"] = False
                    ingredient["category"] = category
                    break

            self.clear_ingredient_form()

            self.dismiss(self.edit_ingredient_id)

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

        for ingredient in ingredients:
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

        for ingredient in ingredients:
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
            for ingredient_idx, ingredient in enumerate(ingredients):
                if int(ingredient["id"]) == int(self.view_ingredient_id):
                    ingredient["deleted"] = True

            self.view_ingredient_id = None

            self.dismiss(None)
        elif event.button.id == "edit_ingredient":
            ingredient_screen = self

            async def edit_ingredient(ingredient_id) -> None:
                ingredient_screen.refresh_ingredient_form()

            self.app.push_screen(EditIngredientScreen(self.view_ingredient_id), edit_ingredient)

class ListIngredientsScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    list_view = None
    ingredient_data = []

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        self.ingredient_data = []

        for ingredient_idx, ingredient in enumerate(ingredients):
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

        for ingredient_idx, ingredient in enumerate(ingredients):
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