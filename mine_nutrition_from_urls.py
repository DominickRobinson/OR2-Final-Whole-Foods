import requests
import json
from bs4 import BeautifulSoup
import time
import os


def get_nutrition_and_badges(url):
    start_time = time.time()
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract nutrition facts
        nutrition_facts = {}
        nutrition_section = soup.find("section", class_="w-pie--nutrition-facts")
        if nutrition_section:
            # Extract servings, calories, and other nutrients
            servings = nutrition_section.find("div", class_="servings")
            if servings:
                nutrition_facts["Servings per container"] = servings.text.strip()

            calories = nutrition_section.find(
                "div", {"data-testid": "nutri-facts-calories"}
            )
            if calories:
                nutrition_facts["Calories"] = calories.find(
                    "div", class_="amount"
                ).text.strip()

            # Extract sugar and fiber specifically
            sugar_row = nutrition_section.find(
                "div", {"data-testid": "nutri-facts-primary-indented-row-sugar"}
            )
            if sugar_row:
                sugar_value = sugar_row.find(
                    "div", class_="nutrition-column"
                ).text.strip()
                nutrition_facts["Sugars"] = sugar_value

            fiber_row = nutrition_section.find(
                "div", {"data-testid": "nutri-facts-primary-indented-row-fiber"}
            )
            if fiber_row:
                fiber_value = fiber_row.find(
                    "div", class_="nutrition-column"
                ).text.strip()
                nutrition_facts["Fiber"] = fiber_value

            # Extract all rows of general nutrition info
            rows = nutrition_section.find_all("div", class_="nutrition-row")
            for row in rows:
                nutrient_name = row.find("div", class_="nutrition-column").text.strip()
                nutrient_value = row.find("div", class_="text-right")
                if nutrient_value:
                    nutrition_facts[nutrient_name] = nutrient_value.text.strip()

        # Extract dietary badges
        badges = []
        badge_elements = soup.find_all("button", {"data-testid": "w-diet-badge"})
        for badge in badge_elements:
            badge_label = badge.find("span", class_="w-diet-badge__label")
            if badge_label:
                badges.append(badge_label.text.strip())

        print("Time to mine: ", time.time() - start_time)
        return {"nutrition": nutrition_facts, "badges": badges}

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from {url}: {e}")
        print(" Time to mine: ", time.time() - start_time)
        return {"nutrition": {}, "badges": []}


def process_products_in_batches(input_file, output_dir, batch_size=50):
    try:
        with open(input_file, "r") as file:
            products = json.load(file)

        enriched_products = {}
        batch_counter = 0
        file_counter = 1

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        for idx, (name, details) in enumerate(products.items(), start=1):
            nutrition_and_badges = get_nutrition_and_badges(details["link"])
            enriched_products[name] = {
                "price": details["price"],
                "link": details["link"],
                "nutrition": nutrition_and_badges["nutrition"],
                "badges": nutrition_and_badges["badges"],
            }
            batch_counter += 1

            # Save progress every batch_size items
            if batch_counter == batch_size or idx == len(products):
                output_file = os.path.join(output_dir, f"batch_{file_counter}.json")
                print("Output file: ", output_file)
                with open(output_file, "w") as file:
                    json.dump(enriched_products, file, indent=4)
                print(
                    f"Saved batch {file_counter} with {batch_counter} items to {output_file}."
                )
                enriched_products = {}
                batch_counter = 0
                file_counter += 1

        print("All batches processed.")

    except IOError as e:
        print(f"Failed to process products: {e}")


def combine_batches(output_dir, combined_output_file):
    try:
        combined_data = {}

        for batch_file in sorted(os.listdir(output_dir)):
            if batch_file.endswith(".json"):
                batch_path = os.path.join(output_dir, batch_file)
                with open(batch_path, "r") as file:
                    batch_data = json.load(file)
                    combined_data.update(batch_data)

        # Save combined data
        with open(combined_output_file, "w") as file:
            json.dump(combined_data, file, indent=4)

        print(f"Combined data saved to {combined_output_file}.")

    except IOError as e:
        print(f"Failed to combine batches: {e}")


print("Starting to mine nutrition from links...")


print("Starting to mine nutrition from links...")

# Input and output configuration
input_filename = "data/filtered_products_prices_links.json"
output_directory = "data/batches"
combined_output_filename = "data/products_with_nutrition_and_badges_combined.json"

# Run the script
process_products_in_batches(input_filename, output_directory)

# Combine all batches into one JSON if processing completes
combine_batches(output_directory, combined_output_filename)
