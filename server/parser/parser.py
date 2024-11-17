response = """content='Creating a CWL workflow for variant calling from whole genome sequencing data involves several steps, including quality control, alignment, and variant calling. Below is a simplified example of a CWL workflow that outlines these steps:\n\n```yaml\ncwlVersion: v1.0\nclass: Workflow\n\ninputs:\n  reference_genome:\n    type: File\n    label: "Reference genome"\n  reads_1:\n    type: File\n    label: "First paired-end read file"\n  reads_2:\n    type: File\n    label: "Second paired-end read file"\n\noutputs:\n  vcf_file:\n    type: File\n    outputSource: variant_calling/vcf\n\nsteps:\n  quality_control:\n    run: fastp.cwl\n    in:\n      reads_1: reads_1\n      reads_2: reads_2\n    out: [trimmed_reads_1, trimmed_reads_2]\n\n  alignment:\n    run: bwa_mem.cwl\n    in:\n      reference_genome: reference_genome\n      reads_1: quality_control/trimmed_reads_1\n      reads_2: quality_control/trimmed_reads_2\n    out: [aligned_bam]\n\n  sort_and_mark_duplicates:\n    run: picard_markduplicates.cwl\n    in:\n      input_bam: alignment/aligned_bam\n    out: [sorted_dedup_bam]\n\n  variant_calling:\n    run: gatk_haplotypecaller.cwl\n    in:\n      reference_genome: reference_genome\n      input_bam: sort_and_mark_duplicates/sorted_dedup_bam\n    out: [vcf]\n```\n\nThis workflow includes steps for quality control using `fastp`, alignment with `bwa_mem`, sorting and marking duplicates with `picard`, and variant calling with `GATK HaplotypeCaller`. Each step references a separate CWL tool definition (e.g., `fastp.cwl`, `bwa_mem.cwl`, etc.) that you would need to create or obtain.' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 422, 'prompt_tokens': 4810, 'total_tokens': 5232, 'completion_tokens_details': {'audio_tokens': 0, 'reasoning_tokens': 0, 'accepted_prediction_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_72bbfa6014', 'finish_reason': 'stop', 'logprobs': None} id='run-c745bcd6-2a6f-465b-b45b-b764c3db4fe7-0' usage_metadata={'input_tokens': 4810, 'output_tokens': 422, 'total_tokens': 5232, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}"""
import re
import yaml
from datetime import datetime

def parse_llm_output(content):
    # Extract the CWL YAML content using regex
    yaml_match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
    if yaml_match:
        return yaml_match.group(1)
    else:
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

# Parse the LLM output to extract the CWL YAML content
extracted_yaml = parse_llm_output(response)
if extracted_yaml:
    # Create the CWL file
    filename = create_cwl_file(extracted_yaml)
    print(f"CWL file created: {filename}")
else:
    print("Failed to extract YAML content from LLM output")
