import json
import os
import argparse

# Function to preprocess shoe data from JSON
def preprocess_shoe_data(file):
    sentences = []
    
    # Open and load the JSON file
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for product in data:
        sentence = []
        
        # Add individual attributes as tagged tokens
        sentence.append(f"{product['price']}/PRICE")
        sentence.append(f"{product['gender']}/GENDER")
        sentence.append(f"{product['color']}/COLOR")
        sentence.append(f"{product['name'].replace(' ', '_')}/NAME")
        sentence.append(f"{product['material']}/MATERIAL")
        sentence.append(f"{product['min_size(vn_size)']}/MIN_SIZE")
        sentence.append(f"{product['max_size(vn_size)']}/MAX_SIZE")
        sentence.append(f"{product['lining']}/LINING")
        sentence.append(f"{product['sole']}/SOLE")
        
        # Check if 'description' exists and is not None
        description = product.get('description', None)
        if description:
            # Tokenize description and label each token as part of description
            description_tokens = description.split()
            for token in description_tokens:
                sentence.append(f"{token}/DESCRIPTION")
        
        # Append the processed sentence to the list of sentences
        sentences.append(" ".join(sentence))
    
    return sentences

# Function to save processed data to a text file
def save_processed_data(sentences, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(sentence + "\n")
    print(f"{len(sentences)} sentences saved to {output_file}")

# Main function to convert raw JSON data to processed format
def raw_to_corpus(input_file, output_file):
    sentences = preprocess_shoe_data(input_file)
    save_processed_data(sentences, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Preprocess shoe data from JSON to text format.")
    parser.add_argument("--input", help="Input JSON file containing the shoe data", required=True)
    parser.add_argument("--output", help="Output file to save processed data", required=True)
    args = parser.parse_args()
    
    raw_to_corpus(args.input, args.output)
