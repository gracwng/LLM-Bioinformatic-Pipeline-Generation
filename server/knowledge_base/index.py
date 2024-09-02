import json
import os
import pymongo
from pymongo import MongoClient

# from server.knowledge_base.load.document_loading import DocumentLoader
# from server.knowledge_base.load.config import common_workflow_library_config
from server.knowledge_base import DocumentLoader, common_workflow_library_config, datirium_workflow_config, ncbi_cwl_ngs_workflow_config
# client = pymongo.MongoClient("mongodb+srv://granx:CzhklAsvIcilxtxV@dev.rm7ss.mongodb.net/")

'''
Load documents from github, workflowhub, other sources
Parse & transform documents so they fit the MongoDB db schema
Store documents into MongoDB
'''
def save_documents_as_cwl(documents, directory="cwl_documents"):
    """Save documents as CWL files."""
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory if it doesn't exist

    for i, document in enumerate(documents):
        file_path = os.path.join(directory, f"document_{i + 1}.cwl")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(document)  # Assuming document is a string representing a CWL file
        print(f"Saved: {file_path}")
def main():
    docLoader = DocumentLoader('github')
    documents = docLoader.getDocuments(common_workflow_library_config)

    # Check the size of the documents array
    size_of_documents = len(documents)
    # Save only the first 5 documents
    first_five_documents = documents[:5]  # Get the first 5 documents


    print(f"Total number of documents retrieved: {size_of_documents}")
    print(first_five_documents[0].page_content)
    print(first_five_documents[0].metadata)
    # save_documents_as_cwl(first_five_documents)  # If documents are dictionaries
if __name__ == '__main__':
    main()