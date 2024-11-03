import os
from dotenv import load_dotenv
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
import json
from bson import json_util
'''
This file contains the vector store retriever functions
Idea: convert the page content and description embedding vector store into a retriever
'''


load_dotenv()  # This line is crucial
# Connect to your Atlas deployment
uri = os.environ.get('MONGODB_URI')
# initialize MongoDB python client
client = MongoClient(uri)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
DB_NAME = "LLM-Bioinformatic-Pipeline-Generation"
COLLECTION_NAME = "Cleaned-CWL-Files"
MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

def vectorStoreAsRetriever(embedding_key, text_key, search_type, k, fetch_k, lambda_mult, relevance_score_fn, ATLAS_VECTOR_SEARCH_INDEX_NAME):

    try:
        vector_store = MongoDBAtlasVectorSearch(
            collection=MONGODB_COLLECTION,
            embedding=embeddings,
            index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
            embedding_key=embedding_key,
            text_key=text_key,
            relevance_score_fn=relevance_score_fn,
        )
    except Exception as e:
        print(f"Error initializing vector store: {e}")

    retriever = vector_store.as_retriever(
        search_type = search_type, # Defines the type of search that the Retriever should perform. Can be “similarity” (default), “mmr”, or “similarity_score_threshold”.
        search_kwargs={"k": k, "fetch_k": fetch_k, "lambda_mult": lambda_mult},
    )

    return retriever

def getRetrievers():
    search_type = "mmr"
    k = 5
    fetch_k = 10
    lambda_mult = 0.5
    relevance_score_fn="cosine"
    vector_description_index = "vector_description_index"
    vector_page_content_index = "vector_page_content_index"
    description_embedding_key="description_embedding"
    description_text_key= "description"
    descriptionRetriever = vectorStoreAsRetriever(description_embedding_key, description_text_key, search_type, k, fetch_k, lambda_mult, relevance_score_fn, vector_description_index)
    # pageContentRetriever = vectorStoreAsRetriever(search_type, k, fetch_k, lambda_mult, relevance_score_fn, vector_page_content_index)
    return descriptionRetriever
# pageContentRetriever
    pass

def main():
    userQuery = "Can you generate a CWL workflow for variant calling from whole genome sequencing data?"
    descriptionRetriever = getRetrievers()
    retrievedDocs = descriptionRetriever.invoke(userQuery, k = 2)
    print(len(retrievedDocs))
    print(retrievedDocs[0].page_content)

    

if __name__ == '__main__':
    main()
    pass