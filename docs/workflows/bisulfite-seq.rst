Bisulfite Sequencing (WGBS)
===========================

Overview
--------

Whole-genome bisulfite sequencing (WGBS) provides single-nucleotide resolution
maps of DNA methylation across the entire genome. Sodium bisulfite treatment
converts unmethylated cytosines to uracils while leaving methylated cytosines
intact. Sequencing reads are then aligned to a bisulfite-converted reference
genome, and the methylation status of each CpG (or non-CpG) site is determined
from the ratio of converted to unconverted bases. This pipeline implements a
standard WGBS analysis: adapter trimming with Trim Galore, alignment and
deduplication with Bismark, methylation extraction, and aggregated quality
reporting with MultiQC.

Pipeline Steps
--------------

1. **Trim Galore** -- Remove adapter sequences and low-quality bases from
   paired-end reads. Trim Galore automatically detects Illumina adapter
   contamination and applies quality trimming.
2. **Bismark align** -- Align trimmed reads to a bisulfite-converted reference
   genome using Bismark (wrapping Bowtie 2). Bismark handles the four possible
   bisulfite-converted strands transparently.
3. **Bismark dedup** -- Remove PCR duplicates from the aligned BAM file.
   Deduplication is critical in WGBS because duplicate reads inflate apparent
   coverage and bias methylation estimates.
4. **Methylation extraction** -- Extract per-cytosine methylation calls from
   deduplicated alignments, producing bedGraph and coverage files.
5. **MultiQC** -- Aggregate Trim Galore, Bismark alignment, deduplication, and
   methylation extraction reports into a single HTML summary.

Implementation
--------------

