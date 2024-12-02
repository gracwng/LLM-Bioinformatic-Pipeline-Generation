#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from langchain_together import ChatTogether
from langchain_openai import ChatOpenAI


load_dotenv() # This loads the variables from .env

TOGETHER_API_KEY = os.environ.get('TOGETHER_API_KEY') # type: ignore
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

llm2 = ChatTogether(
    model="meta-llama/Llama-3-70b-chat-hf",
    temperature=0,
    max_tokens=60,
    timeout=None,
    max_retries=2,
    api_key=TOGETHER_API_KEY,  # if you prefer to pass api key in directly instaed of using env vars
)

llm3 = ChatOpenAI(
    model_name="gpt-4o-mini",
    api_key = OPENAI_API_KEY,
    temperature = 0, 
    )  

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    api_key = OPENAI_API_KEY,
    temperature = 0, 
    )  
print(llm.invoke("Hello how are you?"))
# llm.invoke("Hello how are you?")

