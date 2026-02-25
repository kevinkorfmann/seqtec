Nextflow
========

Overview
--------

Nextflow is a reactive workflow framework built on the dataflow programming
model. In its current DSL2 syntax, pipelines are composed of modular processes
connected through channels. Each process runs in its own isolated environment,
with built-in support for Docker, Singularity, Conda, and cloud executors (AWS
Batch, Google Life Sciences, Azure Batch). Nextflow handles job scheduling,
fault tolerance with automatic retries, and seamless resumption of incomplete
runs via its caching mechanism. The nf-core community maintains a large
collection of peer-reviewed, production-ready pipelines for common
bioinformatics analyses.

Pipeline Steps
--------------

A typical Nextflow QC pipeline follows these steps:

1. Create a channel of paired-end read files using ``fromFilePairs``.
2. Run FastQC on each sample to generate quality reports.
3. Trim adapters and low-quality bases with fastp.
4. Collect all QC outputs and aggregate them into a MultiQC report.

QC Pipeline
-----------

The pipeline below implements the complete quality-control workflow in Nextflow
DSL2. It reads paired FASTQ files from a glob pattern, runs FastQC and fastp in
parallel per sample, then aggregates all reports with MultiQC.

.. code-block:: groovy

   #!/usr/bin/env nextflow
   nextflow.enable.dsl = 2

   params.reads    = "data/*_{R1,R2}.fastq.gz"
   params.outdir   = "results"
   params.min_qual = 20
   params.min_len  = 50

   process FASTQC {
       tag "${sample_id}"
       publishDir "${params.outdir}/fastqc", mode: 'copy'
       conda 'bioconda::fastqc=0.12.1'
       cpus 2

       input:
       tuple val(sample_id), path(reads)

       output:
       path("*.html"), emit: html
       path("*.zip"),  emit: zip

       script:
       """
       fastqc -t ${task.cpus} ${reads}
       """
   }

   process FASTP {
       tag "${sample_id}"
       publishDir "${params.outdir}/fastp", mode: 'copy'
       conda 'bioconda::fastp=0.23.4'
       cpus 4

       input:
       tuple val(sample_id), path(reads)

       output:
       tuple val(sample_id), path("*_trimmed.fastq.gz"), emit: trimmed
       path("*.html"), emit: html
       path("*.json"), emit: json

       script:
       def (r1, r2) = reads
       """
       fastp -i ${r1} -I ${r2} \
         -o ${sample_id}_R1_trimmed.fastq.gz \
         -O ${sample_id}_R2_trimmed.fastq.gz \
         -h ${sample_id}_fastp.html \
         -j ${sample_id}_fastp.json \
         --qualified_quality_phred ${params.min_qual} \
         --length_required ${params.min_len} \
         --detect_adapter_for_pe \
         --thread ${task.cpus}
       """
   }

   process MULTIQC {
       publishDir "${params.outdir}/multiqc", mode: 'copy'
       conda 'bioconda::multiqc=1.21'

       input:
       path('*')

       output:
       path("multiqc_report.html")

       script:
       """
       multiqc . -o . --force
       """
   }

   workflow {
       read_pairs_ch = Channel
           .fromFilePairs(params.reads, checkIfExists: true)

       FASTQC(read_pairs_ch)
       FASTP(read_pairs_ch)

       ch_multiqc = FASTQC.out.zip
           .mix(FASTP.out.json)
           .collect()

       MULTIQC(ch_multiqc)
   }

Configuration
-------------

Nextflow uses a ``nextflow.config`` file to define execution profiles. The
configuration below sets up local, SLURM, Docker, and Singularity profiles:

.. code-block:: groovy

   profiles {
       standard {
           process.executor = 'local'
           process.cpus = 4
           process.memory = '8 GB'
       }
       slurm {
           process.executor = 'slurm'
           process.queue = 'standard'
           process.cpus = 4
           process.memory = '8 GB'
           process.time = '2h'
       }
       docker {
           docker.enabled = true
       }
       singularity {
           singularity.enabled = true
           singularity.autoMounts = true
       }
   }

   process {
       errorStrategy = 'retry'
       maxRetries = 2
   }

Running the Pipeline
--------------------

.. code-block:: bash

   nextflow run main.nf --reads "data/*_{R1,R2}.fastq.gz"
   nextflow run main.nf -profile slurm
   nextflow run main.nf -profile docker
   nextflow run main.nf -resume
   nextflow run nf-core/rnaseq -r 3.14.0 \
     --input samplesheet.csv --genome GRCh38 -profile singularity

See Also
--------

* :doc:`snakemake` -- Snakemake workflow manager
* :doc:`wgs-variant-calling` -- WGS variant calling pipeline
* :doc:`rnaseq-differential-expression` -- RNA-seq differential expression pipeline
