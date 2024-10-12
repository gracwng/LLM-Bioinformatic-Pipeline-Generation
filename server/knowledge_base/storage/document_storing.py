'''
Store data in MongoDB Atlas or other databases/files (CSV, JSON, etc.)
'''
import json
from .utils.process import processDocument
import pandas as pd
from pathlib import Path
from .utils.atlas_client import AtlasClient

class DocumentStorage:

    def __init__(self, source: str) -> None: 
        self.source = source
    
    def storeRawDocumentsInCSV(self, documents):
        if self.source == 'github':
            csv_data = [processDocument(doc) for doc in documents]
            
            df = pd.DataFrame(csv_data)
            csv_file_path = 'cwl_documents/raw_data/cwl_documents.csv'
            df.to_csv(csv_file_path, index=False)
            print(f"Documents saved to {csv_file_path}")

    def storeRawDocumentsInJSON(self, documents):
        if self.source == 'github':
            json_data = [processDocument(doc) for doc in documents]
            
            json_file_path = 'cwl_documents/raw_data/cwl_documents.json'
            Path('cwl_documents').mkdir(parents=True, exist_ok=True)
            with open(json_file_path, 'w') as f:
                json.dump(json_data, f, indent=2)
            print(f"Documents saved to {json_file_path}")

    def storeDocumentsInMongoDB(self, documents, config):
        if self.source == 'github':
            json_data = [processDocument(doc) for doc in documents]
        database, collection = self.initializeDatabase(config)
        database.addDocuments(collection, json_data)
        print(f"Documents stored in MongoDB Atlas collection: {collection}")

    # Initialize the MongoDB database
    def initializeDatabase(self, config):
        '''Expected configuration example:
            mongodb_raw_cwl_files_config = {
                'MONGODB_URI': os.environ.get('MONGODB_URI'),
                'DB_NAME': 'LLM-Bioinformatic-Pipeline-Generation',
                'COLLECTION_NAME': 'Raw-CWL-Files'
                }
        '''
        MONGODB_URI = config['MONGODB_URI']
        DB_NAME = config['DB_NAME']
        collection = config['COLLECTION_NAME']
        database = AtlasClient(MONGODB_URI, DB_NAME)
        return database, collection

