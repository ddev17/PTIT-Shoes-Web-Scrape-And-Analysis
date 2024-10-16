import json

# Define the keys you want to keep
desired_keys = [
    "price", "gender", "color", "name", "material",
    "min_size(vn_size)", "max_size(vn_size)", "lining"
]

# Function to filter the object based on the desired keys


def filter_object(data, desired_keys):
    return {key: value for key, value in data.items() if key in desired_keys}

# Function to check if all desired keys are present in the object


def has_all_desired_keys(data, desired_keys):
    return all(key in data for key in desired_keys)


# List to hold the filtered objects from all files
merged_data = []

# Load and filter each JSON file (which contains a list of objects) with UTF-8 encoding
for file_name in ['./data_clean/cleaned_adidas2.json', './data_clean/drake_clean_2.json', './data_clean/sp_clean_2.json']:
    with open(file_name, 'r', encoding='utf-8') as file:
        data_list = json.load(file)  # data_list is a list of objects
        # Filter each object in the list and extend the merged_data
        for data in data_list:
            if has_all_desired_keys(data, desired_keys):
                filtered_data = filter_object(data, desired_keys)
                merged_data.append(filtered_data)

# Save the merged data back to a file with UTF-8 encoding
with open('./data_clean/shoes_data.json', 'w', encoding='utf-8') as outfile:
    json.dump(merged_data, outfile, ensure_ascii=False, indent=4)

print("Merged data:", merged_data)
