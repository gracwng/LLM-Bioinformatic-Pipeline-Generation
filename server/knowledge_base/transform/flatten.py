'''
Flatten every document object so that every field can be properly recognized by MongoDBAtlasVectorSearch
Immediately after flattening, add to MongoDB database
'''
import os
from server.knowledge_base.storage.document_storing import DocumentStorage
import json

def flatten_dict(d, parent_key='', sep='_'):
    """
    Flatten a nested dictionary. Each nested field will be merged into the top level
    with a separator between levels.
    """
    items = []
    for k, v in d.items():
        if isinstance(v, dict):
            items.extend(flatten_dict(v, sep=sep).items())
        else:
            items.append((k, v))
    return dict(items)

def main():

    # Read the original JSON file
    with open('cwl_documents/embedded_documents.json', 'r') as file:
        data = json.load(file)

    # Flatten each object and store in an array
    flattened_array = []
    for item in data:
        flattened_item = flatten_dict(item)
        flattened_array.append(flattened_item)

    mongodb_cleaned_cwl_files_config = {
        'MONGODB_URI': os.environ.get('MONGODB_URI'),
        'DB_NAME': 'LLM-Bioinformatic-Pipeline-Generation',
        'COLLECTION_NAME': 'Cleaned-CWL-Files'
        }
    documentStorage = DocumentStorage('github')
    documentStorage.storeDocumentsInMongoDB(flattened_array, mongodb_cleaned_cwl_files_config)

if __name__ == '__main__':
    # main()
    pass