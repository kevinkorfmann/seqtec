Unicycler
=========

Overview
--------

Unicycler is a hybrid assembler specifically designed for bacterial genomes.
It combines short Illumina reads with long reads from Oxford Nanopore or
PacBio to produce complete, circularised chromosomes and plasmids. Unicycler
first builds a short-read assembly graph using SPAdes, then uses long reads to
resolve repeats and bridge gaps in the graph. It can also operate in
short-read-only mode, where it functions as an optimised SPAdes pipeline with
additional graph-cleaning heuristics. Unicycler assigns quality scores to
completed replicons, making it straightforward to assess which contigs are
fully resolved.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda unicycler

Basic Usage
-----------

Perform a hybrid assembly using paired-end short reads and long reads.

.. code-block:: bash

   # Hybrid assembly
   unicycler -1 short_R1.fastq.gz -2 short_R2.fastq.gz \
     -l long_reads.fastq.gz \
     -o unicycler_output/ -t 8

Assemble a bacterial genome from short reads only.

.. code-block:: bash

   # Short-read only
   unicycler -1 short_R1.fastq.gz -2 short_R2.fastq.gz \
     -o unicycler_output/ -t 8

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-1`` / ``-2``
     - Input paired-end short-read FASTQ files (read 1 and read 2).
   * - ``-l``
     - Input long reads (Nanopore or PacBio) for hybrid assembly.
   * - ``-o``
     - Output directory for all assembly results.
   * - ``-t``
     - Number of CPU threads to use.
   * - ``--mode``
     - Assembly stringency: ``conservative``, ``normal`` (default), or
       ``bold``. Bold mode resolves more repeats but may introduce errors.
   * - ``--min_fasta_length``
     - Minimum contig length to include in the final output (default 100).
   * - ``--linear_seqs``
     - Expected number of linear sequences (default 0, assumes circular
       chromosomes and plasmids).
   * - ``--no_rotate``
     - Do not rotate completed circular sequences to start at a standard
       gene (e.g. dnaA).

Expected Output
---------------

Unicycler writes output to the specified directory:

* ``assembly.fasta`` -- the final assembly containing both complete and
  incomplete replicons in FASTA format.
* ``assembly.gfa`` -- the final assembly graph in GFA format, viewable in
  Bandage.
* ``unicycler.log`` -- a detailed log file recording every step of the
  assembly pipeline including SPAdes k-mer iterations, graph cleaning, and
  long-read bridging.

Each contig header in the FASTA output includes length, depth (coverage), and
circularity status, allowing rapid identification of complete replicons.

See Also
--------

* :doc:`spades` -- the underlying short-read assembler used by Unicycler
* :doc:`flye` -- long-read-only assembler as an alternative for Nanopore or
  PacBio data
* :doc:`/tools/assembly-qc/busco` -- assess gene-level completeness of the
  assembly
