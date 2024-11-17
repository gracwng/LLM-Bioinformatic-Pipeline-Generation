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

from server.llm_connector import llm
from server.parser.parser import create_cwl_file, parse_llm_output
from server.retriever.retriever_builder import RetrieverBuilder

def main():
    # Define a system prompt that tells the model how to use the retrieved context
    system_prompt = """You are an expert in Common Workflow Language (CWL) with extensive knowledge of bioinformatics tools and workflows. Your primary goal is to generate accurate, well-structured, and comprehensive CWL files based on user queries and provided context.
        Use the following retrieved context to inform your CWL file generation:
        {context}

        When creating CWL files:
        1. Always use the most recent CWL version unless specifically requested otherwise.
        2. Include detailed descriptions for the tool/workflow and each input/output.
        3. Specify appropriate types for inputs and outputs, including file formats where relevant.
        4. Use best practices for naming conventions and structure.
        5. Include relevant requirements (e.g., DockerRequirement, ResourceRequirement, SystemRequirement) and hints.
        6. Ensure command line bindings are correct and follow the tool's documentation.
        7. Add relevant metadata such as labels and software versions.

        If the context doesn't provide enough information for a complete CWL file, use your expert knowledge to fill in the gaps. If critical information is missing, state what additional details would be needed.

        Provide the complete CWL file in YAML format, enclosed in triple backticks (```yaml). After the CWL file, briefly explain any assumptions or decisions you made during the creation process.

        Remember, your goal is to create a CWL file that is not only syntactically correct but also practical and ready for use in a bioinformatics pipeline. Please be thorough and detailed in your response."""
        
    # Define a question
    # userQuery = "Can you generate a CWL workflow for variant calling from whole genome sequencing data?"
    # userQuery = "help me generate a Common Workflow Language (CWL) tool implements the Genome Analysis Toolkit (GATK) function \"ApplyBQSR,\" which is used for base quality score recalibration in genomic data processing. It takes as input a BAM file, a base recalibration file, and various optional parameters, and produces a recalibrated BAM file along with optional index and VCF outputs. Notable features include support for multiple command-line options for fine-tuning the recalibration process, such as output indexing, read filtering, and quality score preservation."
    userQuery = "help me write a cwl file that fufills this: The VDJtools Calc Spectratype workflow is designed to analyze immune repertoire sequencing data by calculating the spectratype, which is a histogram of read counts based on CDR3 nucleotide length. It takes as input a VDJ file along with optional parameters for unweighted and amino acid analysis, and produces several output files, including spectratype data in various formats (e.g., .insert.wt.txt, .ndn.wt.txt, .aa.wt.txt, .nt.wt.txt). Notably, this tool leverages Docker for consistent execution and requires a minimum of 2 CPU cores and 3814 MB of RAM"    # Retrieve relevant documents
    retriever = getRetrievers()
    docs = retriever.invoke(userQuery)

    # Combine the documents into a single string
    format_docs = "\n\n".join(doc.page_content for doc in docs)

    # Populate the system prompt with the retrieved context
    system_prompt_fmt = system_prompt.format(context=format_docs)

    # Create a model
    model = ChatOpenAI(model="gpt-4o", temperature=0) 

    # Generate a response
    response = model.invoke([SystemMessage(content=system_prompt_fmt),
                            HumanMessage(content=userQuery)])
    # print(response)
    extracted_yaml = parse_llm_output(response)
    if extracted_yaml:
        # Create the CWL file
        filename = create_cwl_file(extracted_yaml)
        print(f"CWL file created: {filename}")
    else:
        print("Failed to extract YAML content from LLM output")


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
    # return ensemble
    return compressor

if __name__ == "__main__":
    main()