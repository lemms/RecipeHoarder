from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem

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