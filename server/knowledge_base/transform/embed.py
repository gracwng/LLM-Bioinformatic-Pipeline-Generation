# given a json object within a json file, create embeddings for each object's page_content and description fields

import json
import os
from server.knowledge_base.transform.document_transforming import TransformDocument
from langchain_openai import OpenAIEmbeddings
from server.knowledge_base.storage.document_storing import DocumentStorage  # for storing documents in MongoDB  
def readDocuments(srcLink):
    # read in documents from the enhanced_documents.json file
    transformDocument = TransformDocument()
    documents = transformDocument.readJson(srcLink)
    print(f"Documents have been read from '{srcLink}'")    

    return documents

def removeEmbeddingFields(documents):
    for doc in documents:
        doc['metadata'].pop('embedding', None)
    print("Embedding fields have been removed from each document")
    return documents

def generateEmbeddings(documents):
    embeddings_model = OpenAIEmbeddings(
        model="text-embedding-3-large",
        dimensions = 3072
    )

    for doc in documents:
        if doc['page_content'] is not None:
            doc['metadata']['page_content_embedding'] = embeddings_model.embed_query(doc['page_content'])
        if doc['metadata']['description'] is not None:
            doc['metadata']['description_embedding'] = embeddings_model.embed_query(doc['metadata']['description'])
    print("Embeddings have been generated for each document")
    pass

def saveDocuments(documents, dest):
     # Write the formatted documents to a JSON file
    with open(dest, 'w') as json_file:
        json.dump(documents, json_file, indent=2)

    print(f"Enhanced documents have been saved to {dest}")
    pass

def createEmbeddings():
    '''
    read the enhanced_documents json file
    for each object, remove the embedding field, create a page_content_embedding field, and a description_embedding field
    then generate embeddings for each of these fields
    save objects in new json file
    '''
    srcLink = 'cwl_documents/documents_with_descriptions.json'
    destLink = 'cwl_documents/embedded_documents.json'
    documents = readDocuments(srcLink)
    documents = removeEmbeddingFields(documents)
    # documents = documents[:5]
    generateEmbeddings(documents)
    saveDocuments(documents, destLink)
    pass

# this function takes documents (array of doc objects) that contain embeddings of page_content and description into MongoDB database
def addEmbeddingsToMongoDB():
    srcLink = 'cwl_documents/embedded_documents.json'
    documents = readDocuments(srcLink)
    mongodb_cleaned_cwl_files_config = {
        'MONGODB_URI': os.environ.get('MONGODB_URI'),
        'DB_NAME': 'LLM-Bioinformatic-Pipeline-Generation',
        'COLLECTION_NAME': 'Cleaned-CWL-Files'
        }
    documentStorage = DocumentStorage('github')
    documentStorage.storeDocumentsInMongoDB(documents, mongodb_cleaned_cwl_files_config)


def main():
    
    addEmbeddingsToMongoDB()
    pass

if __name__ == '__main__':
    main()
    pass