from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button
from textual.containers import HorizontalGroup

menus = []

def find_max_menu_id() -> int:
    max_id = 0

    for menu in menus:
        if int(menu["id"]) > max_id:
            max_id = int(menu["id"])

    return max_id

class AddMenuScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Add Menu", id="title")
        yield Input(placeholder="Menu Name", id="menu_name", type="text")
        yield Button("Submit", id="add_menu")
        yield Footer()

class EditMenuScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Edit Menu", id="title")
        yield Footer()

class ViewMenuScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("View Menu", id="title")
        yield Footer()

class ListMenusScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("List Menus", id="title")
        list_items = []
        for menu in menus:
            list_items.append(ListItem(Label(menu["name"]), id=f'menu_{menu["id"]}'))
        yield ListView(*list_items)
        yield Footer()

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