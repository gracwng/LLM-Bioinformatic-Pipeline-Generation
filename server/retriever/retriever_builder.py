# this file creates a class that contains all the retrievers and the methods to use them
import os
from dotenv import load_dotenv
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders.mongodb import MongodbLoader
import nest_asyncio
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers import EnsembleRetriever
from langchain_core.prompts import PromptTemplate
from server.retriever.LineListOutputParser import LineListOutputParser
from server.llm_connector.llm import llm
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import OpenAIEmbeddings
from server.llm_connector.llm import llm
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain_community.document_transformers import EmbeddingsRedundantFilter

class RetrieverBuilder:
    def __init__(self):  
        nest_asyncio.apply()
        load_dotenv()
        self.retrievers = []
        self.docs = None
        self.ensembleRetriever = None
        self.llm = llm

        self.client = MongoClient(os.environ['MONGODB_URI'])
        self.db = self.client[os.environ['MONGODB_DB']]
        self.collection = self.db[os.environ['MONGODB_COLL']]
    
    # load documents from database for the BM25 retriever
    def loadDocs(self): 
        loader = MongodbLoader(
            connection_string=os.environ['MONGODB_URI'],
            db_name=os.environ['MONGODB_DB'],
            collection_name=os.environ['MONGODB_COLL'],
            filter_criteria={},
            field_names=["page_content", "description", "source", "class", "inputs", "outputs", "baseCommand", "arguments", "requirements", "hints", "cwlVersion"]
        )
        self.docs = loader.load()

    # load vector store from database
    def loadVectorStore(self, index_name, embedding_key, text_key, relevance_score_fn = "cosine"):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        try:
            vector_store = MongoDBAtlasVectorSearch(
                collection=self.collection,
                embedding=embeddings,
                index_name=index_name,
                embedding_key=embedding_key,
                text_key=text_key,
                relevance_score_fn=relevance_score_fn,
            )
            return vector_store
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            return None

    def addVectorStoreAsRetriever(self, vector, search_type, k, fetch_k, lambda_mult):
        try:
            vector_store = vector
            if vector_store is None:
                print(f"Failed to initialize vector store for index: {vector}")
                return None
            retriever = vector_store.as_retriever(
                search_type=search_type,
                search_kwargs={"k": k, "fetch_k": fetch_k, "lambda_mult": lambda_mult},
            )
            self.retrievers.append(retriever)
            return retriever
        except Exception as e:
            print(f"Error adding vector store as retriever: {e}")
            return None

    def addBM25Retriever(self):
        if self.docs is None:
            self.loadDocs()
        if self.docs is None: 
            raise Exception("Could not load docs")
        retriever = BM25Retriever.from_documents(self.docs)
        self.retrievers.append(retriever)
        return retriever
    
    def addMultiQueryRetriever(self, vector):
        output_parser = LineListOutputParser()


        QUERY_PROMPT = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI language model assistant. Your task is to generate five 
            different versions of the given user question to retrieve relevant documents from a vector 
            database. By generating multiple perspectives on the user question, your goal is to help
            the user overcome some of the limitations of the distance-based similarity search. 
            Provide these alternative questions separated by newlines.
            Original question: {question}""",
        )
        llm_chain = QUERY_PROMPT | llm | output_parser
        retriever = MultiQueryRetriever(
            retriever=vector.as_retriever(), llm_chain=llm_chain, parser_key="lines")
        self.retrievers.append(retriever)
        return retriever
    def createEnsembleRetriever(self):
        if self.retrievers is None:
            raise Exception("No retrievers to ensemble")
        weights =[1/len(self.retrievers)] * len(self.retrievers)
        self.ensembleRetriever = EnsembleRetriever(
            retrievers = self.retrievers,
            weights = weights)
        return self.ensembleRetriever
    
    # this method takes the results of the ensemble retriever and compresses them using a pipeline of compressors
    def getCompressionRetriever(self, retrievers): 
        embeddings = OpenAIEmbeddings()
        compressor = LLMChainExtractor.from_llm(llm) # iterates over the initially returned documents and extract from each only the content that is relevant to the query.
        _filter = LLMChainFilter.from_llm(llm) # uses an LLM chain to decide which of the initially retrieved documents to filter out and which ones to return, without manipulating the document contents.

        redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
        relevant_filter = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.76)
        pipeline_compressor = DocumentCompressorPipeline(
            transformers=[redundant_filter, relevant_filter, compressor, _filter]
        )
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=pipeline_compressor, base_retriever=retrievers
        )
        self.compression_retriever = compression_retriever
        return compression_retriever
    
    

def main():
    retrievers = RetrieverBuilder()
    retrievers.addBM25Retriever()
    
    vector_store_desc = retrievers.loadVectorStore("vector_description_index", "description_embedding", "description")
    vector_store_content = retrievers.loadVectorStore("vector_page_content_index", "page_content_embedding", "page_content")
    
    retrievers.addVectorStoreAsRetriever(vector_store_desc, "mmr", 5, 10, 0.5)
    retrievers.addVectorStoreAsRetriever(vector_store_content, "mmr", 5, 10, 0.5)
    
    # Add MultiQueryRetriever using one of the vector store retrievers
    retrievers.addMultiQueryRetriever(vector_store_desc)
    retrievers.addMultiQueryRetriever(vector_store_content)
    
    ensemble = retrievers.createEnsembleRetriever()
    compressor = retrievers.getCompressionRetriever(ensemble)

    result = compressor.invoke("Can you generate a CWL workflow for variant calling from whole genome sequencing data?")
    
    print((result))
    print(len(result))

if __name__ == "__main__":
    main()