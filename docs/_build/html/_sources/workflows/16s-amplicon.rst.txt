16S Amplicon Sequencing
=======================

Overview
--------

16S ribosomal RNA gene amplicon sequencing is the standard approach for
profiling bacterial and archaeal community composition. The 16S rRNA gene
contains hypervariable regions (V1--V9) flanked by conserved primer-binding
sites, enabling PCR amplification from mixed microbial DNA. This pipeline
implements a DADA2-based workflow: primers are removed with Cutadapt, reads are
denoised into amplicon sequence variants (ASVs) with DADA2, taxonomy is
assigned against a reference database (SILVA or Greengenes2), and downstream
alpha/beta diversity analyses are performed. ASVs provide single-nucleotide
resolution compared to traditional OTU clustering, improving sensitivity for
detecting closely related taxa.

Pipeline Steps
--------------

1. **Cutadapt** -- Remove PCR primer sequences from the 5' ends of forward and
   reverse reads. Reads that do not contain the expected primer are discarded.
2. **DADA2** -- Learn error profiles, denoise reads, merge paired ends, remove
   chimeras, and assign taxonomy. DADA2 runs as a single R script that produces
   an ASV count table and taxonomy assignments.
3. **Diversity analysis** -- Compute alpha diversity metrics (Shannon, observed
   ASVs, Faith PD), beta diversity ordinations (Bray-Curtis PCoA, weighted
   UniFrac), and generate summary visualizations.

Implementation
--------------

