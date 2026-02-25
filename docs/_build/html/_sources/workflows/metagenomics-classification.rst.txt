Metagenomic Classification
==========================

Overview
--------

Metagenomic classification assigns taxonomic labels to sequencing reads without
requiring assembly or marker-gene amplification, providing a culture-independent
view of microbial community composition directly from shotgun or long-read
sequencing data. This pipeline uses Kraken2 for fast k-mer-based taxonomic
classification, Bracken for Bayesian re-estimation of species-level abundances,
and Krona for interactive hierarchical visualization. An initial quality
filtering step with Chopper removes low-quality and short reads to reduce
spurious classifications.

Pipeline Steps
--------------

1. **Chopper** -- Filter reads by minimum quality (Q10) and minimum length
   (1 kb) to remove low-confidence basecalls and adapter artifacts.
2. **Kraken2** -- Classify each read against a pre-built k-mer database,
   assigning taxonomic labels based on exact k-mer matches. The
   ``--minimum-hit-groups 3`` parameter requires hits across multiple distinct
   minimizer groups to reduce false-positive classifications.
3. **Bracken** -- Re-estimate species-level abundances from the Kraken2 report
   using a Bayesian model that redistributes reads assigned to higher taxonomic
   levels. Reads are re-distributed based on read-length-specific expected
   k-mer distributions.
4. **Krona** -- Convert the Kraken2 report into an interactive HTML
   visualization showing the hierarchical taxonomic composition of the sample.

Implementation
--------------

.. tabs::

   .. tab:: Snakemake

      .. code-block:: python

         # Snakefile -- Metagenomic Classification Pipeline
         configfile: "config.yaml"

         SAMPLES    = config["samples"]
         KRAKEN2_DB = config["kraken2_db"]

         rule all:
             input:
                 expand("results/bracken/{sample}_bracken.txt", sample=SAMPLES),
                 expand("results/krona/{sample}_krona.html", sample=SAMPLES)

         rule chopper_filter:
             input:
                 "data/{sample}.fastq.gz"
             output:
                 "results/filtered/{sample}.filtered.fastq.gz"
             shell:
                 "zcat {input} | chopper --quality 10 --minlength 1000 | gzip > {output}"

         rule kraken2:
             input:
                 "results/filtered/{sample}.filtered.fastq.gz"
             output:
                 classifications="results/kraken2/{sample}_classifications.txt",
                 report="results/kraken2/{sample}_report.txt"
             params:
                 db=KRAKEN2_DB
             threads: 8
             shell:
                 """
                 kraken2 --db {params.db} \
                   --output {output.classifications} \
                   --report {output.report} \
                   --minimum-hit-groups 3 \
                   --threads {threads} \
                   {input}
                 """

         rule bracken:
             input:
                 report="results/kraken2/{sample}_report.txt"
             output:
                 "results/bracken/{sample}_bracken.txt"
             params:
                 db=KRAKEN2_DB
             shell:
                 """
                 bracken -d {params.db} \
                   -i {input.report} \
                   -o {output} \
                   -r 1000 -l S -t 10
                 """

         rule krona:
             input:
                 report="results/kraken2/{sample}_report.txt"
             output:
                 "results/krona/{sample}_krona.html"
             shell:
                 """
                 kreport2krona.py -r {input.report} -o results/krona/{wildcards.sample}_krona_input.txt
                 ktImportText results/krona/{wildcards.sample}_krona_input.txt \
                   -o {output}
                 """

   .. tab:: Nextflow

      .. code-block:: groovy

         #!/usr/bin/env nextflow
         nextflow.enable.dsl = 2

         params.samplesheet = "samplesheet.csv"
         params.kraken2_db  = "ref/kraken2_db"
         params.outdir      = "results"

         process CHOPPER_FILTER {
             tag "${sample_id}"
             publishDir "${params.outdir}/filtered", mode: 'copy'
             input:
                 tuple val(sample_id), path(fastq)
             output:
                 tuple val(sample_id), path("${sample_id}.filtered.fastq.gz"), emit: fastq
             script:
             """
             zcat ${fastq} | chopper --quality 10 --minlength 1000 \
               | gzip > ${sample_id}.filtered.fastq.gz
             """
         }

         process KRAKEN2 {
             tag "${sample_id}"
             publishDir "${params.outdir}/kraken2", mode: 'copy'
             cpus 8
             memory '64 GB'
             input:
                 tuple val(sample_id), path(fastq)
                 path(kraken2_db)
             output:
                 tuple val(sample_id),
                       path("${sample_id}_classifications.txt"),
                       path("${sample_id}_report.txt"), emit: results
                 tuple val(sample_id),
                       path("${sample_id}_report.txt"), emit: report
             script:
             """
             kraken2 --db ${kraken2_db} \
               --output ${sample_id}_classifications.txt \
               --report ${sample_id}_report.txt \
               --minimum-hit-groups 3 \
               --threads ${task.cpus} \
               ${fastq}
             """
         }

         process BRACKEN {
             tag "${sample_id}"
             publishDir "${params.outdir}/bracken", mode: 'copy'
             input:
                 tuple val(sample_id), path(report)
                 path(kraken2_db)
             output:
                 tuple val(sample_id), path("${sample_id}_bracken.txt"), emit: abundances
             script:
             """
             bracken -d ${kraken2_db} \
               -i ${report} \
               -o ${sample_id}_bracken.txt \
               -r 1000 -l S -t 10
             """
         }

         process KRONA {
             tag "${sample_id}"
             publishDir "${params.outdir}/krona", mode: 'copy'
             input:
                 tuple val(sample_id), path(report)
             output:
                 path("${sample_id}_krona.html"), emit: html
             script:
             """
             kreport2krona.py -r ${report} -o ${sample_id}_krona_input.txt
             ktImportText ${sample_id}_krona_input.txt \
               -o ${sample_id}_krona.html
             """
         }

         workflow {
             ch_input = Channel.fromPath(params.samplesheet)
                 .splitCsv(header: true)
                 .map { row -> tuple(row.sample_id, file(row.fastq)) }

             kraken2_db = Channel.value(file(params.kraken2_db))

             CHOPPER_FILTER(ch_input)
             KRAKEN2(CHOPPER_FILTER.out.fastq, kraken2_db)
             BRACKEN(KRAKEN2.out.report, kraken2_db)
             KRONA(KRAKEN2.out.report)
         }

Expected Output
---------------

After a successful run the output directory will contain:

* ``results/filtered/`` -- Quality- and length-filtered FASTQ files.
* ``results/kraken2/<sample>_classifications.txt`` -- Per-read taxonomic
  assignments from Kraken2.
* ``results/kraken2/<sample>_report.txt`` -- Kraken2 summary report with
  read counts and percentages at each taxonomic level.
* ``results/bracken/<sample>_bracken.txt`` -- Bracken species-level abundance
  estimates with re-distributed read counts and fractions.
* ``results/krona/<sample>_krona.html`` -- Interactive Krona pie chart showing
  hierarchical taxonomic composition (viewable in any web browser).

See Also
--------

* :doc:`16s-amplicon` -- 16S amplicon sequencing pipeline with DADA2
* :doc:`bacterial-genome-assembly` -- Nanopore bacterial genome assembly
