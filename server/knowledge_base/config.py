from getpass import getpass
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the environment variable
GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')

# Use GITHUB_PERSONAL_ACCESS_TOKEN 
ACCESS_TOKEN = getpass(GITHUB_PERSONAL_ACCESS_TOKEN)