.. tabs::

   .. tab:: Snakemake

      .. code-block:: python

         # Snakefile -- 16S Amplicon Pipeline (DADA2)
         configfile: "config.yaml"

         SAMPLES   = config["samples"]
         FWD_PRIMER = config["forward_primer"]   # e.g., "CCTACGGGNGGCWGCAG"
         REV_PRIMER = config["reverse_primer"]   # e.g., "GACTACHVGGGTATCTAATCC"
         SILVA_DB   = config["silva_db"]

         rule all:
             input:
                 "results/dada2/asv_table.tsv",
                 "results/dada2/taxonomy.tsv",
                 "results/diversity/alpha_diversity.tsv",
                 "results/diversity/beta_pcoa.pdf"

         rule cutadapt_primers:
             input:
                 r1="data/{sample}_R1.fastq.gz",
                 r2="data/{sample}_R2.fastq.gz"
             output:
                 r1="results/cutadapt/{sample}_R1.trimmed.fastq.gz",
                 r2="results/cutadapt/{sample}_R2.trimmed.fastq.gz"
             params:
                 fwd=FWD_PRIMER,
                 rev=REV_PRIMER
             threads: 4
             conda: "envs/cutadapt.yaml"
             shell:
                 """
                 cutadapt -g {params.fwd} -G {params.rev} \
                   --discard-untrimmed \
                   --cores {threads} \
                   -o {output.r1} -p {output.r2} \
                   {input.r1} {input.r2}
                 """

         rule dada2_pipeline:
             input:
                 r1=expand("results/cutadapt/{sample}_R1.trimmed.fastq.gz",
                           sample=SAMPLES),
                 r2=expand("results/cutadapt/{sample}_R2.trimmed.fastq.gz",
                           sample=SAMPLES)
             output:
                 asv="results/dada2/asv_table.tsv",
                 tax="results/dada2/taxonomy.tsv",
                 seqs="results/dada2/rep_seqs.fasta"
             params:
                 silva=SILVA_DB
             conda: "envs/dada2.yaml"
             script:
                 "scripts/run_dada2.R"

         rule diversity_analysis:
             input:
                 asv="results/dada2/asv_table.tsv",
                 tax="results/dada2/taxonomy.tsv",
                 meta=config["metadata"]
             output:
                 alpha="results/diversity/alpha_diversity.tsv",
                 pcoa="results/diversity/beta_pcoa.pdf"
             conda: "envs/phyloseq.yaml"
             script:
                 "scripts/run_diversity.R"

   .. tab:: Nextflow

      .. code-block:: groovy

         #!/usr/bin/env nextflow
         nextflow.enable.dsl = 2

         params.samplesheet    = "samplesheet.csv"
         params.forward_primer = "CCTACGGGNGGCWGCAG"
         params.reverse_primer = "GACTACHVGGGTATCTAATCC"
         params.silva_db       = "ref/silva_nr99_v138.1_train_set.fa.gz"
         params.metadata       = "metadata.tsv"
         params.outdir         = "results"

         process CUTADAPT {
             tag "${sample_id}"
             publishDir "${params.outdir}/cutadapt", mode: 'copy'
             cpus 4
             input:
                 tuple val(sample_id), path(r1), path(r2)
             output:
                 tuple val(sample_id),
                       path("${sample_id}_R1.trimmed.fastq.gz"),
                       path("${sample_id}_R2.trimmed.fastq.gz"), emit: reads
             script:
             """
             cutadapt -g ${params.forward_primer} -G ${params.reverse_primer} \
               --discard-untrimmed \
               --cores ${task.cpus} \
               -o ${sample_id}_R1.trimmed.fastq.gz \
               -p ${sample_id}_R2.trimmed.fastq.gz \
               ${r1} ${r2}
             """
         }

         process DADA2 {
             publishDir "${params.outdir}/dada2", mode: 'copy'
             cpus 8
             memory '16 GB'
             input:
                 path(trimmed_reads)
                 path(silva_db)
             output:
                 path("asv_table.tsv"), emit: asv
                 path("taxonomy.tsv"), emit: tax
                 path("rep_seqs.fasta"), emit: seqs
             script:
             """
             Rscript ${projectDir}/scripts/run_dada2.R \
               --input_dir . \
               --silva_db ${silva_db} \
               --output_dir .
             """
         }

         process DIVERSITY {
             publishDir "${params.outdir}/diversity", mode: 'copy'
             input:
                 path(asv_table)
                 path(taxonomy)
                 path(metadata)
             output:
                 path("alpha_diversity.tsv"), emit: alpha
                 path("beta_pcoa.pdf"), emit: pcoa
             script:
             """
             Rscript ${projectDir}/scripts/run_diversity.R \
               --asv_table ${asv_table} \
               --taxonomy ${taxonomy} \
               --metadata ${metadata} \
               --output_dir .
             """
         }

         workflow {
             ch_input = Channel.fromPath(params.samplesheet)
                 .splitCsv(header: true)
                 .map { row -> tuple(row.sample_id, file(row.fastq_r1), file(row.fastq_r2)) }

             silva = Channel.value(file(params.silva_db))
             meta  = Channel.value(file(params.metadata))

             CUTADAPT(ch_input)

             // Collect all trimmed FASTQs into a single directory for DADA2
             trimmed_all = CUTADAPT.out.reads
                 .map { sample_id, r1, r2 -> [r1, r2] }
                 .flatten()
                 .collect()

             DADA2(trimmed_all, silva)
             DIVERSITY(DADA2.out.asv, DADA2.out.tax, meta)
         }

Expected Output
---------------

After a successful run the output directory will contain:

* ``results/cutadapt/`` -- Primer-trimmed FASTQ files per sample.
* ``results/dada2/asv_table.tsv`` -- ASV count matrix (samples x ASVs).
* ``results/dada2/taxonomy.tsv`` -- Taxonomic assignments for each ASV from
  kingdom through species.
* ``results/dada2/rep_seqs.fasta`` -- Representative sequences for each ASV.
* ``results/diversity/alpha_diversity.tsv`` -- Per-sample Shannon index,
  observed ASVs, and Faith phylogenetic diversity.
* ``results/diversity/beta_pcoa.pdf`` -- Principal coordinates analysis plot
  based on Bray-Curtis dissimilarity.

See Also
--------

* :doc:`metagenomics-classification` -- Metagenomic classification with Kraken2
* :doc:`snakemake` -- Snakemake workflow manager overview
