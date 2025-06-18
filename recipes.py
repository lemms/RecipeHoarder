from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem

class RecipesScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Recipes", id="title")
        yield ListView(ListItem(Label("Add Recipe"), id="add_recipe"),
                       ListItem(Label("List Recipes"), id="list_recipes"))
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id == "add_recipe":
            self.app.push_screen("add_recipe")
        elif event.item.id == "list_recipes":
            self.app.push_screen("list_recipes")