import os
import yaml
from cwltool import *
from cwl_utils.parser import load_document, save
from schema_salad.exceptions import ValidationException


def isValidCWL(content):
    try:
        yaml.safe_load(content)
        return True
    except yaml.YAMLError:
        return False
    
def validateCWL(requirements, steps):
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

def processDocument(doc):
    doc_data = {
        'path': doc.metadata.get('path', ''),
        'sha': doc.metadata.get('sha', ''),
        'source': doc.metadata.get('source', ''),
        'content': doc.page_content,
        'is_valid_cwl': isValidCWL(doc.page_content)
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
    return doc_data
