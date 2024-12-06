import os
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # This line is crucial

# Connect to your Atlas deployment
uri = os.environ.get('MONGODB_URI')

client = MongoClient(uri)

'''
This script is used to list the search indexes of a collection in a MongoDB database 
(just want to see if we correctly set up the indexes for the collection)
'''
async def run():
    try:

        database = client["LLM-Bioinformatic-Pipeline-Generation"]
        collection = database["Cleaned-CWL-Files"]

        # Get a list of the collection's search indexes and print them
        cursor = collection.list_search_indexes()
        for index in cursor:
            print(index)

 
    finally:
        client.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
