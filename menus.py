from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem

class MenusScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Menus", id="title")
        yield ListView(ListItem(Label("Add Menu"), id="add_menu"),
                       ListItem(Label("List Menus"), id="list_menus"))
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id == "add_menu":
            self.app.push_screen("add_menu")
        elif event.item.id == "list_menus":
            self.app.push_screen("list_menus")