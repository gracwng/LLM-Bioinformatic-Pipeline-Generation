from server.knowledge_base import DocumentLoader
from server.knowledge_base.load.config import raw_cwl_files_config, raw_workflowhub_cwl_files_config
from server.knowledge_base.storage.config import mongodb_raw_cwl_files_config
from server.knowledge_base.storage.document_storing import DocumentStorage

'''
Load documents from github, workflowhub, other sources
Parse & transform documents so they fit the MongoDB db schema
Store documents into MongoDB
'''

def main(raw_cwl_files_config, mongodb_raw_cwl_files_config):

    ''' Load documents from github, workflowhub, other sources'''
    docLoader = DocumentLoader('github')

    documents = docLoader.getDocuments(raw_cwl_files_config)

    ''' Transform documents to fit MongoDB db schema'''

    '''Store documents into CSV file'''
    docStorer = DocumentStorage('github')
    # docStorer.storeRawDocumentsInCSV(documents)
    docStorer.storeRawDocumentsInJSON(documents)
    # docStorer.storeDocumentsInMongoDB(documents, mongodb_raw_cwl_files_config)
    '''Store transformed documents into MongoDB'''
    
if __name__ == '__main__':
    # main(raw_cwl_files_config, mongodb_raw_cwl_files_config)
    main(raw_workflowhub_cwl_files_config, mongodb_raw_cwl_files_config)