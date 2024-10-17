import json
from server.knowledge_base.config import ACCESS_TOKEN

# data from github repositories
common_workflow_library_config = { # https://github.com/common-workflow-library/bio-cwl-tools
    'repo': 'common-workflow-library/bio-cwl-tools',
    'branch': 'release',
    'access_token': ACCESS_TOKEN,
    'github_api_url': 'https://api.github.com',
    'file_filter': '.cwl'
}

datirium_workflow_config = { # https://github.com/datirium/workflows 
    'repo': 'datirium/workflows',
    'branch': 'master',
    'access_token': ACCESS_TOKEN,
    'github_api_url': 'https://api.github.com',
    'file_filter': '.cwl'
}

ncbi_cwl_ngs_workflow_config = { # https://github.com/ncbi/cwl-ngs-workflows-cbb 
    'repo': 'ncbi/cwl-ngs-workflows-cbb',
    'branch': 'master',
    'access_token': ACCESS_TOKEN,
    'github_api_url': 'https://api.github.com',
    'file_filter': '.cwl'
}



# configuration for github database repositories 
raw_cwl_files_config = [common_workflow_library_config, datirium_workflow_config, ncbi_cwl_ngs_workflow_config]
# raw_cwl_files_config = [common_workflow_library_config]

# data that originally came from workflowhub: 
def readJson(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

raw_workflowhub_cwl_files_config = readJson('server/knowledge_base/load/workflow_github_configs.json')

# print(raw_workflowhub_cwl_files_config)