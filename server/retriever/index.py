'''
RAG Flow:
-> self query (transform user input into a string to look up sematically)
-> multi-query retriever (uses an LLM to generate multiple queries from original one and then fetch docs for each of them)

-> vectorstore (creates an embedding for each piece of text and can be used as a retriever)
-> bm25 (uses the BM25 algorithm to rank documents based on the user query)
-> ensemble (fetches documents from multiple retrievers and combines them)
-> contextual compression (extracts only the most relevant information from retrievered documents)
'''