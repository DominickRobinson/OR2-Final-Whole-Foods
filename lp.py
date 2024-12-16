import json
import re
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpInteger

# Load dataset
with open("data/all_meals_mapped_to_products.json", "r") as f:
    meals = json.load(f)


# Function to clean nutrient keys and extract values
def preprocess_nutrient_data(meals):
    for meal in meals:
        for ingredient in meal.get("ingredients", []):
            nutrition = ingredient.get("nutrition", {})
            cleaned_nutrition = {}
            for key, value in nutrition.items():
                # Extract numeric value from nutrient string (e.g., "8g")
                match = re.search(r"[\d.]+", value)
                if match:
                    cleaned_nutrition[key.split()[0]] = float(match.group())
            ingredient["cleaned_nutrition"] = cleaned_nutrition
    return meals


meals = preprocess_nutrient_data(meals)
