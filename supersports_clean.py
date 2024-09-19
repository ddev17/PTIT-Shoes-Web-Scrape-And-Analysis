import re
import json
from urllib.parse import urljoin

# Path to the original scraped data file
scrap_file = 'supersports.json'  
cleaned_file = 'supersports_clean.json'  

# Base URL for the product pages (adjust as needed)
base_url = "https://supersports.com.vn"

# Mapping for US to EU size conversions
us_to_eu_size_mapping = {
    "3.0": (34, 35),
    "4.0": (36, 37),
    "5.0": (37, 38),
    "6.0": (38, 39),
    "7.0": (39, 40),
    "8.0": (41, 42),
    "9.0": (42, 43),
    "10.0": (43, 44),
}

# Mapping for mixed sizes (Men's and Women's)
mixed_size_to_eu_mapping = {
    "M3": (34, 35),
    "M4": (36, 37),
    "M5": (37, 38),
    "M6": (38, 39),
    "M7": (39, 40),
    "M8": (41, 42),
    "M9": (42, 43),
    "M10": (43, 44),
    "W5": (34, 35),
    "W6": (36, 37),
    "W7": (37, 38),
    "W8": (38, 39),
    "W9": (39, 40),
    "W10": (41, 42),
    "W11": (42, 43),
    "W12": (43, 44),
}

# Function to convert US sizes to EU sizes
def us_to_eu_size(us_size):
    return us_to_eu_size_mapping.get(str(us_size), None)

# Function to convert mixed size formats to EU sizes
def convert_mixed_size(mixed_size):
    parts = mixed_size.split('|')
    us_size = parts[0].strip()
    return mixed_size_to_eu_mapping.get(us_size, None)

# Function to format size as "US" and "EUR"
def format_size(size_str):
    size_str = size_str.strip()
    
    # Handle mixed formats like "M3 | W5"
    if '|' in size_str:
        eu_size = convert_mixed_size(size_str)
        us_size = size_str.split('|')[0].strip()
        return {
            "US": us_size,
            "EUR": eu_size
        }
    
    # If size is in standard US format
    if 'US' in size_str:
        us_size = size_str.replace('US', '').strip()
        eu_size = us_to_eu_size(us_size)
        return {
            "US": us_size,
            "EUR": eu_size
        }
    
    # If size is in Women's format (e.g., "W6")
    if 'W' in size_str:
        us_size = size_str.replace('W', '').strip()
        eu_size = convert_mixed_size(f"W{us_size}")
        return {
            "US": size_str,
            "EUR": eu_size
        }
    
    return None

# Function to process and format sizes
def process_sizes(size_data):
    if isinstance(size_data, str):
        sizes = [format_size(size) for size in size_data.split('-') if format_size(size)]
        return [size for size in sizes if size is not None]
    elif isinstance(size_data, list):
        sizes = []
        for size in size_data:
            sizes.extend([format_size(s) for s in size.split('-') if format_size(s)])
        return [size for size in sizes if size is not None]
    else:
        return []

# Function to normalize price (remove currency symbols and commas)
def normalize_price(price):
    price = re.sub(r'[^\d]', '', str(price))  # Remove non-digit characters
    return int(price) if price else None  # Return None if no price

# Function to ensure full URL
def ensure_full_url(url):
    if not url.startswith('http'):
        return urljoin(base_url, url)
    return url

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
    
    # Normalize and format sizes
    if 'sizes' in product:
        product['sizes'] = process_sizes(product['sizes'])
    
    # Ensure full product URL
    if 'product_url' in product:
        product['product_url'] = ensure_full_url(product['product_url'])

# Step 3: Write the cleaned data to a new file
with open(cleaned_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("fCleaned data has been written to {cleaned_file} successfully!")
