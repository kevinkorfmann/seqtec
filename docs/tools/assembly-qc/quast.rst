QUAST
=====

Overview
--------

QUAST (Quality Assessment Tool for Genome Assemblies) evaluates genome
assembly quality by computing a wide range of contiguity and correctness
metrics. When a reference genome is provided, QUAST reports misassemblies,
mismatches, indels, and genome fraction covered. Without a reference, it still
provides useful statistics such as N50, L50, total length, and number of
contigs. QUAST generates interactive HTML reports and machine-readable TSV
tables, making it suitable for both manual inspection and automated pipelines.
It can compare multiple assemblies side by side, which is helpful for
benchmarking different assemblers or parameter settings.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda quast

Basic Usage
-----------

Evaluate a polished assembly against a reference genome downloaded from NCBI.

.. code-block:: bash

   # Download reference for comparison
   wget -q https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz
   gunzip GCF_000005845.2_ASM584v2_genomic.fna.gz

   quast medaka_output/consensus.fasta \
     -r reference.fna \
     -o quast_output/ \
     --threads 4

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - (positional)
     - One or more assembly FASTA files to evaluate.
   * - ``-r``
     - Reference genome in FASTA format for computing correctness metrics.
   * - ``-o``
     - Output directory for the report files.
   * - ``--threads``
     - Number of CPU threads to use.
   * - ``--min-contig``
     - Minimum contig length to include in the analysis (default 500).
   * - ``-g``
     - Reference gene annotations in GFF format for computing gene-level
       metrics.
   * - ``--large``
     - Use settings optimised for large genomes (> 100 Mb).
   * - ``--gene-finding``
     - Run built-in gene prediction (GeneMarkS for prokaryotes) to estimate
       gene counts without external annotations.

Expected Output
---------------

QUAST writes several report files to the output directory:

* ``report.html`` -- an interactive HTML report with tables and Icarus
  contig browser for visual inspection.
* ``report.tsv`` -- a tab-separated summary of all assembly metrics.
* ``report.txt`` -- a plain-text version of the summary table.
* ``icarus.html`` -- the Icarus genome viewer showing contig alignment to
  the reference.
* ``transposed_report.tsv`` -- the same metrics transposed for easier
  parsing when comparing multiple assemblies.

Key metrics in the report include total assembly length, number of contigs,
largest contig, N50/N75, L50/L75, GC content, genome fraction covered,
number of misassemblies, mismatches per 100 kb, and indels per 100 kb.

See Also
--------

* :doc:`busco` -- complementary assessment based on conserved gene content
* :doc:`/tools/assembly/flye` -- long-read assembler whose output is
  commonly evaluated with QUAST
* :doc:`/tools/assembly/medaka` -- polishing tool often used before running
  QUAST
