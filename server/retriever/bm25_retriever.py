from langchain_community.retrievers import BM25Retriever

from langchain_core.documents import Document

import os
from dotenv import load_dotenv
from langchain_community.document_loaders.mongodb import MongodbLoader
import nest_asyncio

nest_asyncio.apply()
load_dotenv()
loader = MongodbLoader(
    connection_string=os.environ['MONGODB_URI'],
    db_name=os.environ['MONGODB_DB'],
    collection_name=os.environ['MONGODB_COLL'],
    filter_criteria={},
    field_names=["page_content", "description", "source", "class", "inputs", "outputs", "baseCommand", "arguments", "requirements", "hints", "cwlVersion"]
)

docs = loader.load()

retriever = BM25Retriever.from_documents(docs)
userQuery = "Can you generate a CWL workflow for variant calling from whole genome sequencing data?"

result = retriever.invoke(userQuery)
print(result)