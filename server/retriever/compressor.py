from langchain_openai import OpenAIEmbeddings
from server.llm_connector.llm import llm
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain_community.document_transformers import EmbeddingsRedundantFilter
from server.retriever.retriever_builder import RetrieverBuilder

# Stringing compressors and document transformers together

embeddings = OpenAIEmbeddings()

compressor = LLMChainExtractor.from_llm(llm) # iterates over the initially returned documents and extract from each only the content that is relevant to the query.
_filter = LLMChainFilter.from_llm(llm) # uses an LLM chain to decide which of the initially retrieved documents to filter out and which ones to return, without manipulating the document contents.

redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
relevant_filter = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.76)
pipeline_compressor = DocumentCompressorPipeline(
    transformers=[redundant_filter, relevant_filter, compressor, _filter]
)

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
compression_retriever = ContextualCompressionRetriever(
    base_compressor=pipeline_compressor, base_retriever=ensemble
)
userQuery = "Can you generate a CWL workflow for variant calling from whole genome sequencing data?"

compressed_docs = compression_retriever.invoke(
    userQuery
)

print(len(compressed_docs))