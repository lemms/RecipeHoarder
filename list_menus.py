from textual import on
from textual.app import ComposeResult
from textual.events import ScreenResume
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem

import menus_util
import view_menu

class ListMenusScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    list_view = None
    menu_data = []

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        self.menu_data = []

        for menu_idx, menu in enumerate(menus_util.menus):
            if not menu["deleted"]:
                self.menu_data.append({"index": menu_idx,
                                       "name": menu["name"]})

        self.menu_data.sort(key=lambda x: x["name"])

        list_items = []
        for menu_datum_idx, menu_datum in enumerate(self.menu_data):
            self.list_view.append(ListItem(Label(f'{menu_datum["name"]}'), id=f'menu_{menu_datum_idx}'))

    def compose(self) -> ComposeResult:
        self.menu_data = []

        for menu_idx, menu in enumerate(menus_util.menus):
            if not menu["deleted"]:
                self.menu_data.append({"index": menu_idx,
                                       "name": menu["name"]})

        self.menu_data.sort(key=lambda x: x["name"])

        list_items = []
        for menu_datum_idx, menu_datum in enumerate(self.menu_data):
            list_items.append(ListItem(Label(f'{menu_datum["name"]}'), id=f'menu_{menu_datum_idx}'))

        yield Header()
        yield Static("List Menus", id="title")
        self.list_view = ListView(*list_items)
        yield self.list_view
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        menu_data_idx = int(event.item.id[5:])
        menu_idx = self.menu_data[menu_data_idx]["index"]
        menu_id = menus_util.menus[menu_idx]["id"]

        self.app.push_screen(view_menu.ViewMenuScreen(menu_id))

    @on(ScreenResume)
    async def handle_list_menus_screen_resumed(self) -> None:
        await self.refresh_list_view()