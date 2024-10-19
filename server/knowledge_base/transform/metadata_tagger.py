import json
from server.knowledge_base.transform.document_transforming import TransformDocument
from server.llm_connector.llm import llm
from langchain_community.document_transformers.openai_functions import (
    create_metadata_tagger,
)
schema = {
    "properties": {
        "description": {
            "type": "string",
            "description": "You are an expert in bioinformatics and workflow languages. Your task is to generate concise descriptions for data points containing Common Workflow Language (CWL) files or code.",
        },
    },
    "required": ["movie_title", "critic", "tone"],
}

document_transformer = create_metadata_tagger(metadata_schema=schema, llm=llm)
transformDocument = TransformDocument()
srcLink = 'cwl_documents/merged_cwl_documents.json'
documents = transformDocument.readJson(srcLink)
documents = documents[:5]
transformedDocuments = transformDocument.convertToLangchainDocuments(documents)

enhancedDocuments = document_transformer.transform_documents(transformedDocuments)
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