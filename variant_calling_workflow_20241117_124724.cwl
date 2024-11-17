baseCommand:
- gatk
- ApplyBQSR
class: CommandLineTool
cwlVersion: v1.0
doc: 'This Common Workflow Language (CWL) tool implements the Genome Analysis Toolkit
  (GATK) function "ApplyBQSR," which is used for base quality score recalibration
  in genomic data processing. It takes as input a BAM file, a base recalibration file,
  and a reference genome, and produces a recalibrated BAM file along with optional
  index and VCF outputs. Notable features include support for multiple command-line
  options for fine-tuning the recalibration process, such as output indexing, read
  filtering, and quality score preservation.

  '
hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/gatk4:4.1.1.0--0
  ResourceRequirement:
    coresMin: 2
    ramMin: 4096
inputs:
  BaseRecalFile:
    inputBinding:
      prefix: --bqsr-recal-file
    type: File
  InputFile:
    inputBinding:
      prefix: --input
    secondaryFiles: .bai
    type: File
  Output:
    inputBinding:
      prefix: --output
      valueFrom: ApplyBQSR.bam
    type: string?
  Reference:
    inputBinding:
      prefix: --reference
    secondaryFiles:
    - .fai
    - ^.dict
    type: File
  isCreateBamIndex:
    inputBinding:
      prefix: --create-output-bam-index
    type: boolean?
  isDisableReadFilter:
    inputBinding:
      prefix: --disable-read-filter
    type: boolean?
  isEmitOriginalQuals:
    inputBinding:
      prefix: --emit-original-quals
    type: boolean?
label: GATK ApplyBQSR
outputs:
  alignment:
    outputBinding:
      glob: ApplyBQSR.bam
    type: File
  index:
    outputBinding:
      glob: ApplyBQSR.bai
    type:
    - 'null'
    - File
  vcf:
    format: edam:format_3016
    outputBinding:
      glob: '*.vcf'
    type:
    - 'null'
    - File
