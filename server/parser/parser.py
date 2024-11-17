import re
import yaml
from datetime import datetime
from langchain.schema import AIMessage
from ruamel.yaml import YAML
from cwltool.load_tool import load_tool

CWL_TEMPLATE = """
#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
label: {label}
doc: |
  {doc}

inputs:
{inputs}

outputs:
{outputs}

steps:
{steps}
"""

def extract_info(generated_code):
    label = re.search(r'label:\s*(.*)', generated_code)
    doc = re.search(r'doc:\s*\|(.*?)(?=\n\w)', generated_code, re.DOTALL)
    inputs = re.search(r'inputs:(.*?)(?=\noutputs:)', generated_code, re.DOTALL)
    outputs = re.search(r'outputs:(.*?)(?=\nsteps:)', generated_code, re.DOTALL)
    steps = re.search(r'steps:(.*)', generated_code, re.DOTALL)

    return {
        'label': label.group(1) if label else '',
        'doc': doc.group(1).strip() if doc else '',
        'inputs': inputs.group(1).strip() if inputs else '',
        'outputs': outputs.group(1).strip() if outputs else '',
        'steps': steps.group(1).strip() if steps else ''
    }

def generate_cwl(generated_code):
    info = extract_info(generated_code)
    
    cwl_content = CWL_TEMPLATE.format(
        label=info['label'],
        doc=info['doc'],
        inputs=info['inputs'],
        outputs=info['outputs'],
        steps=info['steps']
    )

    return cwl_content

def validate_cwl(cwl_content):
    try:
        load_tool(cwl_content)
        return True
    except Exception as e:
        print(f"CWL validation error: {str(e)}")
        return False

def create_cwl_file(cwl_content):
    if not cwl_content.strip().startswith("cwlVersion:"):
        raise ValueError("The provided content does not appear to be a valid CWL file.")

    yaml = YAML()
    
    try:
        cwl_dict = yaml.load(cwl_content)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cwl_file_{timestamp}.cwl"
        
        with open(filename, 'w') as file:
            yaml.dump(cwl_dict, file)
        
        return filename
    except Exception as e:
        print(f"Error parsing or writing CWL file: {str(e)}")
        print("Raw YAML content:")
        print(cwl_content)
        return None

def parse_llm_output(response):
    if isinstance(response, AIMessage):
        content = response.content
    elif isinstance(response, str):
        content = response
    else:
        content = str(response)  # Fallback to string representation

    yaml_match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
    extracted_yaml = yaml_match.group(1) if yaml_match else None
    return extracted_yaml

def parse(generated_code):
    # Parse the LLM output
    extracted_yaml = parse_llm_output(generated_code)
    
    if not extracted_yaml:
        print("Failed to extract YAML content from LLM output")
        return

    # Generate CWL content
    cwl_content = generate_cwl(extracted_yaml)
    
    # Validate CWL content
    if validate_cwl(cwl_content):
        # Create CWL file
        filename = create_cwl_file(cwl_content)
        if filename:
            print(f"Valid CWL file generated: {filename}")
        else:
            print("Failed to create CWL file")
    else:
        print("Failed to generate a valid CWL file")

# # Example usage
# generated_code = """
# Your generated code here
# """

# main(generated_code)