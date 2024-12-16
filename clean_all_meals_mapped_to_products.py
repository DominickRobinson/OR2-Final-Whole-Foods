import json
import re

# Load the meals JSON file
with open("data/all_meals_mapped_to_products.json", "r") as f:
    meals = json.load(f)

# Standard %DV values for 1 oz of various nutrients (approximate, based on FDA guidelines)
dv_per_oz = {
    "Total Fat": 78 / 16,  # grams of fat for 100% DV, divided by 16 oz in a pound
    "Saturated Fat": 20 / 16,
    "Cholesterol": 300 / 16,
    "Sodium": 2300 / 16,
    "Total Carbohydrate": 275 / 16,
    "Dietary Fiber": 28 / 16,
    "Sugars": None,  # No %DV for sugars
    "Protein": 50 / 16,
    "Calcium": 1300 / 16,
    "Iron": 18 / 16,
    "Potassium": 4700 / 16,
    "Vitamin D": 20 / 16,  # mcg
    # Add more nutrients as needed
}


# Function to calculate %DV if missing
def calculate_dv(amount, nutrient, unit):
    if nutrient not in dv_per_oz or dv_per_oz[nutrient] is None:
        return None  # Cannot calculate DV
    if unit.lower() in ["oz", "fl oz"]:  # Check if unit is in ounces
        dv_value = (float(amount) / dv_per_oz[nutrient]) * 100
        return f"{dv_value:.1f}%"  # Return formatted %DV
    return None  # Cannot calculate for other units


# Update the meals with calculated %DV
for meal in meals:
    for ingredient in meal.get("ingredients", []):
        nutrition = ingredient.get("nutrition", {})
        for nutrient, value in nutrition.items():
            if value in [None, "", "null", "% Daily Value *"]:
                # Extract the amount and unit from the nutrient key
                match = re.match(r"(\d+\.?\d*)\s*(\w+)", nutrient, re.IGNORECASE)
                if match:
                    amount, unit = match.groups()
                    nutrient_name = nutrient.split()[0]  # Extract the nutrient name
                    calculated_dv = calculate_dv(amount, nutrient_name, unit)
                    if calculated_dv:
                        nutrition[nutrient] = calculated_dv

# Save the updated meals to a new JSON file
output_path = "data/all_meals_mapped_to_products_updated.json"
with open(output_path, "w") as f:
    json.dump(meals, f, indent=4)

print(f"Updated meals saved to {output_path}")
