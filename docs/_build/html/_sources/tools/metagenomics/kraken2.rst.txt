Kraken2
=======

Overview
--------

Kraken2 is an ultrafast taxonomic classification tool for metagenomic
sequencing reads. It assigns a taxonomic label to each read by matching exact
k-mer sequences against a pre-built database of known genomes. Kraken2 uses a
compact hash table that maps k-mers to the lowest common ancestor (LCA) of all
genomes containing that k-mer, achieving classification speeds of millions of
reads per minute. It is the standard first step in many metagenomics workflows
for determining the taxonomic composition of a sample.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda kraken2

Basic Usage
-----------

Download a pre-built standard database and classify sequencing reads.

.. code-block:: bash

   # Download pre-built database
   wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20240112.tar.gz
   mkdir -p kraken2_db && tar -xzf k2_standard_20240112.tar.gz -C kraken2_db/

   # Classify reads
   kraken2 --db kraken2_db/ \
     --output classifications.txt \
     --report report.txt \
     --minimum-hit-groups 3 \
     --threads 8 \
     reads.fastq.gz

For paired-end reads, add the ``--paired`` flag and provide both FASTQ files:

.. code-block:: bash

   kraken2 --db kraken2_db/ --paired \
     --output classifications.txt \
     --report report.txt \
     --minimum-hit-groups 3 \
     --threads 8 \
     reads_R1.fastq.gz reads_R2.fastq.gz

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``--db``
     - Path to the Kraken2 database directory.
   * - ``--output``
     - Per-read classification output file (read ID, taxon ID, k-mer mapping
       details).
   * - ``--report``
     - Summary report with read counts and percentages at each taxonomic level.
   * - ``--minimum-hit-groups``
     - Minimum number of hit groups needed to make a classification call.
       Higher values improve precision at the cost of sensitivity.
   * - ``--confidence``
     - Confidence score threshold (0--1) for classification. Reads below this
       threshold are marked unclassified.
   * - ``--paired``
     - Input reads are paired-end.
   * - ``--threads``
     - Number of threads for classification.
   * - ``--unclassified-out``
     - Write unclassified reads to the specified file.
   * - ``--classified-out``
     - Write classified reads to the specified file.

Expected Output
---------------

* ``classifications.txt`` -- tab-delimited file with one line per read,
  containing the classification status (C/U), read ID, assigned taxon ID,
  read length, and k-mer-to-taxon mapping.
* ``report.txt`` -- Kraken-style report with columns for percentage of reads,
  number of reads rooted at a taxon, number of reads directly assigned, rank
  code, taxon ID, and taxon name. This report is used as input for Bracken
  abundance estimation and Krona visualisation.

See Also
--------

* :doc:`bracken` -- re-estimates species-level abundance from Kraken2 reports
  using Bayesian methods
* :doc:`krona` -- generates interactive HTML taxonomic visualisations from
  Kraken2 reports
