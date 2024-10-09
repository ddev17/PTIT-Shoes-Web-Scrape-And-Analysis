from languageflow.reader.tagged_corpus import TaggedCorpus

# Function to clean lines
def clean_line(line):
    return line.encode('ascii', 'ignore').decode('ascii')

# util/crf/load_data.py
def load_dataset(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                cleaned_line = clean_line(line)  
                if not cleaned_line.strip():
                    continue  # Skip empty lines

                parts = cleaned_line.strip().split()
                for part in parts:
                    # Check for valid token/tag format
                    if '/' in part:
                        token, label = part.rsplit('/', 1)
                        if token.strip() and label.strip():
                            data.append((token.strip(), label.strip()))
                        else:
                            print(f"Skipping empty token/label pair: {part}")
                    else:
                        print(f"Skipping part: {part} - Expected a token/tag pair.")
        
        if not data:
            print("No valid data found in the dataset.")
    except Exception as e:
        print(f"Error loading dataset from {file_path}: {e}")
    return data
