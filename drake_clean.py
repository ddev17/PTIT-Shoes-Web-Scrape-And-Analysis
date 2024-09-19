import re
import json

# Path to the original scraped data file
scrap_file = 'drake.json'

# Path to the new cleaned file
cleaned_file = 'drake_clean.json'

# Function to normalize price
def normalize_price(price):
    # Remove currency symbols and commas
    price = re.sub(r'[^\d]', '', price)
    return int(price)

# Function to normalize sizes and extract Vietnamese-friendly size (cm)
def normalize_size(size_str):
    # Mapping for special size cases like "OS", "FREE"
    special_sizes = {
        "OS": "One Size",
        "FREE": "Free Size",
        "L": "Large",
        "M": "Medium",
        "S": "Small",
        "XL": "Extra Large",
        "XS": "Extra Small"
    }
    
    # If size is a special size, return the standardized term
    if size_str in special_sizes:
        return special_sizes[size_str], None
    
    # Otherwise, assume it's a size like "10.5US - 44.5EUR - 28.5cm"
    sizes = [s.strip() for s in size_str.split('-')]
    
    # Create a structured dictionary with size categories
    size_dict = {}
    vn_size = None
    for size in sizes:
        if 'US' in size:
            size_dict['US'] = size.replace('US', '').strip()
        elif 'EUR' in size:
            size_dict['EUR'] = size.replace('EUR', '').strip()
        elif 'cm' in size:
            size_cm = size.replace('cm', '').strip()
            size_dict['cm'] = size_cm
            vn_size = cm_to_vn_size(float(size_cm))  # Convert cm to Vietnamese size

    return size_dict, vn_size

# Function to convert cm size to Vietnamese size
def cm_to_vn_size(cm_size):
    if cm_size < 23.0:
        return None
    elif cm_size == 23.0:
        return 36
    elif cm_size == 23.5:
        return 37
    elif cm_size == 24.0:
        return 38
    elif cm_size == 24.5:
        return 39
    elif cm_size == 25.0:
        return 40
    elif cm_size == 25.5:
        return 41
    elif cm_size == 26.0:
        return 42
    elif cm_size == 26.5:
        return 43
    elif cm_size == 27.0:
        return 44
    elif cm_size == 27.5:
        return 45
    elif cm_size == 28.0:
        return 46
    else:
        return None  # For sizes above 28cm

# Step 1: Read data from the original scraped file
with open(scrap_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Step 2: Clean and normalize the data
for product in data:
    # Normalize prices
    if 'sale_price' in product:
        product['sale_price'] = normalize_price(product['sale_price'])
    if 'drake_price' in product:
        product['drake_price'] = normalize_price(product['drake_price'])
    
    # Normalize sizes if available
    if 'sizes' in product:
        normalized_sizes = []
        vn_sizes = []
        for size in product['sizes']:
            norm_size, vn_size = normalize_size(size)
            normalized_sizes.append(norm_size)
            if vn_size is not None:
                vn_sizes.append(vn_size)  # Collect all Vietnamese sizes
            
        product['sizes'] = normalized_sizes
        product['vn_size'] = vn_sizes  # Add the Vietnamese-friendly size list

# Step 3: Write the cleaned data to a new file
with open(cleaned_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Cleaned data with 'vn_size' has been written to {cleaned_file} successfully!")
