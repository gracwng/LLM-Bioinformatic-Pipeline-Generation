'''
Transform data 
'''

''' Create Database Schema (defining our document structure for our DB)'''
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import getpass
import os

cwl_schema = {
    "_id": ObjectId,
    "description": str,
    "source": str,
    "content": str,
    "embedding": object,  # This will be a list or numpy array, depending on your embedding
    "class": str,
    "inputs": str,
    "outputs": str,
    "baseCommand": str,
    "hints": str,
    "cwlVersion": str,
    # "steps": list,
    "arguments": str,
    "requirements": str,
    "createdAt": datetime.datetime,
    "updatedAt": datetime.datetime
}

# for each document, we want to extract the fields from the cwl_schema and create a new document object with it
class TransformDocument:
    def readJson(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
        return data
    '''
    Takes a list of raw documents in the form of an array of json objects and transforms them to fit the schema (essentially filtering out the fields we don't need)
    '''
    def transformDocuments(self, documents): # idea: take each json object and transform it to fit the schema
        transformedDocs = [self.transformDocument(doc) for doc in documents]
        return transformedDocs
    
    def transformDocument(self, document):
        transformedDoc = {}
        for key in cwl_schema.keys():
            if key == "_id":
                transformedDoc[key] = str(ObjectId())
            elif key == "createdAt" or key == "updatedAt":
                transformedDoc[key] = str(datetime.datetime.now())
            elif key == "description":
                transformedDoc[key] = document.get("cwl_doc", None)
                if transformedDoc[key] == None: # we want to generate our own descriptions here
                    
                    pass
            else:
                if key in document:
                    transformedDoc[key] = document[key]
                elif f"cwl_{key}" in document:
                    transformedDoc[key] = document.get(f"cwl_{key}", None)
                else:
                    transformedDoc[key] = None
        return transformedDoc

    def saveTransformedDocuments(self, documents, overWrite=False):
        if overWrite:
            with open('cwl_documents/transformed_data/cwl_documents_transformed.json', 'w') as f:
                json.dump(documents, f, indent=2)
            print("Transformed documents saved to cwl_documents/transformed_data/transformed_cwl_documents.json")
        else:
            print("Permissions denied. Transformed documents not saved")

if __name__ == '__main__':
    transformDocument = TransformDocument()
    documents = transformDocument.readJson('cwl_documents/raw_data/cwl_documents.json')
    transformedDocuments = transformDocument.transformDocuments(documents)
    transformDocument.saveTransformedDocuments(transformedDocuments)
    