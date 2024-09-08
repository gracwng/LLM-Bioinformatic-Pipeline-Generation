import os
import yaml
from yaml.loader import SafeLoader

def processDocument(doc):
    doc_data = {
        'path': doc.metadata.get('path', ''),
        'sha': doc.metadata.get('sha', ''),
        'source': doc.metadata.get('source', ''),
        'content': doc.page_content,
    }

    try:
        # Parse the YAML content
        cwl_content = yaml.load(doc.page_content, Loader=SafeLoader)

        # List of all possible CWL fields
        cwl_fields = [
            'class', 'id', 'inputs', 'outputs', 'hints', 'cwlVersion', 'baseCommand',
            'arguments', '$namespaces', '$schemas', 'requirements', 'doc', 'stdout',
            's:name', 's:license', 's:creator', 'label', 's:downloadUrl', 's:codeRepository',
            's:about', 'stderr', 's:alternateName', 's:author', 'successCodes',
            'expression', 's:isPartOf', 's:mainEntity', 'steps'
        ]

        # Set all fields to None initially
        for field in cwl_fields:
            doc_data[f'cwl_{field}'] = None

        # Update fields that are present in the CWL file
        for key, value in cwl_content.items():
            if key == 'requirements' and not isinstance(value, dict):
                doc_data['cwl_requirements_error'] = 'Requirements should be an object, not a list'
            elif key == 'steps':
                doc_data['cwl_steps'] = {}
                for step_name, step_data in value.items():
                    doc_data['cwl_steps'][step_name] = step_data
                    if 'run' in step_data:
                        doc_data['cwl_steps'][step_name]['run'] = str(step_data['run'])
            else:
                # Convert value to string for consistency
                doc_data[f'cwl_{key}'] = str(value)

    except yaml.YAMLError as e:
        doc_data['yaml_error'] = str(e)
    except Exception as e:
        doc_data['error'] = str(e)

    return doc_data
