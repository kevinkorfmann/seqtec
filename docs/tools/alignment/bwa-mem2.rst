BWA-MEM2
========

Overview
--------

BWA-MEM2 is a highly optimised re-implementation of the BWA-MEM short-read
aligner. It uses SIMD (Single Instruction, Multiple Data) acceleration to
deliver significantly faster alignment speeds while producing identical
output to the original BWA-MEM. BWA-MEM2 is the recommended aligner for
mapping Illumina whole-genome sequencing, whole-exome sequencing, and other
short-read data to a reference genome.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda bwa-mem2

Basic Usage
-----------

Index the reference genome, align paired-end reads, and sort the output into
a coordinate-sorted BAM file.

.. code-block:: bash

   # Index reference genome
   bwa-mem2 index /ref/GRCh38.fa

   # Align paired-end reads
   bwa-mem2 mem -t 16 /ref/GRCh38.fa \
     sample_R1.fastq.gz sample_R2.fastq.gz \
     | samtools sort -@ 4 -o sample.sorted.bam -

   samtools index sample.sorted.bam

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-t``
     - Number of alignment threads (default 1).
   * - ``-R``
     - Read group header line (e.g.,
       ``'@RG\tID:sample\tSM:sample\tPL:ILLUMINA'``). Required for
       downstream variant calling.
   * - ``-M``
     - Mark shorter split hits as secondary (for Picard compatibility).
   * - ``-k``
     - Minimum seed length (default 19). Lower values increase sensitivity
       at the cost of speed.
   * - ``-w``
     - Band width for banded alignment (default 100).
   * - ``-A``
     - Matching score (default 1).
   * - ``-B``
     - Mismatch penalty (default 4).
   * - ``-O``
     - Gap open penalty (default 6,6).
   * - ``-E``
     - Gap extension penalty (default 1,1).
   * - ``-Y``
     - Use soft clipping for supplementary alignments.

Expected Output
---------------

The pipeline above produces:

* ``sample.sorted.bam`` -- a coordinate-sorted BAM file containing all
  aligned and unaligned reads.
* ``sample.sorted.bam.bai`` -- the BAM index file created by
  ``samtools index``.

Verify the alignment with ``samtools flagstat``:

.. code-block:: bash

   samtools flagstat sample.sorted.bam

This prints the total number of reads, mapped reads, properly paired reads,
and other alignment statistics.

See Also
--------

* :doc:`bowtie2` -- alternative short-read aligner often used for ChIP-seq
  and ATAC-seq
* :doc:`minimap2` -- long-read and splice-aware aligner for nanopore and
  PacBio data
* :doc:`/tools/sam-bam-processing/index` -- tools for post-alignment BAM
  processing (sorting, deduplication, filtering)
* :doc:`/data-formats/fastq` -- reference for the FASTQ file format
* :doc:`/data-formats/sam-bam-cram` -- reference for the SAM/BAM/CRAM
  alignment format
