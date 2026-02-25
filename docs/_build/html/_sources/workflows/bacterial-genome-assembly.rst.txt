Bacterial Genome Assembly (Nanopore)
=====================================

Overview
--------

Oxford Nanopore long-read sequencing enables complete or near-complete assembly
of bacterial genomes in a single contig. Long reads span repetitive elements
that fragment short-read assemblies, making it possible to resolve plasmids,
prophages, and genomic islands. This pipeline converts raw Nanopore BAM output
to FASTQ, filters reads by quality and length with Chopper, assembles with Flye
(optimized for bacterial genomes), polishes the consensus with Medaka, evaluates
assembly quality with QUAST and BUSCO, and annotates genes with Bakta.

Pipeline Steps
--------------

1. **BAM to FASTQ** -- Convert the raw Nanopore BAM file (produced by the
   basecaller) into FASTQ format using samtools.
2. **Chopper filter** -- Remove reads below a minimum quality score (Q10) and
   minimum length (1 kb) to reduce noise from failed or chimeric reads.
3. **Flye assembly** -- Assemble filtered long reads into contigs using the Flye
   assembler in ``--nano-hq`` mode, appropriate for Q20+ Nanopore reads.
4. **Medaka polish** -- Correct residual errors in the assembly consensus using
   a neural-network model trained on the specific Nanopore chemistry.
5. **QUAST** -- Compute assembly statistics including total length, number of
   contigs, N50, and GC content.
6. **BUSCO** -- Assess assembly completeness by searching for lineage-specific
   single-copy orthologs.
7. **Bakta annotate** -- Predict and annotate coding sequences, rRNAs, tRNAs,
   and other genomic features.

Implementation
--------------

