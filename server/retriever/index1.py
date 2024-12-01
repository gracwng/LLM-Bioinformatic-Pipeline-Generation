'''
RAG Workflow:
-> ✔ multi-query retriever (uses an LLM to generate multiple queries from original one and then fetch docs for each of them)
-> ✔ vectorstore (creates an embedding for each piece of text and can be used as a retriever)
-> ✔ bm25 (uses the BM25 algorithm to rank documents based on the user query)
-> ✔ ensemble (fetches documents from multiple retrievers and combines them)
-> ✔ contextual compression (extracts only the most relevant information from retrievered documents)
'''
# this file doesn't work because the API contexr length was exceeded
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from server.llm_connector import llm
from server.parser.parser import create_cwl_file, parse
from server.retriever.retriever_builder import RetrieverBuilder

def main():
    # Define a system prompt that tells the model how to use the retrieved context
    system_prompt = """You are an expert in Common Workflow Language (CWL) with extensive knowledge of bioinformatics tools and workflows. Your primary goal is to generate accurate, well-structured, and comprehensive CWL files based on user queries and provided context.
        Use the following retrieved context to inform your CWL file generation:
        {context}

       """
    # Define a question
    userQuery = "Can you generate a CWL workflow for variant calling from whole genome sequencing data?"
    # userQuery = "help me generate a Common Workflow Language (CWL) tool implements the Genome Analysis Toolkit (GATK) function \"ApplyBQSR,\" which is used for base quality score recalibration in genomic data processing. It takes as input a BAM file, a base recalibration file, and various optional parameters, and produces a recalibrated BAM file along with optional index and VCF outputs. Notable features include support for multiple command-line options for fine-tuning the recalibration process, such as output indexing, read filtering, and quality score preservation."
    # userQuery = "help me write a cwl file that fufills this: The VDJtools Calc Spectratype workflow is designed to analyze immune repertoire sequencing data by calculating the spectratype, which is a histogram of read counts based on CDR3 nucleotide length. It takes as input a VDJ file along with optional parameters for unweighted and amino acid analysis, and produces several output files, including spectratype data in various formats (e.g., .insert.wt.txt, .ndn.wt.txt, .aa.wt.txt, .nt.wt.txt). Notably, this tool leverages Docker for consistent execution and requires a minimum of 2 CPU cores and 3814 MB of RAM"    # Retrieve relevant documents
    retriever = getRetrievers()

    # Create a model
    # model = ChatOpenAI(model="gpt-4o", temperature=0) 
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0) 

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{{input}}"),
            
        ]
    )
    # Set up the chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    response = chain.invoke(userQuery)

    stored_filename = store_response(response)
    print(f"Response stored in: {stored_filename}")

    # pass
def getRetrievers():
    retrievers = RetrieverBuilder()
    retrievers.addBM25Retriever()
    
    # vector_store_desc = retrievers.loadVectorStore("vector_description_index", "description_embedding", "description")
    vector_store_content = retrievers.loadVectorStore("vector_page_content_index", "page_content_embedding", "page_content")
    
    # retrievers.addVectorStoreAsRetriever(vector_store_desc, "mmr", 5, 10, 0.5)
    retrievers.addVectorStoreAsRetriever(vector_store_content, "mmr", 5, 10, 0.5)
    
    # Add MultiQueryRetriever using one of the vector store retrievers
    # retrievers.addMultiQueryRetriever(vector_store_desc)
    # retrievers.addMultiQueryRetriever(vector_store_content)
    
    # ensemble = retrievers.createEnsembleRetriever()
    return retrievers.retrievers[0]
    # compressor = retrievers.getCompressionRetriever(ensemble)
    return ensemble
    # return compressor

import json
from datetime import datetime
from langchain.schema import AIMessage

def store_response(response):
    # Convert the response to a dictionary
    if isinstance(response, AIMessage):
        response_dict = {
            "content": response.content,
            "additional_kwargs": response.additional_kwargs,
            "type": "AIMessage"
        }
    else:
        response_dict = {
            "content": str(response),
            "type": str(type(response))
        }

    # Add timestamp
    response_dict["timestamp"] = datetime.now().isoformat()

    # Create a filename with timestamp
    filename = f"model_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Store the response in a JSON file
    with open(filename, 'w') as json_file:
        json.dump(response_dict, json_file, indent=4)

    return filename

if __name__ == "__main__":
    main()
    