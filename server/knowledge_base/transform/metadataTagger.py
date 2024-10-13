from server.llm_connector.llm import llm
from langchain_community.document_transformers.openai_functions import (
    create_metadata_tagger,
)
schema = {
    "properties": {
        "movie_title": {"type": "string"},
        "critic": {"type": "string"},
        "tone": {"type": "string", "enum": ["positive", "negative"]},
        "rating": {
            "type": "integer",
            "description": "The number of stars the critic rated the movie",
        },
    },
    "required": ["movie_title", "critic", "tone"],
}

# Must be an OpenAI model that supports functions (HELP)

document_transformer = create_metadata_tagger(metadata_schema=schema, llm=llm)
