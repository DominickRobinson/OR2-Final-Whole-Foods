import json

# Load the meals JSON file
with open("data/all_meals_mapped_to_products_updated.json", "r") as f:
    meals = json.load(f)


# Function to calculate the total amount per unit for each ingredient
def calculate_total_per_unit(nutrition):
    try:
        servings_per_container = float(nutrition["Servings per container"].split()[0])
        serving_size = nutrition["Serving size"].split()
        if len(serving_size) == 2 and serving_size[1].lower() in ["oz", "fl oz"]:
            serving_size_amount = float(serving_size[0])
            return servings_per_container * serving_size_amount
    except (KeyError, ValueError, IndexError):
        return None
    return None


# Function to calculate total ingredient needed for each meal
def calculate_ingredient_needs(meals):
    for meal in meals:
        for ingredient in meal.get("ingredients", []):
            measure = ingredient.get("measure", "").strip()
            nutrition = ingredient.get("nutrition", {})
            total_per_unit = calculate_total_per_unit(nutrition)

            if not total_per_unit:
                ingredient["total_needed"] = "Unknown (missing or invalid data)"
                continue

            try:
                if "oz" in measure.lower():
                    amount = float(measure.split()[0])
                    ingredient["total_needed"] = amount / total_per_unit
                elif "serving" in measure.lower():
                    servings_per_container = float(
                        nutrition["Servings per container"].split()[0]
                    )
                    amount = float(measure.split()[0])
                    ingredient["total_needed"] = amount / servings_per_container
                else:
                    ingredient["total_needed"] = "Unknown (unsupported unit)"
            except (ValueError, KeyError, IndexError):
                ingredient["total_needed"] = (
                    "Unknown (invalid measure or nutrition data)"
                )
    return meals


# Process meals to calculate ingredient needs
meals_with_needs = calculate_ingredient_needs(meals)

# Save the updated meals with ingredient needs to a new JSON file
output_path = "data/all_meals_with_ingredient_needs.json"
with open(output_path, "w") as f:
    json.dump(meals_with_needs, f, indent=4)

print(f"Updated meals with ingredient needs saved to {output_path}")
