'''
Store data in MongoDB Atlas or other databases/files (CSV, JSON, etc.)
'''
import json
from .utils.process import processDocument
import pandas as pd
from pathlib import Path

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

    # Example usage
    # store_documents_in_csv(documents)
                