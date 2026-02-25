SPAdes
======

Overview
--------

SPAdes (St. Petersburg genome Assembler) is a versatile de Bruijn graph-based
assembler designed for small genomes such as bacteria, fungi, and other
microorganisms. It uses multiple k-mer sizes to build and merge assembly
graphs, which helps resolve repeats and low-coverage regions. SPAdes supports
Illumina short reads, IonTorrent data, and hybrid assembly when long reads
(PacBio or Nanopore) are available alongside short reads. The ``--careful``
mode runs an additional mismatch correction step that reduces errors in the
final contigs.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda spades

Basic Usage
-----------

Assemble a bacterial genome from paired-end Illumina reads using the careful
mismatch correction mode.

.. code-block:: bash

   # Bacterial genome assembly with short reads
   spades.py -1 sample_R1.fastq.gz -2 sample_R2.fastq.gz \
     -o spades_output/ --careful -t 8 -m 32

Hybrid assembly combining short reads with Nanopore long reads for improved
contiguity.

.. code-block:: bash

   # Hybrid assembly (short + long reads)
   spades.py -1 short_R1.fastq.gz -2 short_R2.fastq.gz \
     --nanopore long_reads.fastq.gz \
     -o spades_hybrid/ -t 8

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``-1`` / ``-2``
     - Input paired-end FASTQ files (read 1 and read 2).
   * - ``-s``
     - Input single-end / unpaired reads.
   * - ``--nanopore``
     - Nanopore long reads for hybrid assembly.
   * - ``--pacbio``
     - PacBio long reads for hybrid assembly.
   * - ``-o``
     - Output directory for all assembly results.
   * - ``--careful``
     - Run MismatchCorrector post-processing to reduce mismatches and
       short indels in the final contigs.
   * - ``-t``
     - Number of CPU threads (default 16).
   * - ``-m``
     - Memory limit in gigabytes (default 250).
   * - ``-k``
     - Comma-separated list of k-mer sizes (default auto-selected).
   * - ``--isolate``
     - Mode optimised for high-coverage isolate genomes.

Expected Output
---------------

SPAdes writes output to the specified directory:

* ``contigs.fasta`` -- assembled contigs in FASTA format.
* ``scaffolds.fasta`` -- scaffolded sequences produced from the contigs.
* ``assembly_graph_with_scaffolds.gfa`` -- the assembly graph in GFA format.
* ``spades.log`` -- detailed log of the assembly run with timing and
  parameter information.
* ``K21/``, ``K33/``, ``K55/``, ... -- intermediate assemblies for each
  k-mer size used.

See Also
--------

* :doc:`unicycler` -- hybrid assembler built on SPAdes that is optimised for
  producing complete bacterial genomes
* :doc:`flye` -- long-read assembler for Nanopore and PacBio data
* :doc:`/tools/assembly-qc/quast` -- evaluate assembly contiguity and
  correctness against a reference
