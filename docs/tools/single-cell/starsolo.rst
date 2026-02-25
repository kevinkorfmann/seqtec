STARsolo
========

Overview
--------

STARsolo is a module of the STAR aligner that provides a drop-in, open-source
replacement for Cell Ranger's gene expression quantification. It maps reads to
a reference genome and demultiplexes cell barcodes and UMIs in a single pass,
producing cell-by-gene count matrices compatible with downstream tools such as
Seurat and Scanpy. STARsolo reproduces Cell Ranger results while offering
substantially faster runtimes and greater flexibility for non-10x protocols.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda star

Basic Usage
-----------

Align reads from a 10x Chromium 3' v3 library and produce gene expression
count matrices. Note that Read 2 (cDNA) is provided first, followed by
Read 1 (barcode + UMI).

.. code-block:: bash

   STAR --runMode alignReads \
     --genomeDir star_index/ \
     --readFilesIn sample_R2.fastq.gz sample_R1.fastq.gz \
     --readFilesCommand zcat \
     --soloType CB_UMI_Simple \
     --soloCBstart 1 --soloCBlen 16 \
     --soloUMIstart 17 --soloUMIlen 12 \
     --soloCBwhitelist 3M-february-2018.txt \
     --soloCellFilter EmptyDrops_CR \
     --soloFeatures Gene GeneFull \
     --outSAMtype BAM SortedByCoordinate \
     --runThreadN 16

Before running, build the STAR genome index if it does not yet exist:

.. code-block:: bash

   STAR --runMode genomeGenerate \
     --genomeDir star_index/ \
     --genomeFastaFiles GRCh38.fa \
     --sjdbGTFfile genes.gtf \
     --runThreadN 16

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``--genomeDir``
     - Path to the STAR genome index directory.
   * - ``--readFilesIn``
     - Input FASTQ files. For 10x data, provide the cDNA read first, then the
       barcode/UMI read.
   * - ``--readFilesCommand``
     - Command for decompressing input files (``zcat`` for ``.gz``).
   * - ``--soloType``
     - Barcode/UMI layout type (``CB_UMI_Simple`` for standard 10x protocols).
   * - ``--soloCBstart`` / ``--soloCBlen``
     - Start position and length of the cell barcode within Read 1.
   * - ``--soloUMIstart`` / ``--soloUMIlen``
     - Start position and length of the UMI within Read 1.
   * - ``--soloCBwhitelist``
     - Path to the barcode whitelist (e.g., ``3M-february-2018.txt`` for
       Chromium v3).
   * - ``--soloCellFilter``
     - Cell-calling algorithm (``EmptyDrops_CR`` matches Cell Ranger behaviour).
   * - ``--soloFeatures``
     - Which features to quantify (``Gene`` for exonic, ``GeneFull`` for
       exonic + intronic).
   * - ``--outSAMtype``
     - Output format (``BAM SortedByCoordinate`` produces a sorted BAM file).
   * - ``--runThreadN``
     - Number of threads to use for alignment.

Expected Output
---------------

STARsolo writes output into the default ``Solo.out/`` directory:

* ``Solo.out/Gene/filtered/`` -- filtered count matrix in MEX format
  (``matrix.mtx``, ``barcodes.tsv``, ``features.tsv``), directly loadable by
  Seurat or Scanpy.
* ``Solo.out/Gene/raw/`` -- unfiltered matrix containing all detected barcodes.
* ``Solo.out/GeneFull/filtered/`` -- count matrix including intronic reads
  (useful for single-nucleus RNA-seq).
* ``Aligned.sortedByCoord.out.bam`` -- coordinate-sorted BAM file with barcode
  and UMI tags.
* ``Log.final.out`` -- alignment summary statistics (mapping rate, unique vs.
  multi-mapped reads).

See Also
--------

* :doc:`cellranger` -- the official 10x Genomics pipeline with integrated
  reporting
* :doc:`seurat` -- R toolkit for downstream single-cell analysis
* :doc:`scanpy` -- Python framework for single-cell analysis and visualisation
* :doc:`/tools/alignment/index` -- general-purpose alignment tools
