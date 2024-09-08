import pymongo
from pymongo import MongoClient

from server.knowledge_base import DocumentLoader

from server.knowledge_base.load.config import configs
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
    print(documents[0].page_content)
    print(documents[0].metadata)

    ''' Transform documents to fit MongoDB db schema'''

    '''Store transformed documents into MongoDB'''

if __name__ == '__main__':
    main(configs)