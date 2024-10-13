import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def filter_json(json_data, existing_sources):
    return [item for item in json_data if item.get('source') not in existing_sources]

def save_filtered_json(filtered_data, output_file):
    with open(output_file, 'w') as file:
        json.dump(filtered_data, file, indent=2)

# File paths
json_file_path1 = '/Users/gracewang/Documents/Breakthrough AI/Axle Informatics/LLM-Bioinformatic-Pipeline-Generation/axle-env/workflowhub/raw_data/cwl_documents.json'
json_file_path2 = '/Users/gracewang/Documents/Breakthrough AI/Axle Informatics/LLM-Bioinformatic-Pipeline-Generation/cwl_documents/raw_data/cwl_documents.json'
output_file_path = 'filtered_cwl_documents.json'

# Load data
json_data1 = load_json(json_file_path1)
json_data2 = load_json(json_file_path2)

# Extract sources from the second JSON file
existing_sources = set(item.get('source') for item in json_data2 if 'source' in item)

# Filter JSON data
filtered_data = filter_json(json_data1, existing_sources)

# Save filtered data
save_filtered_json(filtered_data, output_file_path)

print(f"Original JSON items: {len(json_data1)}")
print(f"Filtered JSON items: {len(filtered_data)}")
print(f"Filtered data saved to {output_file_path}")