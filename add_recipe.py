from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button, TextArea

import ingredients_util
import recipes_util
import util

class AddRecipeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    recipe_ingredients = []
    recipe_amounts = []
    recipe_optional_flags = []
    recipe_name_input = None
    recipe_servings_input = None
    recipe_time_input = None
    recipe_stars_input = None
    recipe_instructions_text_area = None
    list_view = None
    recipe_tags_text_area = None
    recipe_source_input = None

    async def clear_recipe(self) -> None:
        self.recipe_ingredients = []
        self.recipe_amounts = []
        self.recipe_optional_flags = []
        self.recipe_name_input.value = ""
        await self.list_view.clear()
        self.recipe_servings_input.value = "1"
        self.recipe_time_input.value = ""
        self.recipe_stars_input.value = "5"
        self.recipe_instructions_text_area.text = ""
        self.recipe_tags_text_area.text = ""
        self.recipe_source_input.value = ""

    async def refresh_list_view(self) -> None:
        await self.list_view.clear()

        for ingredient_idx, recipe_ingredient in enumerate(self.recipe_ingredients):
            ingredient_name = None
            ingredient_unit_of_measure = None

            for ingredient in ingredients_util.ingredients:
                if int(ingredient["id"]) == int(recipe_ingredient):
                    ingredient_name = ingredient["name"]
                    ingredient_unit_of_measure = ingredient["unit_of_measure"]

            ingredient_amount = float(self.recipe_amounts[ingredient_idx])

            if self.recipe_optional_flags[ingredient_idx] == True:
                self.list_view.append(ListItem(Label(f'{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure}) (Optional)'), id=f'ingredient_{ingredient_idx}'))
            else:
                self.list_view.append(ListItem(Label(f'{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure})'), id=f'ingredient_{ingredient_idx}'))

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Add Recipe", id="title")
        self.recipe_name_input = Input(placeholder="Recipe Name", id="recipe_name", type="text")
        yield self.recipe_name_input
        yield Label("Servings")
        self.recipe_servings_input = Input(placeholder="Servings", id="recipe_servings", type="number", value="1")
        yield self.recipe_servings_input
        yield Label("Time")
        self.recipe_time_input = Input(placeholder="Time", id="recipe_time", type="text")
        yield self.recipe_time_input
        yield Button("Add Ingredient", id="add_ingredient")
        self.list_view = ListView()
        yield self.list_view
        yield Label("Instructions")
        self.recipe_instructions_text_area = TextArea(id="recipe_instructions")
        yield self.recipe_instructions_text_area
        yield Label("Star Rating")
        self.recipe_stars_input = Input(placeholder="Star Rating", id="recipe_stars", type="number", value="5")
        yield self.recipe_stars_input
        yield Label("Tags")
        self.recipe_tags_text_area = TextArea(id="recipe_tags")
        yield self.recipe_tags_text_area
        yield Label("Source (Book/Website)")
        self.recipe_source_input = Input(placeholder="Source (Book/Website)", id="recipe_source", type="text")
        yield self.recipe_source_input
        yield Button("Submit", id="add_recipe")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_ingredient":
            async def add_recipe_ingredient_callback(ingredient_tuple) -> None:
                if ingredient_tuple is not None:
                    ingredient_id, ingredient_amount, ingredient_optional_flag = ingredient_tuple

                    if ingredient_id is not None:
                        self.recipe_ingredients.append(ingredient_id)
                        self.recipe_amounts.append(float(ingredient_amount))
                        self.recipe_optional_flags.append(ingredient_optional_flag)

                    if len(self.recipe_ingredients) > 0:
                        await self.refresh_list_view()

            self.app.push_screen("recipe_ingredient_search", add_recipe_ingredient_callback)
        elif event.button.id == "add_recipe":
            recipe_name = self.query_one("#recipe_name").value
            if recipe_name is None or recipe_name == "":
                self.app.pop_screen()
            else:
                max_id = recipes_util.find_max_recipe_id()
                if self.recipe_tags_text_area.text is not None and self.recipe_tags_text_area.text != "":
                    recipe_tags = self.recipe_tags_text_area.text.split("\n")
                else:
                    recipe_tags = []

                recipe = {"id": max_id + 1,
                          "name": recipe_name,
                          "servings": self.recipe_servings_input.value,
                          "time": self.recipe_time_input.value,
                          "ingredients": self.recipe_ingredients,
                          "amounts": self.recipe_amounts,
                          "deleted": False,
                          "instructions": self.recipe_instructions_text_area.text,
                          "stars": self.recipe_stars_input.value,
                          "tags": recipe_tags,
                          "source": self.recipe_source_input.value,
                          "optional_flags": self.recipe_optional_flags}

                recipes_util.recipes.append(recipe)

                util.save_data()

                await self.clear_recipe()
                self.app.pop_screen()

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        del self.recipe_ingredients[int(event.item.id[11:])]
        del self.recipe_amounts[int(event.item.id[11:])]
        del self.recipe_optional_flags[int(event.item.id[11:])]

        await self.refresh_list_view()