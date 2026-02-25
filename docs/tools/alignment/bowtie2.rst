Bowtie2
=======

Overview
--------

Bowtie2 is a fast and memory-efficient short-read aligner that uses an
FM-index based on the Burrows-Wheeler Transform. It supports local and
end-to-end alignment modes and is widely used for ChIP-seq, ATAC-seq, and
other applications where gapped alignment of Illumina reads is needed.
Bowtie2 handles reads of varying lengths and can report multiple alignments
per read when required.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda bowtie2

Basic Usage
-----------

Build a genome index, then align paired-end reads. The example below uses
settings typical for ATAC-seq, with a maximum fragment length of 2000 bp
and the ``--very-sensitive`` preset.

.. code-block:: bash

   # Build index
   bowtie2-build reference.fa reference_index

   # Align paired-end reads (ATAC-seq example with -X 2000)
   bowtie2 -x reference_index \
     -1 sample_R1.fastq.gz -2 sample_R2.fastq.gz \
     -X 2000 --very-sensitive -p 8 \
     | samtools sort -@ 4 -o sample.sorted.bam -

   samtools index sample.sorted.bam

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-x``
     - Basename of the Bowtie2 index (built with ``bowtie2-build``).
   * - ``-1`` / ``-2``
     - Paired-end input FASTQ files (read 1 and read 2).
   * - ``-U``
     - Unpaired (single-end) input FASTQ file.
   * - ``-X``
     - Maximum fragment length for valid paired-end alignments (default 500).
       Increase for ATAC-seq.
   * - ``--very-sensitive``
     - Preset that maximises alignment sensitivity (slower). Equivalent to
       ``-D 20 -R 3 -N 0 -L 20 -i S,1,0.50``.
   * - ``--local``
     - Use local alignment mode (soft-clips read ends rather than penalising
       mismatches at the ends).
   * - ``-p``
     - Number of alignment threads.
   * - ``--no-mixed``
     - Suppress unpaired alignments for reads that cannot be aligned
       concordantly as a pair.
   * - ``--no-discordant``
     - Suppress discordant alignments for paired-end reads.
   * - ``--rg-id``
     - Set the read group ID. Combine with ``--rg`` to set additional read
       group fields.
   * - ``-k``
     - Report up to this many alignments per read (default: best alignment
       only).

Expected Output
---------------

The pipeline above produces:

* ``sample.sorted.bam`` -- a coordinate-sorted BAM file containing all
  aligned and unaligned reads.
* ``sample.sorted.bam.bai`` -- the BAM index file.

Bowtie2 prints alignment summary statistics to standard error, including the
total number of reads, the overall alignment rate, the number of reads that
aligned concordantly, and the number that aligned discordantly.

Verify the alignment with:

.. code-block:: bash

   samtools flagstat sample.sorted.bam

See Also
--------

* :doc:`bwa-mem2` -- alternative short-read aligner, often preferred for
  whole-genome and whole-exome sequencing
* :doc:`star` -- splice-aware aligner for RNA-seq data
* :doc:`/tools/sam-bam-processing/index` -- tools for post-alignment BAM
  processing
* :doc:`/tools/epigenomics/index` -- downstream analysis tools for ATAC-seq
  and ChIP-seq
* :doc:`/data-formats/fastq` -- reference for the FASTQ file format
* :doc:`/data-formats/sam-bam-cram` -- reference for the SAM/BAM/CRAM
  alignment format
