import json

# Define function to load shoe data from file
def load_shoe_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        shoe_data = json.load(f)
    return shoe_data

def create_intent_data(shoe_data):
    intents = []

    common_patterns = [
        "I want a {} shoe", "Show me {} shoes", "Do you have {} shoes", 
        "I'm looking for {} shoes", "What {} shoes do you have"
    ]
    general_responses = [
        "Here are some {} shoes you might like.", 
        "We have a great selection of {} shoes.",
        "Check out these {} shoes."
    ]

    for shoe in shoe_data:
        tag = f"{shoe['name']} {shoe['color']}".replace(" ", "_").lower()

        # Create patterns for the shoe based on attributes like color, name, gender, etc.
        patterns = [pattern.format(shoe["color"]) for pattern in common_patterns] + [
            f"Show me {shoe['name']}", f"I want {shoe['name']}", 
            f"Do you have {shoe['name']}", f"What is {shoe['name']} like?"
        ]
        
        response = f"{shoe['name']} in {shoe['color']} color, available in size {shoe['min_size(vn_size)']} to {shoe['max_size(vn_size)']}. Material: {shoe['material']}, Sole: {shoe['sole']}. {shoe['description']} Price: {shoe['price']}."

        intents.append({
            "tag": tag,
            "patterns": patterns,
            "responses": [response],
            "context_set": ""
        })
    
    general_intents = [
        {"tag": "greeting",
         "patterns": ["Hi", "Hello", "Good day", "Is anyone there?"],
         "responses": ["Hello! How can I assist you with shoes today?", "Hi there! Looking for something specific?"],
         "context_set": ""
        },
        {"tag": "thanks",
         "patterns": ["Thanks", "Thank you", "That's helpful"],
         "responses": ["Happy to help!", "Anytime!", "You're welcome!"]
        }
    ]

    intents.extend(general_intents)
    
    return {"intents": intents}

def save_intent_data(intent_data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(intent_data, f, ensure_ascii=False, indent=4)

def main(input_file, output_file):
    shoe_data = load_shoe_data(input_file)
    intent_data = create_intent_data(shoe_data)
    save_intent_data(intent_data, output_file)
    print(f"Intent data saved to {output_file}")

if __name__ == "__main__":
    input_file = "drake-train.json"  
    output_file = "intent.json"
    main(input_file, output_file)
