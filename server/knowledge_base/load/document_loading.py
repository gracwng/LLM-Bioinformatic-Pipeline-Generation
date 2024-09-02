'''
Provide functions for fetching and loading documents from different database sources

Algorithm:
Given a github repository, go through each folder and extract files that have the type .cwl
Preprocess them (attach source e.g: github URL)
Upload to S3
'''
from langchain_community.document_loaders import GithubFileLoader
from langchain.document_loaders.base import BaseLoader
from server.knowledge_base.config import ACCESS_TOKEN
from server.knowledge_base.load.loaders import gitHubLoader

class DocumentLoader:

    def __init__(self, source) -> None: 
        self.source = source
    
    def getDocuments(self, config):
        if self.source == 'github':
            loader = gitHubLoader(config)
        if loader:
            return loader