.. tabs::

   .. tab:: Snakemake

      .. code-block:: python

         # Snakefile -- Nanopore Bacterial Genome Assembly
         configfile: "config.yaml"

         rule all:
             input:
                 "results/bakta/annotation.gff3"

         rule bam_to_fastq:
             input: config["raw_bam"]
             output: "results/fastq/reads.fastq.gz"
             shell: "samtools fastq {input} | gzip > {output}"

         rule chopper_filter:
             input: "results/fastq/reads.fastq.gz"
             output: "results/filtered/reads.filtered.fastq.gz"
             shell:
                 "zcat {input} | chopper --quality 10 --minlength 1000 | gzip > {output}"

         rule flye_assembly:
             input: "results/filtered/reads.filtered.fastq.gz"
             output: "results/flye/assembly.fasta"
             params: size=config["genome_size"]
             threads: 8
             shell:
                 "flye --nano-hq {input} --out-dir results/flye/ --genome-size {params.size} --threads {threads}"

         rule medaka_polish:
             input:
                 reads="results/filtered/reads.filtered.fastq.gz",
                 asm="results/flye/assembly.fasta"
             output: "results/medaka/consensus.fasta"
             params: model=config["medaka_model"]
             threads: 8
             shell:
                 "medaka_polisher -i {input.reads} -d {input.asm} -o results/medaka/ -m {params.model} --bacteria --threads {threads}"

         rule quast:
             input: "results/medaka/consensus.fasta"
             output: "results/quast/report.txt"
             shell: "quast {input} -o results/quast/"

         rule busco:
             input: "results/medaka/consensus.fasta"
             output: "results/busco/short_summary.txt"
             params: lineage=config["busco_lineage"]
             shell: "busco -i {input} -o results/busco/ -m genome -l {params.lineage} --cpu 8"

         rule bakta_annotate:
             input: "results/medaka/consensus.fasta"
             output: "results/bakta/annotation.gff3"
             params: db=config["bakta_db"]
             shell:
                 "bakta {input} --db {params.db} --output results/bakta/ --complete --threads 8"

   .. tab:: Nextflow

      .. code-block:: groovy

         #!/usr/bin/env nextflow
         nextflow.enable.dsl = 2

         params.raw_bam      = "data/reads.bam"
         params.genome_size   = "5m"
         params.medaka_model  = "r1041_e82_400bps_sup_v4.3.0"
         params.busco_lineage = "bacteria_odb10"
         params.bakta_db      = "ref/bakta_db"
         params.outdir        = "results"

         process BAM_TO_FASTQ {
             publishDir "${params.outdir}/fastq", mode: 'copy'
             input:  path(bam)
             output: path("reads.fastq.gz"), emit: fastq
             script:
             """
             samtools fastq ${bam} | gzip > reads.fastq.gz
             """
         }

         process CHOPPER_FILTER {
             publishDir "${params.outdir}/filtered", mode: 'copy'
             input:  path(fastq)
             output: path("reads.filtered.fastq.gz"), emit: fastq
             script:
             """
             zcat ${fastq} | chopper --quality 10 --minlength 1000 | gzip > reads.filtered.fastq.gz
             """
         }

         process FLYE_ASSEMBLY {
             publishDir "${params.outdir}/flye", mode: 'copy'
             cpus 8
             memory '16 GB'
             input:  path(fastq)
             output: path("assembly.fasta"), emit: assembly
             script:
             """
             flye --nano-hq ${fastq} \
               --out-dir flye_out/ \
               --genome-size ${params.genome_size} \
               --threads ${task.cpus}
             cp flye_out/assembly.fasta assembly.fasta
             """
         }

         process MEDAKA_POLISH {
             publishDir "${params.outdir}/medaka", mode: 'copy'
             cpus 8
             memory '16 GB'
             input:
                 path(reads)
                 path(assembly)
             output: path("consensus.fasta"), emit: consensus
             script:
             """
             medaka_polisher -i ${reads} -d ${assembly} \
               -o medaka_out/ \
               -m ${params.medaka_model} \
               --bacteria --threads ${task.cpus}
             cp medaka_out/consensus.fasta consensus.fasta
             """
         }

         process QUAST {
             publishDir "${params.outdir}/quast", mode: 'copy'
             input:  path(assembly)
             output: path("report.txt"), emit: report
             script:
             """
             quast ${assembly} -o quast_out/
             cp quast_out/report.txt report.txt
             """
         }

         process BUSCO {
             publishDir "${params.outdir}/busco", mode: 'copy'
             cpus 8
             input:  path(assembly)
             output: path("short_summary.txt"), emit: summary
             script:
             """
             busco -i ${assembly} -o busco_out -m genome \
               -l ${params.busco_lineage} --cpu ${task.cpus}
             cp busco_out/short_summary*.txt short_summary.txt
             """
         }

         process BAKTA_ANNOTATE {
             publishDir "${params.outdir}/bakta", mode: 'copy'
             cpus 8
             input:
                 path(assembly)
                 path(bakta_db)
             output:
                 path("annotation.gff3"), emit: gff
                 path("annotation.faa"), emit: proteins
             script:
             """
             bakta ${assembly} --db ${bakta_db} \
               --output bakta_out/ --complete --threads ${task.cpus}
             cp bakta_out/*.gff3 annotation.gff3
             cp bakta_out/*.faa annotation.faa
             """
         }

         workflow {
             raw_bam  = Channel.value(file(params.raw_bam))
             bakta_db = Channel.value(file(params.bakta_db))

             BAM_TO_FASTQ(raw_bam)
             CHOPPER_FILTER(BAM_TO_FASTQ.out.fastq)
             FLYE_ASSEMBLY(CHOPPER_FILTER.out.fastq)
             MEDAKA_POLISH(CHOPPER_FILTER.out.fastq, FLYE_ASSEMBLY.out.assembly)

             // QC and annotation run in parallel on the polished assembly
             QUAST(MEDAKA_POLISH.out.consensus)
             BUSCO(MEDAKA_POLISH.out.consensus)
             BAKTA_ANNOTATE(MEDAKA_POLISH.out.consensus, bakta_db)
         }

Expected Output
---------------

After a successful run the output directory will contain:

* ``results/fastq/reads.fastq.gz`` -- Converted FASTQ from the raw BAM.
* ``results/filtered/reads.filtered.fastq.gz`` -- Quality- and length-filtered
  reads.
* ``results/flye/assembly.fasta`` -- Draft genome assembly from Flye.
* ``results/medaka/consensus.fasta`` -- Polished consensus assembly.
* ``results/quast/report.txt`` -- Assembly statistics (total length, contigs,
  N50, GC content).
* ``results/busco/short_summary.txt`` -- Completeness assessment showing
  complete, fragmented, and missing orthologs.
* ``results/bakta/annotation.gff3`` -- Gene annotations in GFF3 format
  including CDS, rRNA, tRNA, and other features.

See Also
--------

* :doc:`nanopore-variant-calling` -- Nanopore variant calling with Clair3
* :doc:`metagenomics-classification` -- Metagenomic classification with Kraken2
