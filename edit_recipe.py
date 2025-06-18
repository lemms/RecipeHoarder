from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input, Button, TextArea

import ingredients_util
import recipes_util
import util

class EditRecipeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    edit_recipe_id = None

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

    def __init__(self, edit_recipe_id: int) -> None:
        self.edit_recipe_id = edit_recipe_id
        super().__init__()

    async def clear_recipe(self) -> None:
        self.edit_recipe_id = None
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
        recipe_name = None
        recipe_servings = None
        recipe_time = None
        recipe_ingredients = None
        recipe_amounts = None
        recipe_optional_flags = None
        recipe_instructions = None
        recipe_stars = None
        recipe_tags = None
        recipe_source = None

        for recipe in recipes_util.recipes:
            if int(recipe["id"]) == int(self.edit_recipe_id):
                recipe_name = recipe["name"]
                recipe_servings = recipe["servings"]
                recipe_time = recipe["time"]
                recipe_ingredients = recipe["ingredients"]
                recipe_amounts = recipe["amounts"]
                recipe_optional_flags = recipe["optional_flags"]
                recipe_instructions = recipe["instructions"]
                recipe_stars = recipe["stars"]
                recipe_tags = recipe["tags"]
                recipe_source = recipe["source"]
                break

        self.recipe_ingredients = recipe_ingredients
        self.recipe_amounts = recipe_amounts
        self.recipe_optional_flags = recipe_optional_flags

        ingredient_list_items = []
        for ingredient_idx, recipe_ingredient in enumerate(self.recipe_ingredients):
            ingredient_name = None
            ingredient_unit_of_measure = None

            for ingredient in ingredients_util.ingredients:
                if int(ingredient["id"]) == int(recipe_ingredient):
                    ingredient_name = ingredient["name"]
                    ingredient_unit_of_measure = ingredient["unit_of_measure"]

            ingredient_amount = float(self.recipe_amounts[ingredient_idx])

            if self.recipe_optional_flags[ingredient_idx] == True:
                ingredient_list_items.append(ListItem(Label(f'{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure}) (Optional)'), id=f'ingredient_{ingredient_idx}'))
            else:
                ingredient_list_items.append(ListItem(Label(f'{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure})'), id=f'ingredient_{ingredient_idx}'))

        yield Header()
        yield Static("Edit Recipe", id="title")
        self.recipe_name_input = Input(placeholder="Recipe Name", id="recipe_name", type="text", value=recipe_name)
        yield self.recipe_name_input
        yield Label("Servings")
        self.recipe_servings_input = Input(placeholder="Servings", id="recipe_servings", type="number", value=recipe_servings)
        yield self.recipe_servings_input
        yield Label("Time")
        self.recipe_time_input = Input(placeholder="Time", id="recipe_time", type="text", value=recipe_time)
        yield self.recipe_time_input
        yield Button("Add Ingredient", id="add_ingredient")
        self.list_view = ListView(*ingredient_list_items)
        yield self.list_view
        yield Label("Instructions")
        self.recipe_instructions_text_area = TextArea(id="recipe_instructions", text=recipe_instructions)
        yield self.recipe_instructions_text_area
        yield Label("Star Rating")
        self.recipe_stars_input = Input(placeholder="Star Rating", id="recipe_stars", type="number", value=recipe_stars)
        yield self.recipe_stars_input
        yield Label("Tags")
        self.recipe_tags_text_area = TextArea(id="recipe_tags", text="\n".join(recipe_tags))
        yield self.recipe_tags_text_area
        yield Label("Source (Book/Website)")
        self.recipe_source_input = Input(placeholder="Source (Book/Website)", id="recipe_source", type="text", value=recipe_source)
        yield self.recipe_source_input
        yield Button("Submit", id="add_recipe")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_ingredient":
            async def edit_recipe_ingredient_callback(ingredient_tuple) -> None:
                if ingredient_tuple is not None:
                    ingredient_id, ingredient_amount, ingredient_optional_flag = ingredient_tuple

                    if ingredient_id is not None:
                        self.recipe_ingredients.append(ingredient_id)
                        self.recipe_amounts.append(float(ingredient_amount))
                        self.recipe_optional_flags.append(ingredient_optional_flag)

                    if len(self.recipe_ingredients) > 0:
                        await self.refresh_list_view()

            self.app.push_screen("recipe_ingredient_search", edit_recipe_ingredient_callback)
        elif event.button.id == "add_recipe":
            recipe_name = self.query_one("#recipe_name").value
            if recipe_name is None or recipe_name == "":
                self.app.pop_screen()
            else:
                if self.recipe_tags_text_area.text is not None and self.recipe_tags_text_area.text != "":
                    recipe_tags = self.recipe_tags_text_area.text.split("\n")
                else:
                    recipe_tags = []

                for recipe_idx, recipe in enumerate(recipes_util.recipes):
                    if int(recipe["id"]) == int(self.edit_recipe_id):
                        recipe["name"] = recipe_name
                        recipe["servings"] = self.recipe_servings_input.value
                        recipe["time"] = self.recipe_time_input.value
                        recipe["ingredients"] = self.recipe_ingredients
                        recipe["amounts"] = self.recipe_amounts
                        recipe["deleted"] = False
                        recipe["instructions"] = self.recipe_instructions_text_area.text
                        recipe["stars"] = self.recipe_stars_input.value
                        recipe["tags"] = recipe_tags
                        recipe["source"] = self.recipe_source_input.value
                        recipe["optional_flags"] = self.recipe_optional_flags

                util.save_data()

                await self.clear_recipe()

                self.dismiss(self.edit_recipe_id)

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        del self.recipe_ingredients[int(event.item.id[11:])]
        del self.recipe_amounts[int(event.item.id[11:])]
        del self.recipe_optional_flags[int(event.item.id[11:])]

        await self.refresh_list_view()