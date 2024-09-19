import re
import json
from urllib.parse import urljoin

# Path to the original scraped data file
scrap_file = 'supersports.json'  # Thay thế bằng tên file thực tế
cleaned_file = 'supersports_clean.json'  # File sau khi chuẩn hóa

# Base URL of the website
base_url = 'https://supersports.com.vn'

# Function to normalize price (remove currency symbols and commas)
def normalize_price(price):
    price = re.sub(r'[^\d]', '', str(price))  # Loại bỏ ký tự không phải số
    return int(price) if price else None  # Trả về None nếu không có giá

# Function to format size as "US <size>"
def format_us_size(size_str):
    size_str = size_str.strip()
    if 'US' in size_str:
        return f"US {size_str.replace('US', '').strip()}"
    return None

# Function to process and format US sizes
def process_us_sizes(size_data):
    if isinstance(size_data, str):
        us_sizes = [format_us_size(size) for size in size_data.split('-') if format_us_size(size)]
        return us_sizes
    elif isinstance(size_data, list):
        us_sizes = []
        for size in size_data:
            us_sizes.extend([format_us_size(s) for s in size.split('-') if format_us_size(s)])
        return us_sizes
    else:
        return []

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
    
    # Normalize and format US sizes
    if 'sizes' in product:
        product['sizes'] = process_us_sizes(product['sizes'])
    
    # Ensure product_url is a full URL
    if 'product_url' in product:
        product['product_url'] = ensure_full_url(product['product_url'])

# Step 3: Write the cleaned data to a new file
with open(cleaned_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Cleaned data with formatted US sizes, normalized prices, and full URLs has been written to {cleaned_file} successfully!")
