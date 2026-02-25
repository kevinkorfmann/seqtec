Snakemake
=========

Overview
--------

Snakemake is a Python-based workflow management system that uses a declarative
syntax to define data analysis pipelines. Workflows are specified as a set of
rules, each describing how to produce output files from input files. Snakemake
automatically resolves dependencies between rules, determines execution order
via a directed acyclic graph (DAG), and supports parallel execution across
local cores or cluster nodes. Its integration with Conda, containers, and
cluster schedulers (SLURM, PBS, LSF) makes it a standard choice for
reproducible bioinformatics pipelines.

Pipeline Steps
--------------

A typical Snakemake QC pipeline follows these steps:

1. Define sample names and parameters in a configuration file (``config.yaml``).
2. Run FastQC on raw reads to generate per-sample quality reports.
3. Trim adapters and low-quality bases with fastp.
4. Aggregate all QC outputs into a single MultiQC report.

QC Pipeline
-----------

The Snakefile below implements the complete quality-control pipeline described
in the textbook. It reads sample names from a YAML configuration file, runs
FastQC on the raw paired-end reads, trims with fastp, and produces a combined
MultiQC report.

.. code-block:: python

   # Snakefile for basic QC pipeline
   configfile: "config.yaml"

   SAMPLES = config["samples"]

   rule all:
       input:
           expand("results/fastqc/{sample}_{read}_fastqc.html",
                  sample=SAMPLES, read=["R1", "R2"]),
           expand("results/fastp/{sample}_R1.trimmed.fastq.gz",
                  sample=SAMPLES),
           "results/multiqc/multiqc_report.html"

   rule fastqc_raw:
       input:
           "data/{sample}_{read}.fastq.gz"
       output:
           html="results/fastqc/{sample}_{read}_fastqc.html",
           zip="results/fastqc/{sample}_{read}_fastqc.zip"
       threads: 2
       conda:
           "envs/qc.yaml"
       shell:
           "fastqc -t {threads} -o results/fastqc/ {input}"

   rule fastp_trim:
       input:
           r1="data/{sample}_R1.fastq.gz",
           r2="data/{sample}_R2.fastq.gz"
       output:
           r1="results/fastp/{sample}_R1.trimmed.fastq.gz",
           r2="results/fastp/{sample}_R2.trimmed.fastq.gz",
           html="results/fastp/{sample}_fastp.html",
           json="results/fastp/{sample}_fastp.json"
       threads: 4
       conda:
           "envs/qc.yaml"
       params:
           qual=config.get("min_quality", 20),
           len=config.get("min_length", 50)
       shell:
           """
           fastp -i {input.r1} -I {input.r2} \
             -o {output.r1} -O {output.r2} \
             -h {output.html} -j {output.json} \
             --qualified_quality_phred {params.qual} \
             --length_required {params.len} \
             --detect_adapter_for_pe \
             --thread {threads}
           """

   rule multiqc:
       input:
           expand("results/fastqc/{sample}_{read}_fastqc.zip",
                  sample=SAMPLES, read=["R1", "R2"]),
           expand("results/fastp/{sample}_fastp.json",
                  sample=SAMPLES)
       output:
           "results/multiqc/multiqc_report.html"
       conda:
           "envs/qc.yaml"
       shell:
           "multiqc results/ -o results/multiqc/ --force"

Running the Pipeline
--------------------

.. code-block:: bash

   # Dry run
   snakemake -n --cores 8

   # Execute locally
   snakemake --cores 8 --use-conda

   # Execute on SLURM cluster
   snakemake --cores 100 --use-conda --slurm \
     --default-resources slurm_partition=standard mem_mb=8000

   # Generate DAG
   snakemake --dag | dot -Tpdf > dag.pdf

Configuration
-------------

Create a ``config.yaml`` file in the same directory as the Snakefile:

.. code-block:: yaml

   samples:
     - sample1
     - sample2
     - sample3
   min_quality: 20
   min_length: 50

See Also
--------

* :doc:`nextflow` -- Nextflow DSL2 workflow manager
* :doc:`wgs-variant-calling` -- WGS variant calling pipeline
* :doc:`rnaseq-differential-expression` -- RNA-seq differential expression pipeline
