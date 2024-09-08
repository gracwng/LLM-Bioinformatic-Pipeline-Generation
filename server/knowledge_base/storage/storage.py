'''
Store data in MongoDB Atlas or other databases
'''


class DocumentsStorage:

    def __init__(self, source: str) -> None: 
        self.source = source

    def storeDocumentInCSV(self, document):
    
    def storeDocumentsInCSV(self, documents):
        documents = []  # Initialize an empty list to hold documents
        try:
            if self.source == 'github':
                

        except Exception as e:
            print(f"An error occurred while loading documents: {e}")
            return None  # Return None or handle the error as needed

        