'''
Provide functions for fetching and loading documents from different database sources

'''
from server.knowledge_base.load.loaders import gitHubLoader

class DocumentLoader:

    def __init__(self, source: str) -> None: 
        self.source = source
    
    def getDocument(self, config: dict[str, str]):
        documents = []  # Initialize an empty list to hold documents
        try:
            if self.source == 'github':
                documents = gitHubLoader(config)  # Attempt to load documents from GitHub

            if documents:  # Check if documents were successfully loaded
                return documents
            else:
                print("No documents found.")
                return None

        except Exception as e:
            print(f"An error occurred while loading documents: {e}")
            return None  # Return None or handle the error as needed

    def getDocuments(self, configs: list[dict[str, str]]):
        documents = []  # Initialize an empty list to hold documents
        if self.source == 'github':
            for config in configs:
                try:
                    # Attempt to get documents for the current config
                    docs = self.getDocument(config)
                    if docs:  # Check if any documents were returned
                        documents += docs  # Append the retrieved documents
                    else:
                        print(f"No documents found for config: {config}")
                except Exception as e:
                    print(f"An error occurred while getting documents for config {config}: {e}")

        return documents
    
    