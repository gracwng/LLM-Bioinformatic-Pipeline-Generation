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

def main(configs):
    docLoader = DocumentLoader('github')

    documents = docLoader.getDocuments(configs)
    print(documents[0].page_content)
    print(documents[0].metadata)


    # File Input - This is the only thing you will need to adjust or take in as an input to your function:
    cwl_file = "https://github.com/common-workflow-library/bio-cwl-tools/blob/release/GATK/GATK-ApplyBQSR.cwl"  # or a plain string works as well

    # Import CWL Object
    cwl_obj = load_document(documents[11].page_content)

    # View CWL Object
    print("List of object attributes:\n{}".format("\n".join(map(str, dir(cwl_obj)))))

    # Export CWL Object into a built-in typed object
    saved_obj = save(cwl_obj) # """Convert a CWL Python object into a JSON/YAML serializable object."""
    print(f"Export of the loaded CWL object: {saved_obj}.")

    # Save the CWL object to a file
    yaml = YAML()
    output_file = Path("cwl_documents/cwlDoc1.cwl")  # Specify the path where you want to save the file

    with output_file.open('w') as file:
        yaml.dump(saved_obj, file)

    print(f"CWL object saved to {output_file}")

    # # Access fields of the CWL object
    # print("CWL Version:", cwl_obj.cwlVersion)
    # print("Base Command:", cwl_obj.baseCommand)
    # print("Inputs:", cwl_obj.inputs)

    # Access fields in the saved object
    print("Top-level keys in saved_obj:", saved_obj.keys())
    for key, value in saved_obj.items():
        print(f"Key: {key}, Value: {value}")
if __name__ == '__main__':
    main(configs)