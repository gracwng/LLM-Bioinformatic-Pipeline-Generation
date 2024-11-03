'''
This is the main file for the RAG pipeline generation

1. Read in user query
2. Generate embeddings for the user query
3. Generate multiple queries to retrieve data for
4. Retrieve the top k documents using EnsembleRetriever
5. Do retrieval with contextual compression

'''
def main():
    userQuery = "Can you generate a CWL workflow for variant calling from whole genome sequencing data?"

if __name__ == '__main__':
    main()
    pass

