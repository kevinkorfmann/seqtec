Cell Ranger
===========

Overview
--------

Cell Ranger is the official analysis pipeline from 10x Genomics for processing
Chromium single-cell gene expression data. It performs FASTQ generation,
read alignment to a reference transcriptome, barcode and UMI counting, and
cell-by-gene matrix construction. Cell Ranger also runs secondary analyses
including dimensionality reduction, clustering, and differential expression,
providing web-viewable summary reports for rapid quality assessment.

Installation
------------

Download the latest release from the
`10x Genomics support site <https://support.10xgenomics.com/>`_. After
extracting the archive, add the ``cellranger`` binary to your ``PATH``:

.. code-block:: bash

   tar -xzf cellranger-8.0.1.tar.gz
   export PATH=$PWD/cellranger-8.0.1:$PATH

Cell Ranger is not available through Bioconda. A 10x-compatible reference
package is also required (e.g., ``refdata-gex-GRCh38-2024-A``).

Basic Usage
-----------

Run the ``count`` pipeline to align reads and generate the filtered
feature-barcode matrix for a single sample.

.. code-block:: bash

   cellranger count --id=sample1 \
     --transcriptome=/ref/refdata-gex-GRCh38-2024-A \
     --fastqs=/data/sample1/ \
     --sample=sample1 \
     --localcores=16 --localmem=64

Cell Ranger auto-detects chemistry by default. If multiple FASTQ directories
exist for the same sample, provide them as a comma-separated list to
``--fastqs``.

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``--id``
     - A unique run ID; Cell Ranger creates an output directory with this name.
   * - ``--transcriptome``
     - Path to the Cell Ranger-compatible reference transcriptome directory.
   * - ``--fastqs``
     - Path to the directory containing FASTQ files (or a comma-separated list
       of directories).
   * - ``--sample``
     - Sample name prefix as it appears in the FASTQ file names.
   * - ``--localcores``
     - Maximum number of CPU cores to use (default: all available).
   * - ``--localmem``
     - Maximum memory in GB to use (default: 90% of system memory).
   * - ``--expect-cells``
     - Expected number of recovered cells (default: 3000). Cell Ranger uses
       this as a hint for cell calling.
   * - ``--chemistry``
     - Assay chemistry (e.g., ``SC3Pv3``). Usually auto-detected.
   * - ``--include-introns``
     - Count reads mapping to introns (enabled by default since Cell Ranger
       7.0 for single-nuclei data).

Expected Output
---------------

Cell Ranger creates a directory named after the ``--id`` value. Key outputs
include:

* ``outs/filtered_feature_bc_matrix/`` -- the filtered cell-by-gene count
  matrix in Market Exchange format (MEX), containing barcodes that Cell Ranger
  identified as valid cells.
* ``outs/raw_feature_bc_matrix/`` -- the unfiltered count matrix for all
  detected barcodes.
* ``outs/possorted_genome_bam.bam`` -- coordinate-sorted BAM file with
  cell-barcode and UMI tags.
* ``outs/web_summary.html`` -- interactive HTML report with sequencing quality,
  mapping statistics, and preliminary clustering results.
* ``outs/metrics_summary.csv`` -- tab-delimited summary of key metrics
  (estimated cells, reads per cell, median genes per cell, etc.).

See Also
--------

* :doc:`starsolo` -- open-source alternative for 10x-compatible single-cell
  quantification using the STAR aligner
* :doc:`seurat` -- R toolkit for downstream analysis of single-cell count
  matrices
* :doc:`scanpy` -- Python toolkit for downstream analysis and visualisation of
  single-cell data
