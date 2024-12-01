'''
RAG Workflow:
-> ✔ multi-query retriever (uses an LLM to generate multiple queries from original one and then fetch docs for each of them)
-> ✔ vectorstore (creates an embedding for each piece of text and can be used as a retriever)
-> ✔ bm25 (uses the BM25 algorithm to rank documents based on the user query)
-> ✔ ensemble (fetches documents from multiple retrievers and combines them)
-> ✔ contextual compression (extracts only the most relevant information from retrievered documents)
'''

import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from server.llm_connector import llm
from server.parser.CWLWorkflow import CWLDocument
from server.parser.parser import create_cwl_file, parse
from server.retriever.retriever_builder import RetrieverBuilder

from langchain.output_parsers import YamlOutputParser

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
error_log_file = "error_log.txt"
result_file = "parsed_results.yaml"


def save_result(filename, content):
    with open(filename, "a") as f:
        f.write(content + "\n\n")


def getRetrievers():
    retrievers = RetrieverBuilder()
    retrievers.addBM25Retriever()
    
    vector_store_desc = retrievers.loadVectorStore("vector_description_index", "description_embedding", "description")
    vector_store_content = retrievers.loadVectorStore("vector_page_content_index", "page_content_embedding", "page_content")
    
    retrievers.addVectorStoreAsRetriever(vector_store_desc, "mmr", 5, 10, 0.5)
    retrievers.addVectorStoreAsRetriever(vector_store_content, "mmr", 5, 10, 0.5)
    
    # Add MultiQueryRetriever using one of the vector store retrievers
    # retrievers.addMultiQueryRetriever(vector_store_desc)
    # retrievers.addMultiQueryRetriever(vector_store_content)
    
    ensemble = retrievers.createEnsembleRetriever()
    # compressor = retrievers.getCompressionRetriever(ensemble)
    return ensemble
    # return compressor



