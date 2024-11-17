# Create a Pydantic model to represent the CWL structure. This will include sections for the header, inputs, outputs, and steps.

from pydantic import BaseModel, Field
from typing import List, Dict, Any

class CWLInput(BaseModel):
    name: str = Field(description="Name of the input")
    type: str = Field(description="Type of the input (e.g., string, File)")

class CWLOutput(BaseModel):
    name: str = Field(description="Name of the output")
    type: str = Field(description="Type of the output (e.g., File)")
    source: str = Field(description="Source of the output")

class CWLStepInput(BaseModel):
    name: str = Field(description="Name of the step input")
    source: str = Field(description="Source of the input")

class CWLStep(BaseModel):
    name: str = Field(description="Step identifier")
    label: str = Field(description="Step label")
    doc: str = Field(description="Documentation for the step")
    run: str = Field(description="Path to the CWL tool for the step")
    inputs: List[CWLStepInput] = Field(description="Inputs to the step")
    outputs: List[str] = Field(description="Outputs of the step")

class CWLWorkflow(BaseModel):
    cwlVersion: str = Field(default="v1.0", description="CWL version")
    class_field: str = Field(default="Workflow", description="Class of the CWL document")
    label: str = Field(description="Workflow label")
    doc: str = Field(description="Workflow documentation")
    inputs: List[CWLInput] = Field(description="List of inputs")
    outputs: List[CWLOutput] = Field(description="List of outputs")
    steps: List[CWLStep] = Field(description="List of steps")
