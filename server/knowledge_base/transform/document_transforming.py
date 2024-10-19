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

    def saveTransformedDocuments(self, documents, destLink, overWrite=False):
        # before saving, remove all duplicates
        unique_documents = self.removeDuplicatesBySource(documents)
        if overWrite:
            with open(destLink, 'w') as f:
                json.dump(unique_documents, f, indent=2)
            print("Transformed documents saved to ", destLink)
        else:
            print("Permissions denied. Transformed documents not saved")
    
    def removeDuplicatesBySource(self, data):
        unique_sources = set()
        result = []

        for item in data:
            if item.get('source') and item['source'] not in unique_sources:
                unique_sources.add(item['source'])
                result.append(item)
            else:
                print(f"Duplicate source: {item['source']}")

        return result
    
if __name__ == '__main__':
    transformDocument = TransformDocument()
    srcLink = 'cwl_documents/workflowhub/raw_data/cwl_documents.json'
    destLink = 'cwl_documents/workflowhub/transformed_data/transformed_workflow_cwl_documents.json'
    documents = transformDocument.readJson(srcLink)
    transformedDocuments = transformDocument.transformDocuments(documents)
    transformDocument.saveTransformedDocuments(transformedDocuments, destLink, overWrite=True)
    