def main():
    try:
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

        # Set up a parser for CWL documents
        parser = YamlOutputParser(pydantic_object=CWLDocument)

        # Create a model
        model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0) 

        # Generate a response
        raw_response = model.invoke([SystemMessage(content=system_prompt_fmt),
                                HumanMessage(content=userQuery)])
        raw_response_content = raw_response.content

        parsing_system_prompt = """ 
            You are an expert in Common Workflow Language (CWL) and technical documentation. Your task is to extract, format, and explain a CWL file from the given content. Follow these steps:

            1. Extract the CWL YAML content from within the triple backticks.

            2. Format the extracted YAML for maximum readability, ensuring proper indentation and spacing.

            3. After the formatted YAML, provide a structured explanation of the CWL file, including:
            a. A brief overview of the workflow's purpose
            b. Explanation of key components (inputs, outputs, requirements, etc.)
            c. Any notable features or assumptions made in the CWL file

            4. Organize your response as follows:
            - Title: "[Workflow Name] CWL File"
            - Section 1: "CWL File Contents"
                (Include the formatted YAML here)
            - Section 2: "Explanation"
                (Include your structured explanation here)

            Ensure your explanation is clear, concise, and accessible to users with basic knowledge of CWL and bioinformatics workflows.
        """
    
        raw_response_content = "Based on the provided context, here is a CWL file for the VDJtools Calc Spectratype workflow. This file includes the necessary inputs, outputs, and requirements for running the tool using Docker.\n\n```yaml\ncwlVersion: v1.2\nclass: CommandLineTool\n\nhints:\n  ResourceRequirement:\n    ramMin: 3814\n    coresMin: 2\n  DockerRequirement:\n    dockerPull: yyasumizu/vdjtools\n\nbaseCommand: [\"vdjtools\", \"CalcSpectratype\"]\n\ndoc: |\n  The VDJtools Calc Spectratype workflow is designed to analyze immune repertoire sequencing data\n  by calculating the spectratype, which is a histogram of read counts based on CDR3 nucleotide length.\n  It takes as input a VDJ file along with optional parameters for unweighted and amino acid analysis,\n  and produces several output files, including spectratype data in various formats.\n\ninputs:\n  vdj_file:\n    type: File\n    inputBinding:\n      position: 1\n    label: \"VDJ File\"\n    doc: \"The input VDJ file containing immune repertoire sequencing data.\"\n\n  unweighted:\n    type: boolean?\n    inputBinding:\n      position: 2\n      prefix: \"--unweighted\"\n    label: \"Unweighted Analysis\"\n    doc: \"Optional parameter to perform unweighted analysis.\"\n\n  amino_acid:\n    type: boolean?\n    inputBinding:\n      position: 3\n      prefix: \"--amino-acid\"\n    label: \"Amino Acid Analysis\"\n    doc: \"Optional parameter to perform amino acid analysis.\"\n\noutputs:\n  insert_wt_txt:\n    type: File\n    outputBinding:\n      glob: \"*.insert.wt.txt\"\n    label: \"Insert Weighted Spectratype\"\n    doc: \"Output file containing insert weighted spectratype data.\"\n\n  ndn_wt_txt:\n    type: File\n    outputBinding:\n      glob: \"*.ndn.wt.txt\"\n    label: \"NDN Weighted Spectratype\"\n    doc: \"Output file containing NDN weighted spectratype data.\"\n\n  aa_wt_txt:\n    type: File\n    outputBinding:\n      glob: \"*.aa.wt.txt\"\n    label: \"Amino Acid Weighted Spectratype\"\n    doc: \"Output file containing amino acid weighted spectratype data.\"\n\n  nt_wt_txt:\n    type: File\n    outputBinding:\n      glob: \"*.nt.wt.txt\"\n    label: \"Nucleotide Weighted Spectratype\"\n    doc: \"Output file containing nucleotide weighted spectratype data.\"\n\nrequirements:\n  InlineJavascriptRequirement: {}\n\n```\n\n### Explanation and Assumptions:\n\n1. **CWL Version**: The file uses CWL version 1.2, which is the most recent stable version as of the training data.\n\n2. **Docker Requirement**: The tool is executed within a Docker container (`yyasumizu/vdjtools`) to ensure consistent execution across different environments.\n\n3. **Resource Requirements**: The tool requires a minimum of 2 CPU cores and 3814 MB of RAM, as specified in the context.\n\n4. **Inputs**:\n   - `vdj_file`: The primary input file containing the immune repertoire sequencing data.\n   - `unweighted` and `amino_acid`: Optional boolean parameters to control the type of analysis performed.\n\n5. **Outputs**: The workflow produces several output files in different formats, each representing a different aspect of the spectratype analysis.\n\n6. **Command Line Bindings**: The `baseCommand` and `inputBinding` sections are structured to correctly pass the inputs to the command line tool.\n\n7. **Assumptions**: It is assumed that the output files will have specific extensions (`.insert.wt.txt`, `.ndn.wt.txt`, etc.) based on the context provided. If the actual tool behavior differs, these patterns may need adjustment."

        parsing_query = raw_response_content
        # parsing_raw_response = model.invoke([SystemMessage(content=parsing_system_prompt),
        #                         HumanMessage(content=parsing_query)])
        # # Parse the YAML content
        # parsed_cwl = parser.parse(parsing_raw_response.content)
        # print(parsed_cwl)
        # stored_filename = store_response(parsing_raw_response)
        # print(f"Response stored in: {stored_filename}")
        # Generate a response
        try:
            raw_response = model.invoke([SystemMessage(content=system_prompt_fmt), HumanMessage(content=userQuery)])
            raw_response_content = raw_response.content
        except Exception as e:
            logging.error(f"Error during generation: {e}")
            with open(error_log_file, "a") as err_file:
                err_file.write(f"Error during generation: {e}\n")
            return  # Skip to the next iteration or exit

        # Define parsing system prompt

        # Parse response
        try:
            parsing_query = raw_response_content
            parsing_raw_response = model.invoke([SystemMessage(content=parsing_system_prompt), HumanMessage(content=parsing_query)])
            parsed_cwl = parser.parse(parsing_raw_response.content)
            save_result(result_file, parsing_raw_response.content)
        except Exception as e:
            logging.error(f"Error during parsing: {e}")
            with open(error_log_file, "a") as err_file:
                err_file.write(f"Error during parsing: {e}\n")
            return  # Skip to the next iteration or exit

        # Print the parsed CWL
        print(parsed_cwl)

    except Exception as e:
        logging.critical(f"Unexpected error: {e}", exc_info=True)
        with open(error_log_file, "a") as err_file:
            err_file.write(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()



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