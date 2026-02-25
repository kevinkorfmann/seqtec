scRNA-seq
=========

Overview
--------

Single-cell RNA sequencing (scRNA-seq) measures gene expression in individual
cells, enabling the identification of cell types, states, and trajectories
within heterogeneous tissues. This workflow covers the complete analysis from
raw FASTQ files to an integrated multi-sample object. STARsolo performs barcode
demultiplexing and UMI counting directly during alignment, producing a
cell-by-gene count matrix. Scanpy then handles quality filtering, normalization,
dimensionality reduction, clustering, and marker gene detection. When multiple
samples are profiled, batch-aware integration (e.g., scVI, Harmony, or
scanorama) corrects for technical variation while preserving biological signal.

Pipeline Steps
--------------

1. **STARsolo** -- Align reads, demultiplex cell barcodes, collapse UMIs, and
   produce a filtered count matrix per sample. Empty droplets are removed with
   the ``EmptyDrops_CR`` cell-calling algorithm.
2. **Scanpy analysis** -- For each sample, load the count matrix, filter cells
   and genes, normalize, identify highly variable genes, compute PCA, build a
   neighbor graph, cluster (Leiden), and run UMAP embedding.
3. **Integration** -- Concatenate per-sample AnnData objects and apply a
   batch-correction method to produce a unified embedding across all samples.

Implementation
--------------

.. tabs::

   .. tab:: Snakemake

      .. code-block:: python

         # Snakefile -- scRNA-seq Pipeline
         configfile: "config.yaml"

         SAMPLES    = config["samples"]
         STAR_IDX   = config["star_index"]
         WHITELIST  = config["barcode_whitelist"]

         rule all:
             input:
                 expand("results/scanpy/{sample}_processed.h5ad", sample=SAMPLES),
                 "results/scanpy/integrated.h5ad"

         rule starsolo:
             input:
                 r1="data/{sample}_R1.fastq.gz",
                 r2="data/{sample}_R2.fastq.gz"
             output:
                 bam="results/starsolo/{sample}/Aligned.sortedByCoord.out.bam",
                 mtx="results/starsolo/{sample}/Solo.out/Gene/filtered/matrix.mtx"
             threads: 16
             params:
                 idx=STAR_IDX,
                 wl=WHITELIST,
                 outdir="results/starsolo/{sample}/"
             conda: "envs/starsolo.yaml"
             shell:
                 """
                 STAR --runThreadN {threads} \
                   --genomeDir {params.idx} \
                   --readFilesIn {input.r1} {input.r2} \
                   --readFilesCommand zcat \
                   --soloType CB_UMI_Simple \
                   --soloCBwhitelist {params.wl} \
                   --soloCBstart 1 --soloCBlen 16 \
                   --soloUMIstart 17 --soloUMIlen 12 \
                   --outSAMtype BAM SortedByCoordinate \
                   --outFileNamePrefix {params.outdir} \
                   --soloFeatures Gene \
                   --soloCellFilter EmptyDrops_CR
                 """

         rule scanpy_analysis:
             input:
                 mtx="results/starsolo/{sample}/Solo.out/Gene/filtered/matrix.mtx"
             output:
                 h5ad="results/scanpy/{sample}_processed.h5ad"
             conda: "envs/scanpy.yaml"
             script:
                 "scripts/run_scanpy.py"

         rule integrate_samples:
             input:
                 expand("results/scanpy/{sample}_processed.h5ad", sample=SAMPLES)
             output:
                 "results/scanpy/integrated.h5ad"
             conda: "envs/scanpy.yaml"
             script:
                 "scripts/integrate_scanpy.py"

   .. tab:: Nextflow

      .. code-block:: groovy

         #!/usr/bin/env nextflow
         nextflow.enable.dsl = 2

         params.samplesheet = "samplesheet.csv"
         params.star_index  = "ref/star_index"
         params.whitelist   = "ref/3M-february-2018.txt"
         params.outdir      = "results"

         process STARSOLO {
             tag "${sample_id}"
             publishDir "${params.outdir}/starsolo/${sample_id}", mode: 'copy'
             cpus 16
             memory '64 GB'
             input:
                 tuple val(sample_id), path(r1), path(r2)
                 path(star_index)
                 path(whitelist)
             output:
                 tuple val(sample_id), path("Solo.out/Gene/filtered/"), emit: counts
                 path("Log.final.out"), emit: log
             script:
             """
             STAR --runThreadN ${task.cpus} \
               --genomeDir ${star_index} \
               --readFilesIn ${r1} ${r2} \
               --readFilesCommand zcat \
               --soloType CB_UMI_Simple \
               --soloCBwhitelist ${whitelist} \
               --soloCBstart 1 --soloCBlen 16 \
               --soloUMIstart 17 --soloUMIlen 12 \
               --outSAMtype BAM SortedByCoordinate \
               --soloFeatures Gene \
               --soloCellFilter EmptyDrops_CR
             """
         }

         process SCANPY_PROCESS {
             tag "${sample_id}"
             publishDir "${params.outdir}/scanpy", mode: 'copy'
             input:  tuple val(sample_id), path(counts_dir)
             output: tuple val(sample_id), path("${sample_id}_processed.h5ad"), emit: h5ad
             script:
             """
             python ${projectDir}/scripts/run_scanpy.py \
               --input ${counts_dir} --sample ${sample_id} \
               --output ${sample_id}_processed.h5ad
             """
         }

         process INTEGRATE {
             publishDir "${params.outdir}/scanpy", mode: 'copy'
             input:  path(h5ad_files)
             output: path("integrated.h5ad")
             script:
             """
             python ${projectDir}/scripts/integrate_scanpy.py \
               --input_files ${h5ad_files} --output integrated.h5ad
             """
         }

         workflow {
             ch_input = Channel.fromPath(params.samplesheet)
                 .splitCsv(header: true)
                 .map { row -> tuple(row.sample_id, file(row.fastq_r1), file(row.fastq_r2)) }

             star_idx = Channel.value(file(params.star_index))
             wl       = Channel.value(file(params.whitelist))

             STARSOLO(ch_input, star_idx, wl)
             SCANPY_PROCESS(STARSOLO.out.counts)
             INTEGRATE(SCANPY_PROCESS.out.h5ad.map { it[1] }.collect())
         }

Expected Output
---------------

After a successful run the output directory will contain:

* ``results/starsolo/<sample>/Solo.out/Gene/filtered/`` -- Per-sample filtered
  count matrices (``matrix.mtx``, ``barcodes.tsv``, ``features.tsv``).
* ``results/scanpy/<sample>_processed.h5ad`` -- AnnData objects with QC
  metrics, clusters, UMAP coordinates, and marker genes per sample.
* ``results/scanpy/integrated.h5ad`` -- Combined AnnData with batch-corrected
  embedding, joint clustering, and cell-type annotations.

See Also
--------

* :doc:`rnaseq-differential-expression` -- Bulk RNA-seq differential expression pipeline
* :doc:`snakemake` -- Snakemake workflow manager overview
