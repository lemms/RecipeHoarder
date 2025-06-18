import pyperclip

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Button

import edit_recipe
import ingredients_util
import recipes_util

class ViewRecipeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    view_recipe_id = None
    recipe_name_label = None
    recipe_time_label = None
    recipe_servings_label = None
    recipe_ingredients_list_view = None
    recipe_instructions_label = None
    recipe_tags_label = None
    recipe_stars_label = None
    recipe_source_label = None

    def __init__(self, view_recipe_id: int) -> None:
        self.view_recipe_id = view_recipe_id
        super().__init__()

    async def refresh_recipe_form(self) -> None:
        recipe_name = None
        recipe_instructions = None
        recipe_time = None
        recipe_servings = None
        recipe_ingredients = None
        recipe_amounts = None
        recipe_optional_flags = None
        recipe_tags = None
        recipe_stars = None
        recipe_source = None
        for recipe in recipes_util.recipes:
            if int(recipe["id"]) == int(self.view_recipe_id):
                recipe_name = recipe["name"]
                recipe_instructions = recipe["instructions"]
                recipe_time = recipe["time"]
                recipe_servings = recipe["servings"]
                recipe_ingredients = recipe["ingredients"]
                recipe_amounts = recipe["amounts"]
                recipe_optional_flags = recipe["optional_flags"]
                recipe_tags = recipe["tags"]
                recipe_stars = recipe["stars"]
                recipe_source = recipe["source"]
                break

        self.recipe_name_label.update(f"Recipe Name: {recipe_name}")
        self.recipe_time_label.update(f"Time: {recipe_time}")
        self.recipe_servings_label.update(f"Servings: {recipe_servings}")

        await self.recipe_ingredients_list_view.clear()
        recipe_ingredients_list_items = []
        for recipe_ingredient_idx, recipe_ingredient in enumerate(recipe_ingredients):
            ingredient_name = None
            ingredient_unit_of_measure = None
            ingredient_amount = float(recipe_amounts[recipe_ingredient_idx])

            for ingredient in ingredients_util.ingredients:
                if int(ingredient["id"]) == int(recipe_ingredient):
                    ingredient_name = ingredient["name"]
                    ingredient_unit_of_measure = ingredient["unit_of_measure"].replace("_", " ")
                    break

            if recipe_optional_flags[recipe_ingredient_idx] == True:
                self.recipe_ingredients_list_view.append(ListItem(Label(f"{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure}) (Optional)"), id=f'ingredient_{recipe_ingredient_idx}'))
            else:
                self.recipe_ingredients_list_view.append(ListItem(Label(f"{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure})"), id=f'ingredient_{recipe_ingredient_idx}'))

        self.recipe_instructions_label.update(recipe_instructions)
        self.recipe_tags_label.update(", ".join(recipe_tags))
        self.recipe_stars_label.update(f'Star Rating: {recipe_stars}')
        self.recipe_source_label.update(f'Source: {recipe_source}')

    def compose(self) -> ComposeResult:
        recipe_name = None
        recipe_instructions = None
        recipe_time = None
        recipe_servings = None
        recipe_ingredients = None
        recipe_amounts = None
        recipe_optional_flags = None
        recipe_tags = None
        recipe_stars = None
        recipe_source = None
        for recipe in recipes_util.recipes:
            if int(recipe["id"]) == int(self.view_recipe_id):
                recipe_name = recipe["name"]
                recipe_instructions = recipe["instructions"]
                recipe_time = recipe["time"]
                recipe_servings = recipe["servings"]
                recipe_ingredients = recipe["ingredients"]
                recipe_amounts = recipe["amounts"]
                recipe_optional_flags = recipe["optional_flags"]
                recipe_tags = recipe["tags"]
                recipe_stars = recipe["stars"]
                recipe_source = recipe["source"]
                break

        recipe_ingredients_list_items = []

        for recipe_ingredient_idx, recipe_ingredient in enumerate(recipe_ingredients):
            ingredient_name = None
            ingredient_unit_of_measure = None
            ingredient_amount = float(recipe_amounts[recipe_ingredient_idx])

            for ingredient in ingredients_util.ingredients:
                if int(ingredient["id"]) == int(recipe_ingredient):
                    ingredient_name = ingredient["name"]
                    ingredient_unit_of_measure = ingredient["unit_of_measure"].replace("_", " ")
                    break

            if recipe_optional_flags[recipe_ingredient_idx] == True:
                recipe_ingredients_list_items.append(ListItem(Label(f"{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure}) (Optional)"), id=f'ingredient_{recipe_ingredient_idx}'))
            else:
                recipe_ingredients_list_items.append(ListItem(Label(f"{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure})"), id=f'ingredient_{recipe_ingredient_idx}'))

        yield Header()
        yield Static("View Recipe", id="title")
        self.recipe_name_label = Label(f"Recipe Name: {recipe_name}")
        yield self.recipe_name_label
        self.recipe_time_label = Label(f"Time: {recipe_time}")
        yield self.recipe_time_label
        self.recipe_servings_label = Label(f"Servings: {recipe_servings}")
        yield self.recipe_servings_label
        yield Label("Ingredients")
        self.recipe_ingredients_list_view = ListView(*recipe_ingredients_list_items)
        yield self.recipe_ingredients_list_view
        yield Label("Instructions")
        self.recipe_instructions_label = Label(recipe_instructions)
        yield self.recipe_instructions_label
        yield Label("Tags")
        self.recipe_tags_label = Label(", ".join(recipe_tags))
        yield self.recipe_tags_label
        self.recipe_stars_label = Label(f'Star Rating: {recipe_stars}')
        yield self.recipe_stars_label
        self.recipe_source_label = Label(f'Source: {recipe_source}')
        yield self.recipe_source_label
        yield Button("Copy to Clipboard", id="copy_to_clipboard")
        yield Button("Edit Recipe", id="edit_recipe")
        yield Button("Delete Recipe", id="delete_recipe")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete_recipe":
            for recipe_idx, recipe in enumerate(recipes_util.recipes):
                if int(recipe["id"]) == int(self.view_recipe_id):
                    recipe["deleted"] = True

            self.view_recipe_id = None

            self.dismiss(None)
        elif event.button.id == "edit_recipe":
            recipe_screen = self

            async def edit_recipe_callback(recipe_id) -> None:
                await recipe_screen.refresh_recipe_form()

            self.app.push_screen(edit_recipe.EditRecipeScreen(self.view_recipe_id), edit_recipe_callback)
        elif event.button.id == "copy_to_clipboard":
            recipe_name = None
            recipe_instructions = None
            recipe_time = None
            recipe_servings = None
            recipe_ingredients = None
            recipe_amounts = None
            recipe_optional_flags = None
            recipe_tags = None
            recipe_stars = None
            recipe_source = None
            for recipe in recipes_util.recipes:
                if int(recipe["id"]) == int(self.view_recipe_id):
                    recipe_name = recipe["name"]
                    recipe_instructions = recipe["instructions"]
                    recipe_time = recipe["time"]
                    recipe_servings = recipe["servings"]
                    recipe_ingredients = recipe["ingredients"]
                    recipe_amounts = recipe["amounts"]
                    recipe_optional_flags = recipe["optional_flags"]
                    recipe_tags = recipe["tags"]
                    recipe_stars = recipe["stars"]
                    recipe_source = recipe["source"]
                    break

            recipe_text = f"Recipe: {recipe_name}\n"
            recipe_text += "\n"
            recipe_text += f"Time: {recipe_time}\n"
            recipe_text += f"Servings: {recipe_servings}\n"
            recipe_text += "\n"
            recipe_text += "Ingredients:\n"
            recipe_text += "-----------\n"

            recipe_ingredients_list_items = []

            for recipe_ingredient_idx, recipe_ingredient in enumerate(recipe_ingredients):
                ingredient_name = None
                ingredient_unit_of_measure = None
                ingredient_amount = float(recipe_amounts[recipe_ingredient_idx])

                for ingredient in ingredients_util.ingredients:
                    if int(ingredient["id"]) == int(recipe_ingredient):
                        ingredient_name = ingredient["name"]
                        ingredient_unit_of_measure = ingredient["unit_of_measure"].replace("_", " ")
                        break

                if recipe_optional_flags[recipe_ingredient_idx] == True:
                    recipe_text += f"{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure}) (Optional)\n"
                else:
                    recipe_text += f"{ingredient_name} ({ingredient_amount} {ingredient_unit_of_measure})\n"

            recipe_text += "\n"
            recipe_text += "Instructions:\n"
            recipe_text += "------------\n"
            recipe_text += f"{recipe_instructions}\n"
            recipe_text += "\n"
            recipe_text += "Tags:\n"
            recipe_text += "----\n"
            recipe_text += ", ".join(recipe_tags)
            recipe_text += "\n\n"
            recipe_text += f"Star Rating: {recipe_stars}\n"
            recipe_text += f"Source: {recipe_source}\n"

            pyperclip.copy(recipe_text)