'''
Store data in MongoDB Atlas or other databases
'''

import os
import pandas as pd
import yaml
from cwltool import *
from cwl_utils.parser import load_document, save
from schema_salad.exceptions import ValidationException
# from cwltool.load_tool import load_document
# from cwltool.main import save
# from cwltool.errors import ValidationException

class DocumentStorage:

    def __init__(self, source: str) -> None: 
        self.source = source
        
    def isValidCWL(self, content):
        try:
            yaml.safe_load(content)
            return True
        except yaml.YAMLError:
            return False
        
    def validateCWL(self, requirements, steps):
        errors = {}
        
        # Validate requirements
        if requirements is not None and not isinstance(requirements, dict):
            errors['requirements'] = 'Requirements should be an object, not a list'
        
        # Validate steps
        step_errors = {}
        for step_name, step_data in steps.items():
            if 'run' in step_data:
                run_value = step_data['run']
                if isinstance(run_value, str) and not os.path.exists(run_value):
                    step_errors[f'step_{step_name}_run_error'] = f"File not found: {run_value}"
        
        if step_errors:
            errors['steps'] = step_errors
        
        return errors

    def processDocument(self, doc):
        doc_data = {
            'path': doc.metadata.get('path', ''),
            'sha': doc.metadata.get('sha', ''),
            'source': doc.metadata.get('source', ''),
            'content': doc.page_content,
            'is_valid_cwl': self.isValidCWL(doc.page_content)
        }

        if doc_data['is_valid_cwl']:
            try:
                cwl_obj = load_document(doc.page_content)
                saved_obj = save(cwl_obj)
                
                # Validate and collect CWL data
                validation_errors = self.validateCWL(saved_obj.get('requirements'), saved_obj.get('steps'))
                if validation_errors:
                    doc_data.update(validation_errors)
                
                # Store the CWL data
                for key, value in saved_obj.items():
                    doc_data[f'cwl_{key}'] = str(value)

            except ValidationException as e:
                doc_data['cwl_validation_error'] = str(e)
            except Exception as e:
                doc_data['cwl_error'] = str(e)
        
        return doc_data
    
    # main func for CSV
    def storeRawDocumentsInCSV(self, documents):
        if self.source == 'github':
            csv_data = [self.processDocument(doc) for doc in documents]
            
            df = pd.DataFrame(csv_data)
            csv_file_path = 'cwl_documents/cwl_documents.csv'
            df.to_csv(csv_file_path, index=False)
            print(f"Documents saved to {csv_file_path}")

    # Example usage
    # store_documents_in_csv(documents)
                