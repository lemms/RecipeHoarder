from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button
from textual.containers import HorizontalGroup

grocery_lists = []

def find_max_grocery_list_id() -> int:
    max_id = 0

    for grocery_list in grocery_lists:
        if int(grocery_list["id"]) > max_id:
            max_id = int(grocery_list["id"])

    return max_id

class AddGroceryListScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Add Grocery List", id="title")
        yield Input(placeholder="Grocery List Name", id="grocery_list_name", type="text")
        yield Button("Submit", id="add_grocery_list")
        yield Footer()

class EditGroceryListScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Edit Grocery List", id="title")
        yield Footer()

class ViewGroceryListScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("View Grocery List", id="title")
        yield Footer()

class ListGroceryListsScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("List Grocery Lists", id="title")
        list_items = []
        for grocery_list in grocery_lists:
            list_items.append(ListItem(Label(grocery_list["name"]), id=f'grocery_list_{grocery_list["id"]}'))
        yield ListView(*list_items)
        yield Footer()

class GroceryListsScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Grocery Lists", id="title")
        yield ListView(ListItem(Label("Add Grocery List"), id="add_grocery_list"),
                       ListItem(Label("List Grocery Lists"), id="list_grocery_lists"))
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id == "add_grocery_list":
            self.app.push_screen("add_grocery_list")
        elif event.item.id == "list_grocery_lists":
            self.app.push_screen("list_grocery_lists")