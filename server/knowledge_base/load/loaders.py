from langchain_community.document_loaders import GithubFileLoader

def gitHubLoader(config):
    loader = GithubFileLoader(
        repo = config['repo'],
        branch = config['branch'], 
        access_token = config['access_token'],
        github_api_url = config['github_api_url'],
        file_filter = lambda file_path: file_path.endswith(config['file_filter']),
)
    documents = loader.load()