'''
Transform data 
'''

''' Create Database Schema (defining our document structure for our DB)'''
from pymongo import MongoClient
import yaml
import os
from bson.objectid import ObjectId
import datetime

cwl_schema = {
    "_id": ObjectId,
    "title": str,
    "description": str,
    "raw": str,
    "embedding": object,  # This will be a list or numpy array, depending on your embedding
    "class": str,
    "doc": str,
    "codeSource": str,
    "steps": list,
    "inputs": list,
    "outputs": list,
    "requirements": list,
    "s3Location": {
        "bucketName": str,
        "key": str
    },
    "createdAt": datetime.datetime,
    "updatedAt": datetime.datetime
}

class TransformDocument:

    def transformDocument(self, document):
        pass
    def transformDocuments(self, documents):
        pass
