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
