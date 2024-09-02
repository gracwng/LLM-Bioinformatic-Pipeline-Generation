# Axle Informatics: Large Language Model Driven Bioinformatics Pipeline Generation

## Challenge Summary: 
The Axle's team has developed a Common Workflow Language (CWL) based workflow builder named Sophios. It offers a concise YAML syntax, a Python API, and a REST API for defining compute-agnostic scientific workflows. Users need familiarity with the CWL ecosystem, intermediate Python skills, and basic containerization knowledge. However, these requirements may be restrictive for wet-lab biologists. With advancements in Large Language Model (LLM) based code generation, there's potential to create a tool that generates Sophios-based Python workflows from prompts, requiring minimal changes.

## Context / Impact:
A conversational agent for workflow creation can significantly reduce the need for scientists to master Python, CWL, and containerization, enhancing productivity and reproducibility.

## Project Goals:

- Generate training datasets for CLTs, CWL workflows, and Sophios API.
- Develop test and validation datasets for these components.
- Build a recursive testing framework for various models.
- Compare model performance on validation datasets.

## Suggested Approach:
Use resources like Bio-cwl-tools and WorkFlowHub for training data to develop a prompt-based tool that creates maintainable and compute-agnostic Python scripts in Sophios' language.

Citations:
- [1] https://www.commonwl.org
- [4] https://github.com/common-workflow-language/cwltool
- [6] https://cwl.discourse.group/t/writing-a-simple-cwl-workflow/568
