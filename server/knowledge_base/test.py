'''
db.Cleaned-CWL-Files.aggregate([
  {
    "$vectorSearch": {
      "index": "vector_description_index",
      "path": "metadata.description_embedding",
      "queryVector": [<array-of-numbers>],
      "numCandidates": <number-of-candidates>,
      "limit": <number-of-results>
    }
  }
])
'''
