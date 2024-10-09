import json
from googletrans import Translator

# Initialize the translator
translator = Translator()

# Define function to load shoe data from file
def load_shoe_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        shoe_data = json.load(f)
    return shoe_data

# Define function to translate Vietnamese text to English
def translate_text(text):
    translation = translator.translate(text, src="vi", dest="en")
    return translation.text

# Define function to create intent data from shoe data
def create_intent_data(shoe_data):
    intents = []

    # Define general patterns and responses based on typical user queries
    common_patterns = [
        "I want a {} shoe", "Show me {} shoes", "Do you have {} shoes", 
        "I'm looking for {} shoes", "What {} shoes do you have"
    ]
    
    for shoe in shoe_data:
        tag = f"{shoe['name']} {shoe['color']}".replace(" ", "_").lower()

        # Create patterns for the shoe based on attributes like color, name, etc.
        patterns = [pattern.format(shoe["color"]) for pattern in common_patterns] + [
            f"Show me {shoe['name']}", f"I want {shoe['name']}", 
            f"Do you have {shoe['name']}", f"What is {shoe['name']} like?"
        ]
        
        # Original response containing both English and Vietnamese
        original_response = f"{shoe['name']} in {shoe['color']} color, available in size {shoe['min_size(vn_size)']} to {shoe['max_size(vn_size)']}. Material: {shoe['material']}, Sole: {shoe['sole']}. {shoe['description']} Price: {shoe['price']}."

        # Translate the original response from Vietnamese to English
        translated_response = translate_text(original_response)

        intents.append({
            "tag": tag,
            "patterns": patterns,
            "responses": [translated_response],
            "context_set": ""
        })
    
    return {"intents": intents}

# Define function to save intent data to json file
def save_intent_data(intent_data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(intent_data, f, ensure_ascii=False, indent=4)

# Main function to orchestrate the process
def main(input_file, output_file):
    shoe_data = load_shoe_data(input_file)
    intent_data = create_intent_data(shoe_data)
    save_intent_data(intent_data, output_file)
    print(f"Intent data saved to {output_file}")

# Execute main function with file paths
if __name__ == "__main__":
    input_file = "drake-train.json" 
    output_file = "intent2.json"
    main(input_file, output_file)
