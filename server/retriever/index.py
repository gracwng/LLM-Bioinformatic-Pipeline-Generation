'''
RAG Workflow:
-> ✔ multi-query retriever (uses an LLM to generate multiple queries from original one and then fetch docs for each of them)

-> ✔ vectorstore (creates an embedding for each piece of text and can be used as a retriever)
-> ✔ bm25 (uses the BM25 algorithm to rank documents based on the user query)
-> ✔ ensemble (fetches documents from multiple retrievers and combines them)
-> ✔ contextual compression (extracts only the most relevant information from retrievered documents)
'''

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from server.retriever.retriever_builder import RetrieverBuilder

def main():
    # Define a system prompt that tells the model how to use the retrieved context
    system_prompt = """You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise.
    Context: {context}:"""
        
    # Define a question
    userQuery = "Can you generate a CWL workflow for variant calling from whole genome sequencing data?"

    # Retrieve relevant documents
    retriever = getRetrievers()
    docs = retriever.invoke(userQuery)

    # Combine the documents into a single string
    docs_text = "".join(d.page_content for d in docs)

    # Populate the system prompt with the retrieved context
    system_prompt_fmt = system_prompt.format(context=docs_text)

    # Create a model
    model = ChatOpenAI(model="gpt-4o", temperature=0) 

    # Generate a response
    response = model.invoke([SystemMessage(content=system_prompt_fmt),
                            HumanMessage(content=userQuery)])
    print(response)

    pass
def getRetrievers():
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
    return compressor

if __name__ == "__main__":
    main()