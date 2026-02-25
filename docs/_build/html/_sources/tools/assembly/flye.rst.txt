Flye
====

Overview
--------

Flye is a de novo long-read genome assembler designed for PacBio and Oxford
Nanopore Technologies reads. It builds an assembly graph from approximate
repeat graphs and resolves repeats using read overlap information. Flye
handles both raw and corrected reads, supports metagenome mode, and produces
contiguous assemblies with relatively low computational requirements. It is
especially well suited for bacterial and small eukaryotic genomes sequenced
with modern high-accuracy long-read chemistries.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda flye

Basic Usage
-----------

Assemble high-quality Nanopore reads into a bacterial genome, specifying the
expected genome size and using one polishing iteration.

.. code-block:: bash

   flye --nano-hq filtered_reads.fastq.gz \
     --out-dir flye_output/ \
     --genome-size 4.6m \
     --iterations 1 \
     --threads 8

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``--nano-hq``
     - Input reads from ONT high-quality basecalling (Q20+).
   * - ``--nano-raw``
     - Input reads from ONT raw (lower accuracy) basecalling.
   * - ``--pacbio-hifi``
     - Input PacBio HiFi / CCS reads.
   * - ``--out-dir``
     - Directory where all output files will be written.
   * - ``--genome-size``
     - Estimated genome size (e.g. ``4.6m``, ``1g``). Required unless
       ``--meta`` is used.
   * - ``--iterations``
     - Number of polishing iterations to run on the assembly (default 1).
   * - ``--threads``
     - Number of CPU threads to use.
   * - ``--meta``
     - Enable metagenome assembly mode (skips genome size requirement).
   * - ``--min-overlap``
     - Minimum overlap between reads (default auto-detected).

Expected Output
---------------

Flye writes several files to the output directory:

* ``assembly.fasta`` -- the final polished consensus assembly in FASTA format.
* ``assembly_info.txt`` -- a tab-delimited table listing each contig with its
  length, coverage, circularity status, and repeat classification.
* ``assembly_graph.gfa`` -- the assembly graph in GFA format, suitable for
  inspection in tools such as Bandage.
* ``assembly_graph.gv`` -- a Graphviz representation of the assembly graph.

See Also
--------

* :doc:`canu` -- alternative long-read assembler with built-in read
  correction and trimming
* :doc:`medaka` -- neural-network polisher for improving ONT assemblies
* :doc:`/tools/assembly-qc/quast` -- evaluate assembly contiguity and
  correctness against a reference
