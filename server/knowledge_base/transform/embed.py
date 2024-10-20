# given a json object within a json file, create embeddings for each object's page_content and description fields

import json
from server.knowledge_base.transform.document_transforming import TransformDocument
from langchain_openai import OpenAIEmbeddings

def readDocuments():
    # read in documents from the enhanced_documents.json file
    transformDocument = TransformDocument()
    srcLink = 'cwl_documents/documents_with_descriptions.json'
    documents = transformDocument.readJson(srcLink)
    print("Documents have been read from 'enhanced_documents.json'")    

    return documents

def removeEmbeddingFields(documents):
    for doc in documents:
        doc['metadata'].pop('embedding', None)
    print("Embedding fields have been removed from each document")
    return documents

def generateEmbeddings(documents):
    embeddings_model = OpenAIEmbeddings()

    for doc in documents:
        if doc['page_content'] is not None:
            doc['metadata']['page_content_embedding'] = embeddings_model.embed_query(doc['page_content'])
        if doc['metadata']['description'] is not None:
            doc['metadata']['description_embedding'] = embeddings_model.embed_query(doc['metadata']['description'])
    print("Embeddings have been generated for each document")
    pass

def saveDocuments(documents):
     # Write the formatted documents to a JSON file
    dest = 'cwl_documents/embedded_documents.json'
    with open(dest, 'w') as json_file:
        json.dump(documents, json_file, indent=2)

    print("Enhanced documents have been saved to 'embedded_documents.json'")
    pass

def main():
    '''
    read the enhanced_documents json file
    for each object, remove the embedding field, create a page_content_embedding field, and a description_embedding field
    then generate embeddings for each of these fields
    save objects in new json file
    '''
    documents = readDocuments()
    documents = removeEmbeddingFields(documents)
    # documents = documents[:5]
    generateEmbeddings(documents)
    saveDocuments(documents)
    pass

if __name__ == '__main__':
    main()
    pass