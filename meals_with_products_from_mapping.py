import json
import inflect  # Library for handling singular/plural conversions

# Initialize inflect engine for singularization
inflect_engine = inflect.engine()


# Normalize ingredient names to lowercase and singular
def normalize_ingredient(ingredient):
    """Normalize ingredient by converting to lowercase and singular form."""
    if not ingredient:
        return None
    words = ingredient.lower().strip().split()
    singular_words = [inflect_engine.singular_noun(word) or word for word in words]
    return " ".join(singular_words)


# Load the input files
with open("data/all_meals_normalized.json", "r") as f:
    all_meals = json.load(f)

with open("data/ingredient_to_product_mapping.json", "r") as f:
    ingredient_to_product_mapping = json.load(f)


# Function to map ingredients to products with normalization
def map_ingredients_to_products(meals, ingredient_mapping):
    updated_meals = []

    for meal in meals:
        updated_meal = meal.copy()
        updated_ingredients = []

        for i in range(1, 21):  # strIngredient1 to strIngredient20
            ingredient_key = f"strIngredient{i}"
            measure_key = f"strMeasure{i}"

            ingredient = meal.get(ingredient_key)
            if ingredient:  # Ensure ingredient is not None
                normalized_ingredient = normalize_ingredient(
                    ingredient
                )  # Normalize ingredient
                # Map ingredient to product name or fallback to the normalized ingredient name
                product_name = ingredient_mapping.get(
                    normalized_ingredient, normalized_ingredient
                )
                updated_ingredients.append(
                    {
                        "product": product_name,
                        "measure": meal.get(measure_key, "").strip(),
                    }
                )

        updated_meal["ingredients"] = updated_ingredients

        # Remove old strIngredient and strMeasure keys
        for i in range(1, 21):
            updated_meal.pop(f"strIngredient{i}", None)
            updated_meal.pop(f"strMeasure{i}", None)

        updated_meals.append(updated_meal)

    return updated_meals


# Process the meals
updated_meals = map_ingredients_to_products(all_meals, ingredient_to_product_mapping)

# Save the updated meals to a new JSON file
output_path = "data/all_meals_mapped_to_products.json"
with open(output_path, "w") as f:
    json.dump(updated_meals, f, indent=4)


# Load the processed products file
with open("data/processed_products.json", "r") as f:
    processed_products = json.load(f)


# Function to enrich ingredients with nutrition and price information
def enrich_ingredients_with_product_info(meals, processed_products):
    enriched_meals = []

    for meal in meals:
        enriched_meal = meal.copy()
        enriched_ingredients = []

        for ingredient in meal["ingredients"]:
            product_name = ingredient["product"]
            product_info = processed_products.get(product_name, {})

            # Add price and nutrition info if available
            enriched_ingredient = ingredient.copy()
            enriched_ingredient["price"] = product_info.get("price")
            enriched_ingredient["nutrition"] = product_info.get("nutrition", {})

            enriched_ingredients.append(enriched_ingredient)

        enriched_meal["ingredients"] = enriched_ingredients
        enriched_meals.append(enriched_meal)

    return enriched_meals


# Enrich the meals with product info
enriched_meals = enrich_ingredients_with_product_info(updated_meals, processed_products)

# Save the enriched meals to a new JSON file
output_path = "data/all_meals_enriched_with_products.json"
with open(output_path, "w") as f:
    json.dump(enriched_meals, f, indent=4)

output_path
