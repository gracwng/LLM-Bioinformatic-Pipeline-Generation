from getpass import getpass
from dotenv import load_dotenv
import os
from server.knowledge_base import common_workflow_library_config, datirium_workflow_config, ncbi_cwl_ngs_workflow_config

# Load environment variables from .env file
load_dotenv()

# Access the environment variable
GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
# Use GITHUB_PERSONAL_ACCESS_TOKEN 
ACCESS_TOKEN = getpass(GITHUB_PERSONAL_ACCESS_TOKEN)

# configuration for github database repositories 
# configs = [common_workflow_library_config, datirium_workflow_config, ncbi_cwl_ngs_workflow_config]
configs = [common_workflow_library_config]