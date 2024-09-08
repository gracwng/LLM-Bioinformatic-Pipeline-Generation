import os
import sys
import pymongo
from pymongo import MongoClient

from server.knowledge_base import DocumentLoader
from server.knowledge_base.load.config import configs
from server.knowledge_base.storage.storage import DocumentStorage
# client = pymongo.MongoClient("mongodb+srv://granx:CzhklAsvIcilxtxV@dev.rm7ss.mongodb.net/")

'''
Load documents from github, workflowhub, other sources
Parse & transform documents so they fit the MongoDB db schema
Store documents into MongoDB
'''

def main(configs):

    ''' Load documents from github, workflowhub, other sources'''
    docLoader = DocumentLoader('github')

    documents = docLoader.getDocuments(configs)

    ''' Transform documents to fit MongoDB db schema'''

    '''Store transformed documents into CSV file'''
    docStorer = DocumentStorage('github')
    docStorer.storeRawDocumentsInCSV(documents)

    '''Store transformed documents into MongoDB'''

if __name__ == '__main__':
    main(configs)