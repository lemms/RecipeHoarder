from textual.widgets import Label, ListView, ListItem

ingredients = []

def find_max_ingredient_id() -> int:
    max_id = 0

    for ingredient in ingredients:
        if int(ingredient["id"]) > max_id:
            max_id = int(ingredient["id"])

    return max_id

units_of_measure = ["lbs",
                    "oz",
                    "fl_oz",
                    "tsp",
                    "tbsp",
                    "cups",
                    "pieces",
                    "cans",
                    "bags",
                    "packages",
                    "bottles",
                    "boxes",
                    "jars",
                    "cartons",
                    "containers",
                    "cloves",
                    "loaves",
                    "slices",
                    "ribs",
                    "g",
                    "kg",
                    "ml",
                    "l",
                    "pints",
                    "quarts",
                    "gallons",
                    "heads",
                    "bunches",
                    "bulbs"]

def create_unit_of_measure_list_view() -> ListView:
    list_items = []
    for unit_of_measure in units_of_measure:
        list_items.append(ListItem(Label(unit_of_measure.replace("_", " ")), id=f"unit_{unit_of_measure}"))

    return ListView(*list_items, id="unit_of_measure_list")

def unit_of_measure_list_index(unit_of_measure: str) -> int:
    return units_of_measure.index(unit_of_measure)

categories = ["Produce",
              "Dairy",
              "Meat",
              "Seafood",
              "Bakery",
              "Frozen",
              "Pantry",
              "Other"]

categories_lower = [category.lower() for category in categories]

def create_category_list_view() -> ListView:
    list_items = []
    for category in categories:
        list_items.append(ListItem(Label(category), id=f"category_{category.lower()}"))

    return ListView(*list_items, id="category_list")

def category_list_index(category: str) -> int:
    return categories_lower.index(category.lower())