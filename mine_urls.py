import requests
import json

# Base URL
base_url = "https://www.wholefoodsmarket.com/api/products/category/all-products"
store_id = "10694"


# Create a function to fetch and save JSON data into a specific format
def fetch_and_save_filtered_json(limit=60, max_offset=120000):
    combined_data = {}  # Initialize an empty dictionary to store filtered results

    for i in range(0, max_offset + 1, limit):
        url = f"{base_url}?leafCategory=all-products&store={store_id}&limit={limit}&offset={i}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors
            data = response.json()

            # Extract the relevant data
            results = data.get("results", [])
            for product in results:
                name = product.get("name")
                price = product.get("regularPrice")
                slug = product.get("slug")
                if name and price and slug:
                    link = f"https://www.wholefoodsmarket.com/product/{slug}"
                    combined_data[name] = {"price": price, "link": link}

            print(f"Data for offset {i} fetched successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data for offset {i}: {e}")

    # Save the combined filtered data to a JSON file
    filename = "filtered_products_prices_links.json"
    try:
        with open(filename, "w") as file:
            json.dump(combined_data, file, indent=4)
        print(f"Filtered data saved to {filename}.")
    except IOError as e:
        print(f"Failed to save filtered data: {e}")


# Run the function
fetch_and_save_filtered_json()
