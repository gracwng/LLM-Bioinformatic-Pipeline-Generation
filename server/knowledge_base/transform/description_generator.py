import json
from server.knowledge_base.transform.document_transforming import TransformDocument
from server.llm_connector.llm import llm
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

# given a json file that contains json objects with information on CWL files (content, source, input, output, etc), generate the descriptions for each CWL file
def generateDescription():
    # Create a custom LLM chain for generating descriptions
    promptTemplate = """
    You are an expert in bioinformatics and workflow languages. Your task is to generate a concise description (2-3 sentences) for the following Common Workflow Language (CWL) file or code snippet. Include:
    1. The main purpose or function of the workflow/tool
    2. A brief description of how the workflow/tool works
    2. Key input and output data types
    3. Any notable features or operations performed

    CWL Content:
    {cwl_content}

    Concise Description:
    """
    
    # read in documents from the merged_cwl_documents.json file and convert them to Langchain documents
    transformDocument = TransformDocument()
    srcLink = 'cwl_documents/enhanced_documents.json'
    documents = transformDocument.readJson(srcLink)
    # documents = documents[:5]
    transformedDocuments = transformDocument.convertToLangchainDocuments(documents)

    # Create a prompt chain to generate descriptions for the CWL documents
    prompt = PromptTemplate(template = promptTemplate, input_variables=['cwl_content'])

    chain = (
        {"cwl_content": RunnablePassthrough()}
        | prompt
        | llm
    )

    enhancedDocuments = []

    for doc in transformedDocuments:
        description = chain.invoke({"cwl_content": doc.page_content}) # returns an AIMessage Object
        descriptionContent = description.content
        enhancedDocument = Document(page_content=doc.page_content, metadata={"description": descriptionContent, **doc.metadata})
        enhancedDocuments.append(enhancedDocument)

    # Create a list to store the formatted document data
    formatted_documents = []

    for doc in enhancedDocuments:
        formatted_doc = {
            "page_content": doc.page_content,
            "metadata": doc.metadata
        }
        formatted_documents.append(formatted_doc)

    # Write the formatted documents to a JSON file
    with open('enhanced_documents.json', 'w') as json_file:
        json.dump(formatted_documents, json_file, indent=2)

    print("Enhanced documents have been saved to 'enhanced_documents.json'")

if __name__ == '__main__':
    # generateDescription()
    pass