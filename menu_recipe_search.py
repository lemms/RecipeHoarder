from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button

import recipes_util

class MenuRecipeSearchScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    name_matches = []
    id_matches = []

    recipe_name_input = None
    list_view = None

    async def clear_menu_recipe_search(self) -> None:
        self.name_matches = []
        self.id_matches = []
        self.recipe_name_input.value = ""
        await self.list_view.clear()

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for name_match_idx, name_match in enumerate(self.name_matches):
            recipe_time = None
            recipe_servings = None
            recipe_stars = None

            for recipe in recipes_util.recipes:
                if int(recipe["id"]) == int(self.id_matches[name_match_idx]):
                    recipe_time = recipe["time"]
                    recipe_servings = recipe["servings"]
                    recipe_stars = recipe["stars"]
                    break

            self.list_view.append(ListItem(Label(f'{name_match} ({recipe_servings} servings) ({recipe_time}) {recipe_stars} stars'), id=f'search_recipe_{name_match_idx}'))

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Recipe Search", id="title")
        self.recipe_name_input = Input(placeholder="Recipe Name", id="recipe_name", type="text")
        yield self.recipe_name_input
        yield Button("Search", id="search_recipe")
        yield Label("Select Recipe")
        self.list_view = ListView()
        yield self.list_view
        yield Button("Add Recipe", id="add_recipe")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search_recipe":
            self.name_matches = []
            self.id_matches = []

            self.name_matches, self.id_matches = recipes_util.search_recipe(self.query_one("#recipe_name").value)

            await self.refresh_list_view()
        elif event.button.id == "add_recipe":
            if self.list_view.index is None:
                await self.clear_menu_recipe_search()

                self.dismiss(None)
            else:
                recipe_id = self.id_matches[self.list_view.index]

                await self.clear_menu_recipe_search()

                self.dismiss(recipe_id)