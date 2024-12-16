import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import inflect  # Library for handling singular/plural conversions


# Load the last outputted JSON file
with open("data/processed_products.json", "r") as f:
    products = json.load(f)

# Load the ingredients
with open("data/ingredients.txt", "r") as f:
    ingredients = [line.strip() for line in f.readlines()]


# Cache for normalized texts
normalize_cache = {}
# Handles plurals
inflect_engine = inflect.engine()


# Normalize text function
def normalize_text(text):
    """Normalize text by converting to lowercase, stripping extra spaces, and singularizing words."""
    if text in normalize_cache:
        return normalize_cache[text]  # Return cached result

    words = text.lower().strip().split()
    singularized_words = [inflect_engine.singular_noun(word) or word for word in words]
    normalized = " ".join(singularized_words)
    normalize_cache[text] = normalized  # Cache the result
    return normalized


# Get product names
product_names = list(products.keys())
normalized_product_names = [normalize_text(name) for name in product_names]

# Create a mapping from ingredients to product names
ingredient_to_product_mapping = {}

for ingredient in ingredients:
    normalized_ingredient = normalize_text(ingredient)

    # Use cosine similarity
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(
        [normalized_ingredient] + normalized_product_names
    )
    cosine_sim = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    best_match_index = cosine_sim.argmax()
    best_match_score = cosine_sim[best_match_index] * 100  # Convert to percentage

    # Store the best match
    best_match_product = product_names[best_match_index]
    ingredient_to_product_mapping[ingredient] = best_match_product

# Save the mapping to a JSON file
with open("data/ingredient_to_product_mapping.json", "w") as f:
    json.dump(ingredient_to_product_mapping, f, indent=4)

print(
    "Ingredient to product mapping completed. Saved to 'data/ingredient_to_product_mapping.json'."
)
