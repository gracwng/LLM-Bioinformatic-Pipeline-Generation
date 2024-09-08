import sys
import os
# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pathlib import Path
from ruamel import yaml
from ruamel.yaml import YAML
import pymongo
from pymongo import MongoClient

from server.knowledge_base.load.document_loading import DocumentLoader
from server.knowledge_base.load.config import configs
from cwl_utils.parser import load_document, save

import pandas as pd
import pandas as pd
from cwl_utils.parser import load_document, save
from schema_salad.exceptions import ValidationException
import yaml

def is_valid_cwl(content):
    try:
        yaml.safe_load(content)
        return True
    except yaml.YAMLError:
        return False

def main(configs):
    docLoader = DocumentLoader('github')
    documents = docLoader.getDocuments(configs)

    csv_data = []
    for doc in documents:
        doc_data = {
            'path': doc.metadata.get('path', ''),
            'sha': doc.metadata.get('sha', ''),
            'source': doc.metadata.get('source', ''),
            'content': doc.page_content,
            'is_valid_cwl': is_valid_cwl(doc.page_content)
        }

        if doc_data['is_valid_cwl']:
            try:
                cwl_obj = load_document(doc.page_content)
                saved_obj = save(cwl_obj)

                for key, value in saved_obj.items():
                    if key == 'requirements' and not isinstance(value, dict):
                        doc_data['cwl_requirements_error'] = 'Requirements should be an object, not a list'
                    elif key == 'steps':
                        for step_name, step_data in value.items():
                            if 'run' in step_data:
                                run_value = step_data['run']
                                if isinstance(run_value, str) and not os.path.exists(run_value):
                                    doc_data[f'cwl_step_{step_name}_run_error'] = f"File not found: {run_value}"

                    doc_data[f'cwl_{key}'] = str(value)

            except ValidationException as e:
                doc_data['cwl_validation_error'] = str(e)
            except Exception as e:
                doc_data['cwl_error'] = str(e)
        
        csv_data.append(doc_data)

    df = pd.DataFrame(csv_data)
    csv_file_path = 'cwl_documents.csv'
    df.to_csv(csv_file_path, index=False)
    print(f"Documents saved to {csv_file_path}")

if __name__ == '__main__':
    main(configs)