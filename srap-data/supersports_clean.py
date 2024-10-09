import re
import json
from urllib.parse import urljoin

# Path to the original scraped data file
scrap_file = 'supersports.json'
cleaned_file = 'supersports_clean.json'

# Base URL for the product pages (adjust as needed)
base_url = "https://supersports.com.vn"

# Function to normalize price (remove currency symbols and commas)
def normalize_price(price):
    price = re.sub(r'[^\d]', '', str(price))  # Remove non-digit characters
    return int(price) if price else None  # Return None if no price

# Function to ensure full URL
def ensure_full_url(url):
    if not url.startswith('http'):
        return urljoin(base_url, url)
    return url

# Function to process and format product features
def process_product_features(features):
    # Ensure features are not empty
    return features if features else "No features listed"

# Step 1: Read data from the original scraped file
with open(scrap_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Step 2: Clean and normalize the data
for product in data:
    # Normalize prices
    if 'sale_price' in product:
        product['sale_price'] = normalize_price(product['sale_price'])
    if 'price' in product:
        product['price'] = normalize_price(product['price'])
    
    # Ensure full product URL
    if 'product_url' in product:
        product['product_url'] = ensure_full_url(product['product_url'])
    
    # Ensure product features are present
    if 'product_features' in product:
        product['product_features'] = process_product_features(product['product_features'])
    else:
        product['product_features'] = "No features listed"  # Default value if not provided

# Step 3: Write the cleaned data to a new file
with open(cleaned_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Cleaned data has been written to {cleaned_file} successfully!")
