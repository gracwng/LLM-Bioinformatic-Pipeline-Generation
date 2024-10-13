#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from langchain_together import ChatTogether
load_dotenv() # This loads the variables from .env

TOGETHER_API_KEY = os.environ.get('TOGETHER_API_KEY') # type: ignore

llm = ChatTogether(
    model="meta-llama/Llama-3-70b-chat-hf",
    temperature=0,
    max_tokens=60,
    timeout=None,
    max_retries=2,
    api_key=TOGETHER_API_KEY,  # if you prefer to pass api key in directly instaed of using env vars
)

