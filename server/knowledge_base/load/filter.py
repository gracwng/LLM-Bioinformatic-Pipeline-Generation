import json

# this script here checks if our json file contains any duplicate objects
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def remove_duplicates_by_source(data):
    unique_sources = set()
    result = []

    for item in data:
        if item.get('source') and item['source'] not in unique_sources:
            unique_sources.add(item['source'])
            result.append(item)
        else:
            print(f"Duplicate source: {item['source']}")

    return result

def save_filtered_json(filtered_data, output_file):
    with open(output_file, 'w') as file:
        json.dump(filtered_data, file, indent=2)

# File paths
json_file_path1 = 'cwl_documents/merged_cwl_documents.json'
output_file_path = json_file_path1

# Load data
json_data1 = load_json(json_file_path1)

# Filter JSON data
filtered_data = remove_duplicates_by_source(json_data1)

# Save filtered data
# save_filtered_json(filtered_data, output_file_path)

print(f"Original JSON items: {len(json_data1)}")
print(f"Filtered JSON items: {len(filtered_data)}")
print(f"Filtered data saved to {output_file_path}")