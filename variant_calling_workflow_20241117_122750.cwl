class: Workflow
cwlVersion: v1.0
inputs:
  reads_1:
    label: First paired-end read file
    type: File
  reads_2:
    label: Second paired-end read file
    type: File
  reference_genome:
    label: Reference genome
    type: File
outputs:
  vcf_file:
    outputSource: variant_calling/vcf
    type: File
steps:
  alignment:
    in:
      reads_1: quality_control/trimmed_reads_1
      reads_2: quality_control/trimmed_reads_2
      reference_genome: reference_genome
    out:
    - aligned_bam
    run: bwa_mem.cwl
  quality_control:
    in:
      reads_1: reads_1
      reads_2: reads_2
    out:
    - trimmed_reads_1
    - trimmed_reads_2
    run: fastp.cwl
  sort_and_mark_duplicates:
    in:
      input_bam: alignment/aligned_bam
    out:
    - sorted_dedup_bam
    run: picard_markduplicates.cwl
  variant_calling:
    in:
      input_bam: sort_and_mark_duplicates/sorted_dedup_bam
      reference_genome: reference_genome
    out:
    - vcf
    run: gatk_haplotypecaller.cwl