.. tabs::

   .. tab:: Snakemake

      .. code-block:: python

         # Snakefile -- WGBS Bisulfite Sequencing Pipeline
         configfile: "config.yaml"

         SAMPLES     = config["samples"]
         BISMARK_IDX = config["bismark_index"]

         rule all:
             input:
                 expand("results/methylation/{sample}.bismark.cov.gz", sample=SAMPLES),
                 "results/multiqc/multiqc_report.html"

         rule trim_galore:
             input:
                 r1="data/{sample}_R1.fastq.gz",
                 r2="data/{sample}_R2.fastq.gz"
             output:
                 r1="results/trimmed/{sample}_R1_val_1.fq.gz",
                 r2="results/trimmed/{sample}_R2_val_2.fq.gz",
                 report_r1="results/trimmed/{sample}_R1.fastq.gz_trimming_report.txt",
                 report_r2="results/trimmed/{sample}_R2.fastq.gz_trimming_report.txt"
             threads: 4
             conda: "envs/trimgalore.yaml"
             shell:
                 """
                 trim_galore --paired --cores {threads} \
                   -o results/trimmed/ \
                   {input.r1} {input.r2}
                 """

         rule bismark_align:
             input:
                 r1="results/trimmed/{sample}_R1_val_1.fq.gz",
                 r2="results/trimmed/{sample}_R2_val_2.fq.gz"
             output:
                 bam="results/bismark/{sample}_R1_val_1_bismark_bt2_pe.bam",
                 report="results/bismark/{sample}_R1_val_1_bismark_bt2_PE_report.txt"
             threads: 8
             params:
                 idx=BISMARK_IDX
             conda: "envs/bismark.yaml"
             shell:
                 """
                 bismark --genome {params.idx} \
                   -1 {input.r1} -2 {input.r2} \
                   --parallel {threads} \
                   -o results/bismark/
                 """

         rule bismark_dedup:
             input:
                 "results/bismark/{sample}_R1_val_1_bismark_bt2_pe.bam"
             output:
                 bam="results/dedup/{sample}.deduplicated.bam",
                 report="results/dedup/{sample}.deduplication_report.txt"
             conda: "envs/bismark.yaml"
             shell:
                 """
                 deduplicate_bismark --paired --bam \
                   --output_dir results/dedup/ \
                   {input}
                 """

         rule methylation_extract:
             input:
                 "results/dedup/{sample}.deduplicated.bam"
             output:
                 "results/methylation/{sample}.bismark.cov.gz"
             params:
                 idx=BISMARK_IDX
             threads: 8
             conda: "envs/bismark.yaml"
             shell:
                 """
                 bismark_methylation_extractor --paired-end \
                   --comprehensive --merge_non_CpG \
                   --parallel {threads} \
                   --genome_folder {params.idx} \
                   --bedGraph --counts \
                   -o results/methylation/ \
                   {input}
                 """

         rule multiqc:
             input:
                 expand("results/methylation/{sample}.bismark.cov.gz", sample=SAMPLES)
             output:
                 "results/multiqc/multiqc_report.html"
             conda: "envs/multiqc.yaml"
             shell:
                 "multiqc results/ -o results/multiqc/ --force"

   .. tab:: Nextflow

      .. code-block:: groovy

         #!/usr/bin/env nextflow
         nextflow.enable.dsl = 2

         params.samplesheet  = "samplesheet.csv"
         params.bismark_index = "ref/bismark_index"
         params.outdir        = "results"

         process TRIM_GALORE {
             tag "${sample_id}"
             publishDir "${params.outdir}/trimmed", mode: 'copy'
             cpus 4
             input:
                 tuple val(sample_id), path(r1), path(r2)
             output:
                 tuple val(sample_id),
                       path("*_val_1.fq.gz"),
                       path("*_val_2.fq.gz"), emit: reads
                 path("*_trimming_report.txt"), emit: reports
             script:
             """
             trim_galore --paired --cores ${task.cpus} ${r1} ${r2}
             """
         }

         process BISMARK_ALIGN {
             tag "${sample_id}"
             publishDir "${params.outdir}/bismark", mode: 'copy'
             cpus 8
             memory '32 GB'
             input:
                 tuple val(sample_id), path(r1), path(r2)
                 path(bismark_index)
             output:
                 tuple val(sample_id), path("*_bismark_bt2_pe.bam"), emit: bam
                 path("*_PE_report.txt"), emit: report
             script:
             """
             bismark --genome ${bismark_index} \
               -1 ${r1} -2 ${r2} \
               --parallel ${task.cpus}
             """
         }

         process BISMARK_DEDUP {
             tag "${sample_id}"
             publishDir "${params.outdir}/dedup", mode: 'copy'
             input:
                 tuple val(sample_id), path(bam)
             output:
                 tuple val(sample_id), path("*.deduplicated.bam"), emit: bam
                 path("*.deduplication_report.txt"), emit: report
             script:
             """
             deduplicate_bismark --paired --bam ${bam}
             """
         }

         process METHYL_EXTRACT {
             tag "${sample_id}"
             publishDir "${params.outdir}/methylation", mode: 'copy'
             cpus 8
             input:
                 tuple val(sample_id), path(bam)
                 path(bismark_index)
             output:
                 tuple val(sample_id), path("*.bismark.cov.gz"), emit: coverage
                 path("*.txt"), emit: reports
             script:
             """
             bismark_methylation_extractor --paired-end \
               --comprehensive --merge_non_CpG \
               --parallel ${task.cpus} \
               --genome_folder ${bismark_index} \
               --bedGraph --counts \
               ${bam}
             """
         }

         workflow {
             ch_input = Channel.fromPath(params.samplesheet)
                 .splitCsv(header: true)
                 .map { row -> tuple(row.sample_id, file(row.fastq_r1), file(row.fastq_r2)) }

             bismark_idx = Channel.value(file(params.bismark_index))

             TRIM_GALORE(ch_input)
             BISMARK_ALIGN(TRIM_GALORE.out.reads, bismark_idx)
             BISMARK_DEDUP(BISMARK_ALIGN.out.bam)
             METHYL_EXTRACT(BISMARK_DEDUP.out.bam, bismark_idx)
         }

Expected Output
---------------

After a successful run the output directory will contain:

* ``results/trimmed/`` -- Adapter-trimmed FASTQ files and Trim Galore
  trimming reports.
* ``results/bismark/`` -- Bismark-aligned BAM files and alignment reports
  showing mapping efficiency, C-to-T conversion rates, and strand information.
* ``results/dedup/`` -- Deduplicated BAM files and deduplication reports
  indicating the fraction of duplicate reads removed.
* ``results/methylation/`` -- Per-cytosine methylation coverage files
  (``*.bismark.cov.gz``), bedGraph files, and M-bias reports.
* ``results/multiqc/multiqc_report.html`` -- Aggregated quality report
  summarizing all pipeline stages.

See Also
--------

* :doc:`snakemake` -- Snakemake workflow manager overview
* :doc:`chipseq` -- ChIP-seq pipeline for histone modification profiling
