# # Create a Pydantic model to represent the CWL structure. This will include sections for the header, inputs, outputs, and steps.

# from pydantic import BaseModel, Field
# from typing import List, Union, Optional, Dict, Any

# class CWLVersion(BaseModel):
#     cwlVersion: str = Field(description="The version of CWL being used")

# class CWLBase(CWLVersion):
#     class_: str = Field(description="The class of the CWL document", alias="class")
#     id: Optional[str] = Field(description="Unique identifier for this object")
#     label: Optional[str] = Field(description="A short, human-readable label")
#     doc: Optional[str] = Field(description="A long, human-readable description")

# class InputParameter(BaseModel):
#     id: str = Field(description="The unique identifier for this input parameter")
#     type: Union[str, List[str]] = Field(description="The valid types for the input")
#     label: Optional[str] = Field(description="A short, human-readable label")
#     doc: Optional[str] = Field(description="A long, human-readable description")
#     default: Optional[Any] = Field(description="The default value for the input")

# class OutputParameter(BaseModel):
#     id: str = Field(description="The unique identifier for this output parameter")
#     type: Union[str, List[str]] = Field(description="The valid types for the output")
#     label: Optional[str] = Field(description="A short, human-readable label")
#     doc: Optional[str] = Field(description="A long, human-readable description")

# class CommandLineTool(CWLBase):
#     inputs: Dict[str, InputParameter] = Field(description="Input parameters for the tool")
#     outputs: Dict[str, OutputParameter] = Field(description="Output parameters for the tool")
#     baseCommand: Union[str, List[str]] = Field(description="The command line to execute")
#     arguments: Optional[List[str]] = Field(description="Additional command line arguments")

# class WorkflowStep(BaseModel):
#     id: str = Field(description="The unique identifier for this step")
#     run: str = Field(description="The CWL file to run for this step")
#     in_: Dict[str, str] = Field(description="Input mappings for this step", alias="in")
#     out: List[str] = Field(description="Outputs from this step")

# class Workflow(CWLBase):
#     inputs: Dict[str, InputParameter] = Field(description="Input parameters for the workflow")
#     outputs: Dict[str, OutputParameter] = Field(description="Output parameters for the workflow")
#     steps: Dict[str, WorkflowStep] = Field(description="The steps that make up the workflow")

# # class CWLDocument(BaseModel):
# #     cwl_object: Union[CommandLineTool, Workflow] = Field(description="The main CWL object")
    
# class CWLDocument(BaseModel):
#     cwl_object: Optional[Union[CommandLineTool, Workflow]] = Field(default=None, description="The main CWL object")

from pydantic import BaseModel, Field
from typing import List, Union, Optional, Dict, Any

class ResourceRequirement(BaseModel):
    ramMin: int
    coresMin: int

class DockerRequirement(BaseModel):
    dockerPull: str

class InlineJavascriptRequirement(BaseModel):
    pass  # Add fields as necessary for inline JavaScript requirements

class Requirements(BaseModel):
    ResourceRequirement: Optional[ResourceRequirement] = None # type: ignore
    DockerRequirement: Optional[DockerRequirement] = None # type: ignore
    InlineJavascriptRequirement: Optional[InlineJavascriptRequirement] = None # type: ignore
    # Add other requirement types as needed

class CWLVersion(BaseModel):
    cwlVersion: str = Field(description="The version of CWL being used")

class CWLBase(CWLVersion):
    class_: str = Field(description="The class of the CWL document", alias="class")
    id: Optional[str] = Field(description="Unique identifier for this object")
    label: Optional[str] = Field(description="A short, human-readable label")
    doc: Optional[str] = Field(description="A long, human-readable description")

class InputParameter(BaseModel):
    id: str = Field(description="The unique identifier for this input parameter")
    type: Union[str, List[str]] = Field(description="The valid types for the input")
    label: Optional[str] = Field(description="A short, human-readable label")
    doc: Optional[str] = Field(description="A long, human-readable description")
    default: Optional[Any] = Field(description="The default value for the input")

class OutputParameter(BaseModel):
    id: str = Field(description="The unique identifier for this output parameter")
    type: Union[str, List[str]] = Field(description="The valid types for the output")
    label: Optional[str] = Field(description="A short, human-readable label")
    doc: Optional[str] = Field(description="A long, human-readable description")

class CommandLineTool(CWLBase):
    inputs: Dict[str, InputParameter] = Field(default_factory=dict, description="Input parameters for the tool")
    outputs: Dict[str, OutputParameter] = Field(default_factory=dict, description="Output parameters for the tool")
    baseCommand: Union[str, List[str]] = Field(description="The command line to execute")
    arguments: Optional[List[str]] = Field(default=None, description="Additional command line arguments")
    requirements: Optional[Requirements] = Field(default=None, description="Requirements for the tool")

class WorkflowStep(BaseModel):
    id: str = Field(description="The unique identifier for this step")
    run: str = Field(description="The CWL file to run for this step")
    in_: Dict[str, str] = Field(description="Input mappings for this step", alias="in")
    out: List[str] = Field(description="Outputs from this step")

class Workflow(CWLBase):
    inputs: Dict[str, InputParameter] = Field(description="Input parameters for the workflow")
    outputs: Dict[str, OutputParameter] = Field(description="Output parameters for the workflow")
    steps: Dict[str, WorkflowStep] = Field(description="The steps that make up the workflow")
    requirements: Optional[Requirements] = Field(default=None, description="Requirements for the workflow")

class CWLDocument(BaseModel):
    cwl_object: Union[CommandLineTool, Workflow] = Field(description="The main CWL object")
    