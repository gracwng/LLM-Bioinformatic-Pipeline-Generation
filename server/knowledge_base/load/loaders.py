from langchain_community.document_loaders import GithubFileLoader

def gitHubLoader(config):
    # Initialize the loader
    loader = GithubFileLoader(
        repo=config['repo'],
        branch=config['branch'], 
        access_token=config['access_token'],
        github_api_url=config['github_api_url'],
        file_filter=lambda file_path: file_path.endswith(config['file_filter']),
    )
    # Attempt to load documents and print any errors
    try:
        documents = loader.load()
        print("Documents loaded successfully:", documents)
        return documents
    except Exception as e:
        print("Error loading documents:", e)
        return None