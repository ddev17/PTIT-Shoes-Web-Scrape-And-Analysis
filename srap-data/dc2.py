import json

# Read the product data from a JSON file
with open('data_clean/drake_clean.json', 'r', encoding='utf-8') as file:
    product_data_list = json.load(file)

# Modify each product data object in the array
for product_data in product_data_list:
    # Remove the 'sku' field
    product_data.pop('sku', None)

# Write the modified product data back to the same JSON file
with open('data_clean/drake_clean.json', 'w', encoding='utf-8') as file:
    json.dump(product_data_list, file, ensure_ascii=False, indent=4)

print("Product data has been modified and saved to 'data_clean/drake_clean.json'.")
