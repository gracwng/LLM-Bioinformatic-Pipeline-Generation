class: CommandLineTool
id: 
  file:///Users/gracewang/Documents/Breakthrough%20AI/Axle%20Informatics/LLM-Bioinformatic-Pipeline-Generation/
inputs:
- id: IndexName
  inputBinding:
    prefix: "--index="
    separate: false
    valueFrom: $(self).kl
  type: string
- id: InputFiles
  format: http://edamontology.org/format_1929
  inputBinding:
    position: 200
  type:
    items: File
    type: array
- id: kmerSize
  inputBinding:
    prefix: "--kmer-size="
    separate: false
  type:
  - 'null'
  - int
- id: makeUnique
  inputBinding:
    prefix: "--make-unique"
  type:
  - 'null'
  - boolean
outputs:
- id: index
  outputBinding:
    glob: $(inputs.IndexName)
  type: File
hints:
- class: DockerRequirement
  dockerPull: quay.io/biocontainers/kallisto:0.45.0--hdcc98e5_0
- class: SoftwareRequirement
  packages:
  - package: kallisto
    version:
    - "0.45.0"
    specs:
    - https://identifiers.org/biotools/kallisto
cwlVersion: v1.0
baseCommand:
- kallisto
- index
$namespaces:
  edam: http://edamontology.org/
$schemas:
- https://edamontology.org/EDAM_1.18.owl
