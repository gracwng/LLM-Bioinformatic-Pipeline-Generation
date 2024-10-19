import os
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env

mongodb_raw_cwl_files_config = {
    'MONGODB_URI': os.environ.get('MONGODB_URI'),
    'DB_NAME': 'LLM-Bioinformatic-Pipeline-Generation',
    'COLLECTION_NAME': 'Raw-CWL-Files'
}

mongodb_clean_cwl_files_config = {
    'MONGODB_URI': os.environ.get('MONGODB_URI'),
    'DB_NAME': 'LLM-Bioinformatic-Pipeline-Generation',
    'COLLECTION_NAME': 'Cleaned-CWL-Files'
}
