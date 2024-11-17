import re
import yaml
from datetime import datetime
from langchain.schema import AIMessage

import yaml
from ruamel.yaml import YAML
import re
from datetime import datetime

def create_cwl_file(yaml_content):
    # First, let's validate that we have valid CWL content
    if not yaml_content.strip().startswith("cwlVersion:"):
        raise ValueError("The provided content does not appear to be a valid CWL file.")

    # Use ruamel.yaml for parsing, as it's more lenient with CWL-specific syntax
    yaml = YAML()
    
    try:
        # Parse the YAML content
        cwl_dict = yaml.load(yaml_content)
        
        # Create a unique filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cwl_file_{timestamp}.cwl"
        
        # Write the CWL content to a file
        with open(filename, 'w') as file:
            yaml.dump(cwl_dict, file)
        
        return filename
    except Exception as e:
        print(f"Error parsing or writing CWL file: {str(e)}")
        print("Raw YAML content:")
        print(yaml_content)
        return None
    
def create_cwl_file(yaml_content):
    # Convert the extracted YAML content into Python dictionary
    cwl_dict = yaml.safe_load(yaml_content)
    
    # Create a filename with a timestamp
    filename = f'variant_calling_workflow_{datetime.now().strftime("%Y%m%d_%H%M%S")}.cwl'
    
    # Write the YAML content to a file
    with open(filename, 'w') as file:
        yaml.dump(cwl_dict, file, default_flow_style=False)
    
    return filename
