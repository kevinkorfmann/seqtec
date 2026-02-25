minimap2
========

Overview
--------

minimap2 is a versatile sequence alignment tool designed for mapping long
noisy reads (Oxford Nanopore, PacBio), short reads, and spliced reads
(RNA-seq) to a reference genome. It supports a wide range of presets
optimised for different data types (``map-ont``, ``map-hifi``, ``map-pb``,
``sr``, ``splice``) and is substantially faster than its predecessor
minimap while maintaining high accuracy. minimap2 is the de facto standard
aligner for long-read sequencing data.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda minimap2

Basic Usage
-----------

Download a reference, index it, align nanopore reads, and produce a sorted
BAM file.

.. code-block:: bash

   # Download and index reference
   wget -q https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/005/845/GCA_000005845.2_ASM584v2/GCA_000005845.2_ASM584v2_genomic.fna.gz
   gunzip GCA_000005845.2_ASM584v2_genomic.fna.gz
   samtools faidx reference.fna

   # Align nanopore reads
   minimap2 -ax map-ont --MD \
     -R '@RG\tID:sample1\tSM:sample1\tPL:ONT' \
     reference.fna reads.fastq.gz \
     | samtools sort -@ 4 -o aligned.sorted.bam -

   samtools index aligned.sorted.bam

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-a``
     - Output in SAM format (required when piping to samtools).
   * - ``-x``
     - Preset for the data type. Common values:

       - ``map-ont`` -- Oxford Nanopore reads
       - ``map-hifi`` -- PacBio HiFi reads
       - ``map-pb`` -- PacBio CLR reads
       - ``sr`` -- short (Illumina) reads
       - ``splice`` -- long-read RNA-seq
   * - ``--MD``
     - Include the MD tag for reference base information (needed by some
       variant callers).
   * - ``-R``
     - Read group header line (e.g.,
       ``'@RG\tID:sample1\tSM:sample1\tPL:ONT'``).
   * - ``-t``
     - Number of alignment threads (default 3).
   * - ``-d``
     - Save the index to a file for reuse with large genomes.
   * - ``-k``
     - Minimizer k-mer length (preset-dependent).
   * - ``-w``
     - Minimizer window size (preset-dependent).
   * - ``--secondary=no``
     - Do not output secondary alignments.
   * - ``-Y``
     - Use soft clipping for supplementary alignments.

Expected Output
---------------

The pipeline above produces:

* ``aligned.sorted.bam`` -- a coordinate-sorted BAM file with all aligned
  and unaligned reads.
* ``aligned.sorted.bam.bai`` -- the BAM index for fast random access.

Verify alignment statistics with:

.. code-block:: bash

   samtools flagstat aligned.sorted.bam

This reports total reads, mapped reads, primary and supplementary alignments,
and properly paired reads (if applicable).

See Also
--------

* :doc:`bwa-mem2` -- optimised short-read aligner for Illumina data
* :doc:`/tools/quality-control/nanoplot` -- visualise read quality and length
  distributions for long-read data
* :doc:`/tools/quality-control/chopper` -- quality and length filtering
  before alignment
* :doc:`/data-formats/fastq` -- reference for the FASTQ file format
* :doc:`/data-formats/sam-bam-cram` -- reference for the SAM/BAM/CRAM
  alignment format
