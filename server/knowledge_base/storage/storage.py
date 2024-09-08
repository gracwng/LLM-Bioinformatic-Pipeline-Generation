'''
Store data in MongoDB Atlas or other databases
'''

from .utils.process import processDocument
import pandas as pd

class DocumentStorage:

    def __init__(self, source: str) -> None: 
        self.source = source
       
    def storeRawDocumentsInCSV(self, documents):
        if self.source == 'github':
            csv_data = [processDocument(doc) for doc in documents]
            
            df = pd.DataFrame(csv_data)
            csv_file_path = 'cwl_documents/cwl_documents.csv'
            df.to_csv(csv_file_path, index=False)
            print(f"Documents saved to {csv_file_path}")

    # Example usage
    # store_documents_in_csv(documents)
                