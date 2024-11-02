'''This class is a client to connect to MongoDB Atlas'''

from pymongo import MongoClient

class AtlasClient:
    def __init__(self, atlasUri, dbName):
        self.mongodbClient = MongoClient(atlasUri)
        self.database = self.mongodbClient[dbName]

    # A quick way to test if we can connect to Atlas instance
    def ping(self):
        self.mongodbClient.admin.command('ping')

    def getCollection(self, collectionName):
        collection = self.database[collectionName]
        return collection

    def find(self, collectionName, filter={}, limit=0):
        collection = self.database[collectionName]
        items = list(collection.find(filter=filter, limit=limit))
        return items
   
    # Add a document to a collection into MongoDB Atlas
    def addDocument(self, collectionName, document):
        collection = self.database[collectionName]
        collection.insert_one(document)
        print(f"Document added to {collectionName}")
    
    # Add multiple documents to a collection into MongoDB Atlas
    def addDocuments(self, collectionName, documents):
        collection = self.database[collectionName]
        collection.insert_many(documents)
        print(f"Documents added to {collectionName}")
