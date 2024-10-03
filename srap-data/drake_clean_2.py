import json


def clean_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    cleaned_data = []
    
    for item in data:
        # Extract only the required fields
        cleaned_item = {
            "price": item.get("price"),
            "gender": item.get("gender"),
            "color": item.get("color"),
            "name": item.get("name"),
            "material": item.get("upper_material"),
            "min_size(vn_size)": min(item.get("vn_size", []), default=None),
            "max_size(vn_size)": max(item.get("vn_size", []), default=None),
            "lining": item.get("lining"),
            "sole": item.get("sole"),
            "description": item.get("product_features")
        }
        cleaned_data.append(cleaned_item)
    
    # Save the cleaned data to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(cleaned_data, file, ensure_ascii=False, indent=4)


input_file = 'data_clean/drake_clean.json'  
output_file = 'data_clean/drake_clean_2.json'  

clean_data(input_file, output_file)

print(f"Data cleaned and saved to {output_file}")

# //////////////////////////////////////////////////////

# import json
# from googletrans import Translator

# translator = Translator()

# def translate_to_vietnamese(text):
#     if text is None:
#         return None
#     translated = translator.translate(text, src='en', dest='vi')
#     return translated.text


# def clean_data(input_file, output_file):
#     with open(input_file, 'r', encoding='utf-8') as file:
#         data = json.load(file)
    
#     cleaned_data = []
    
#     for item in data:
#         cleaned_item = {
#             "price": item.get("price"),
#             "gender": item.get("gender"),
#             "color": translate_to_vietnamese(item.get("color")),
#             "name": translate_to_vietnamese(item.get("name")),
#             "material": translate_to_vietnamese(item.get("upper_material")),
#             "min_size(vn_size)": min(item.get("vn_size", []), default=None),
#             "max_size(vn_size)": max(item.get("vn_size", []), default=None),
#             "lining": translate_to_vietnamese(item.get("lining")),
#             "sole": translate_to_vietnamese(item.get("sole")),
#             "description": item.get("product_features")
#         }
#         cleaned_data.append(cleaned_item)
    
#     with open(output_file, 'w', encoding='utf-8') as file:
#         json.dump(cleaned_data, file, ensure_ascii=False, indent=4)


# input_file = 'data_clean/drake_clean.json'  
# output_file = 'data_clean/drake_clean_2.json' 

# clean_data(input_file, output_file)

# print(f"Data cleaned, translated, and saved to {output_file}")
