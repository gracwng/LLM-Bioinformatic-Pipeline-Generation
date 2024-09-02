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
class DocumentLoader:

    def __init__(self, loader) -> None: 
        # Check that loader is a valid document loader, if provided
        if not issubclass(loader, BaseLoader):
            raise TypeError("loader must be a subclass of DocumentLoader")
        self.loader = loader

    def getDocuments (self):
