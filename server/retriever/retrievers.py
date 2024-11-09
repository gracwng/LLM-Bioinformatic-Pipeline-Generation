# this file creates a class that contains all the retrievers and the methods to use them

class Retrievers:
    def __init__(self, retrievers):
        self.retrievers = retrievers

    def invoke(self, user_query):
        results = []
        for retriever in self.retrievers:
            results.append(retriever.invoke(user_query))
        return results