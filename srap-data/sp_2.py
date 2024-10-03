import json
import re

# Function to convert price from string to integer
def convert_price(price_str):
    if price_str:  # Check if the price string exists
        return int(re.sub(r"[^\d]", "", price_str)) 
    return 0  
# Function to convert sizes to the desired format and add vn_size
def convert_sizes(sizes):
    converted_sizes = []
    vn_sizes = []
    
    # Extended VN size mapping from US sizes
    us_to_vn_mapping = {
        "US 7": 40, "US 8": 41, "US 9": 42, "US 10": 43, "US 11": 44, 
        "US M3W5": 35, "US M4W6": 36, "US M5W7": 37, "US M6W8": 38, "US M7W9": 39,
        "US M8W10": 40, "US M9W11": 41, "US M10W12": 42,
        "US 3/5": 35, "US 4/6": 36, "US 5/7": 37, "US 6/8": 38, "US 7/9": 39,
        "US 8/10": 40, "US 9/11": 41, "US 10/12": 42, "US 11/13": 43, "US 12/14": 44,
        "UK 4": 37, "UK 5": 38, "UK 6": 39, "UK 7": 40, "UK 8": 41, "UK 9": 42,
        "UK 10": 43, "UK 11": 44  
    }
    
    for size in sizes:
        converted_sizes.append({
            "US": size,
            "EUR": "",  
            "cm": ""    
        })
        
        # Map size to VN size using the dictionary, if exists
        vn_size = us_to_vn_mapping.get(size, None)  
        if vn_size is not None:
            vn_sizes.append(vn_size)  
    return converted_sizes, vn_sizes

# Function to convert each product to the desired format
def convert_product(product):
    sizes, vn_sizes = convert_sizes(product.get("sizes", []))
    product_url = product.get("product_url", "")
    sku_matches = re.findall(r'\d+-\w+', product_url)  
    sku = sku_matches[0] if sku_matches else ""  

    return {
        "image_url": "https:" + product.get("image_url", ""),  
        "name": product.get("name", ""),
        "product_url": "https://supersports.com.vn" + product_url,
        "sale_price": convert_price(product.get("sale_price", "")),  
        "price": convert_price(product.get("price", "")), 
        "discount": product.get("discount", ""),
        "sizes": sizes,
        "vn_size": vn_sizes,  
        "gender": "Unisex" if "unisex" in product.get("name", "").lower() else "Men", 
        "color": product.get("name", "").split("-")[-1].strip(),  
        "upper_material": product.get("lining", ""),
        "lining": product.get("lining", ""),
        "sole": "",
        "product_features": product.get("product_features", "")
    }

# Function to process the entire file
def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        raw_data = json.load(file)

    # Process each product in the list
    formatted_data = [convert_product(product) for product in raw_data]

    # Save the formatted data to a new file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(formatted_data, file, indent=4, ensure_ascii=False)

    print(f"Data has been processed and saved to {output_file}")


input_file = 'data/supersports.json' 
output_file = 'sp_clean.json' 

process_file(input_file, output_file)
