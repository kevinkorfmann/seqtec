RNA-seq Differential Expression
================================

Overview
--------

RNA-seq differential expression analysis quantifies gene expression levels
across experimental conditions and identifies genes with statistically
significant changes. The Snakemake implementation uses STAR for splice-aware
alignment followed by featureCounts for read summarisation, while the Nextflow
implementation uses Salmon for lightweight, alignment-free quantification via
quasi-mapping. Both approaches feed count matrices into DESeq2 for
normalisation, dispersion estimation, and differential testing.

Pipeline Steps
--------------

1. Trim adapters and low-quality bases with fastp.
2. Align reads to the reference genome (STAR) or quantify transcripts directly (Salmon).
3. Generate a gene-level count matrix (featureCounts or Salmon ``quant.sf``).
4. Run DESeq2 for normalisation and differential expression testing.
5. Aggregate QC metrics into a MultiQC report.

Implementation
--------------

.. tabs::

   .. tab:: Snakemake

      The Snakemake approach uses STAR two-pass alignment and featureCounts for
      read counting, then runs DESeq2 via an R script.

      .. code-block:: python

         # Snakefile -- RNA-seq Differential Expression (STAR + featureCounts)
         configfile: "config.yaml"

         SAMPLES = config["samples"]
         REF     = config["star_index"]
         GTF     = config["gtf"]

         rule all:
             input:
                 "results/deseq2/differential_expression.csv",
                 "results/multiqc/multiqc_report.html"

         rule fastp_trim:
             input:
                 r1="data/{sample}_R1.fastq.gz",
                 r2="data/{sample}_R2.fastq.gz"
             output:
                 r1="results/trimmed/{sample}_R1.trimmed.fastq.gz",
                 r2="results/trimmed/{sample}_R2.trimmed.fastq.gz",
                 json="results/trimmed/{sample}_fastp.json",
                 html="results/trimmed/{sample}_fastp.html"
             threads: 4
             conda: "envs/qc.yaml"
             shell:
                 """
                 fastp -i {input.r1} -I {input.r2} \
                   -o {output.r1} -O {output.r2} \
                   -j {output.json} -h {output.html} \
                   --detect_adapter_for_pe --thread {threads}
                 """

         rule star_align:
             input:
                 r1="results/trimmed/{sample}_R1.trimmed.fastq.gz",
                 r2="results/trimmed/{sample}_R2.trimmed.fastq.gz",
                 index=REF
             output:
                 bam="results/star/{sample}/{sample}.Aligned.sortedByCoord.out.bam",
                 log="results/star/{sample}/{sample}.Log.final.out"
             threads: 12
             conda: "envs/align.yaml"
             shell:
                 """
                 STAR --runThreadN {threads} \
                   --genomeDir {input.index} \
                   --readFilesIn {input.r1} {input.r2} \
                   --readFilesCommand zcat \
                   --outSAMtype BAM SortedByCoordinate \
                   --outFileNamePrefix results/star/{wildcards.sample}/{wildcards.sample}. \
                   --quantMode GeneCounts \
                   --twopassMode Basic
                 samtools index {output.bam}
                 """

         rule featurecounts:
             input:
                 bams=expand("results/star/{sample}/{sample}.Aligned.sortedByCoord.out.bam",
                             sample=SAMPLES),
                 gtf=GTF
             output:
                 counts="results/featurecounts/gene_counts.txt",
                 summary="results/featurecounts/gene_counts.txt.summary"
             threads: 8
             conda: "envs/quantification.yaml"
             shell:
                 """
                 featureCounts -T {threads} -p --countReadPairs \
                   -a {input.gtf} -o {output.counts} \
                   -s 2 --primary \
                   {input.bams}
                 """

         rule deseq2:
             input:
                 counts="results/featurecounts/gene_counts.txt",
                 metadata=config["sample_metadata"]
             output:
                 results="results/deseq2/differential_expression.csv",
                 norm_counts="results/deseq2/normalised_counts.csv",
                 pca="results/deseq2/pca_plot.pdf",
                 ma="results/deseq2/ma_plot.pdf",
                 volcano="results/deseq2/volcano_plot.pdf"
             conda: "envs/deseq2.yaml"
             script:
                 "scripts/run_deseq2.R"

         rule multiqc:
             input:
                 expand("results/trimmed/{sample}_fastp.json", sample=SAMPLES),
                 expand("results/star/{sample}/{sample}.Log.final.out",
                        sample=SAMPLES),
                 "results/featurecounts/gene_counts.txt.summary"
             output:
                 "results/multiqc/multiqc_report.html"
             conda: "envs/qc.yaml"
             shell:
                 "multiqc results/ -o results/multiqc/ --force"

   .. tab:: Nextflow

      The Nextflow approach uses Salmon for alignment-free transcript
      quantification and passes the results to DESeq2 via tximport.

      .. code-block:: groovy

         #!/usr/bin/env nextflow
         nextflow.enable.dsl = 2

         params.reads       = "data/*_{R1,R2}.fastq.gz"
         params.salmon_index = "ref/salmon_index"
         params.gtf         = "ref/genes.gtf"
         params.outdir      = "results"
         params.metadata    = "samplesheet.csv"

         process FASTP {
             tag "${sample_id}"
             publishDir "${params.outdir}/trimmed", mode: 'copy'
             cpus 4
             input:  tuple val(sample_id), path(reads)
             output:
                 tuple val(sample_id), path("*_trimmed.fastq.gz"), emit: trimmed
                 path("*.json"), emit: json
             script:
             def (r1, r2) = reads
             """
             fastp -i ${r1} -I ${r2} \
               -o ${sample_id}_R1_trimmed.fastq.gz \
               -O ${sample_id}_R2_trimmed.fastq.gz \
               -j ${sample_id}_fastp.json \
               --detect_adapter_for_pe --thread ${task.cpus}
             """
         }

         process SALMON_QUANT {
             tag "${sample_id}"
             publishDir "${params.outdir}/salmon", mode: 'copy'
             cpus 8
             input:
                 tuple val(sample_id), path(reads)
                 path(index)
             output:
                 path("${sample_id}"), emit: quant_dir
             script:
             def (r1, r2) = reads
             """
             salmon quant -i ${index} -l A \
               -1 ${r1} -2 ${r2} \
               -o ${sample_id} \
               --threads ${task.cpus} \
               --validateMappings \
               --gcBias --seqBias
             """
         }

         process DESEQ2 {
             publishDir "${params.outdir}/deseq2", mode: 'copy'
             input:
                 path(quant_dirs)
                 path(metadata)
             output:
                 path("differential_expression.csv"), emit: results
                 path("normalised_counts.csv")
                 path("*.pdf")
             script:
             """
             run_deseq2_tximport.R \
               --quant_dirs . \
               --metadata ${metadata} \
               --output_prefix .
             """
         }

         process MULTIQC {
             publishDir "${params.outdir}/multiqc", mode: 'copy'
             input:  path('*')
             output: path("multiqc_report.html")
             script:
             """
             multiqc . -o . --force
             """
         }

         workflow {
             reads_ch = Channel.fromFilePairs(params.reads, checkIfExists: true)
             index_ch = Channel.value(file(params.salmon_index))

             FASTP(reads_ch)
             SALMON_QUANT(FASTP.out.trimmed, index_ch)

             quant_dirs = SALMON_QUANT.out.quant_dir.collect()
             DESEQ2(quant_dirs, file(params.metadata))

             ch_multiqc = FASTP.out.json
                 .mix(SALMON_QUANT.out.quant_dir)
                 .collect()
             MULTIQC(ch_multiqc)
         }

See Also
--------

* :doc:`snakemake` -- Snakemake workflow manager overview
* :doc:`nextflow` -- Nextflow DSL2 workflow manager overview
* :doc:`/tools/alignment/star` -- STAR aligner reference
* :doc:`/tools/quantification/index` -- Quantification tools
* :doc:`/tools/differential-expression/index` -- Differential expression tools
