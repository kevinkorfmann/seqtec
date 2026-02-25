Canu
====

Overview
--------

Canu is a de novo long-read assembler derived from the Celera Assembler. It
provides an integrated pipeline that corrects, trims, and assembles PacBio or
Oxford Nanopore reads in a single workflow. Canu is designed to handle noisy
long reads and uses adaptive k-mer weighting and three-stage processing
(correction, trimming, assembly) to produce high-quality contigs. It works
well for bacterial genomes and moderately sized eukaryotic genomes, and it can
operate on compute clusters via built-in grid engine support.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda canu

Basic Usage
-----------

Assemble a bacterial genome from Nanopore reads, specifying a prefix for
output files and the estimated genome size.

.. code-block:: bash

   canu -p ecoli -d canu_output/ \
     genomeSize=4.6m \
     -nanopore reads.fastq.gz \
     maxThreads=8

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``-p``
     - Prefix for output file names (e.g. ``ecoli``).
   * - ``-d``
     - Directory where all output files will be written.
   * - ``genomeSize=``
     - Estimated genome size (e.g. ``4.6m``, ``1g``).
   * - ``-nanopore``
     - Input Oxford Nanopore reads.
   * - ``-pacbio-hifi``
     - Input PacBio HiFi / CCS reads.
   * - ``maxThreads=``
     - Maximum number of CPU threads to use.
   * - ``correctedErrorRate=``
     - Expected error rate after correction (lower values produce more
       stringent overlap filtering).
   * - ``minReadLength=``
     - Minimum read length to use in the assembly (default 1000).
   * - ``stopOnLowCoverage=``
     - Minimum coverage threshold below which Canu will stop and warn.

Expected Output
---------------

Canu writes output to the specified directory using the prefix from ``-p``:

* ``ecoli.contigs.fasta`` -- the final assembled contigs in FASTA format.
* ``ecoli.report`` -- a summary report with assembly statistics including
  read correction rates, overlap counts, and contig metrics.
* ``ecoli.unassembled.fasta`` -- reads that could not be placed into contigs.
* ``ecoli.contigs.gfa`` -- the assembly graph in GFA format.
* ``ecoli.contigs.layout.tigInfo`` -- detailed information about each contig
  including length and coverage.

See Also
--------

* :doc:`flye` -- alternative long-read assembler with fast repeat-graph
  approach
* :doc:`medaka` -- neural-network polisher for improving ONT assemblies
* :doc:`/tools/assembly-qc/quast` -- evaluate assembly contiguity and
  correctness against a reference
