import json
import re

# Load the JSON data
with open("data/products_with_nutrition_and_badges_combined.json", "r") as f:
    products = json.load(f)


def convert_to_dv(value, dv):
    try:
        # Extract numeric value and calculate percent DV
        num_value = float(re.search(r"[\d.]+", value).group())
        return f"{round((num_value / dv) * 100)}%"
    except (AttributeError, ValueError):
        return "0%"


# Process each product
processed_products = {}
for product_name, details in products.items():
    nutrition = details.get("nutrition", {})

    # Handle sugars and dietary fiber
    sugars = nutrition.get("Sugars", "Sugars 0g")
    fiber = nutrition.get("Fiber", "Dietary Fiber 0g")
    nutrition[f"Sugars {sugars.split(' ')[-1]}"] = convert_to_dv(
        sugars, 50
    )  # Sugars DV: 50g
    nutrition[f"Dietary Fiber {fiber.split(' ')[-1]}"] = convert_to_dv(
        fiber, 28
    )  # Fiber DV: 28g

    # Remove original 'Sugars' and 'Fiber' fields
    if "Sugars" in nutrition:
        del nutrition["Sugars"]
    if "Fiber" in nutrition:
        del nutrition["Fiber"]

    # Remove products without "Servings per container"
    if "Serving size" in nutrition and "Servings per container" not in nutrition:
        continue

    # Convert serving size to oz or fl oz
    if "Serving size" in nutrition:
        serving_size = nutrition["Serving size"]
        match = re.search(r"(\d+(\.\d+)?)\s*(g|ml)", serving_size)
        if match:
            value, unit = float(match.group(1)), match.group(3)
            if unit == "g":
                value = value * 0.035274  # Convert grams to ounces
                unit = "oz"
            elif unit == "ml":
                value = value * 0.033814  # Convert milliliters to fluid ounces
                unit = "fl oz"
            nutrition["Serving size"] = f"{round(value, 2)} {unit}"

    # Update the product name
    updated_name = re.sub(r",\s*\d+\s*(ml|g|oz|fl oz)$", "", product_name)

    # Save the updated product details
    processed_products[updated_name] = details

# Save the processed data
with open("data/processed_products.json", "w") as f:
    json.dump(processed_products, f, indent=4)

print("Processing complete. Updated data saved.")
