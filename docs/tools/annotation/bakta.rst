Bakta
=====

Overview
--------

Bakta is a rapid and comprehensive annotation tool for bacterial genomes. It
identifies coding sequences, rRNAs, tRNAs, ncRNAs, CRISPR arrays, and other
genomic features using a combination of database searches and predictive
models. Bakta relies on a pre-built, regularly updated database that combines
UniProt, AMRFinderPlus, Pfam, and other resources for functional annotation.
It produces standard output formats (GFF3, GenBank, EMBL) that are compatible
with downstream analysis tools and public database submissions.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda bakta

Basic Usage
-----------

Download the Bakta database and annotate a polished bacterial assembly.

.. code-block:: bash

   # Download database
   bakta_db download --output /databases/bakta --type full

   bakta medaka_output/consensus.fasta \
     --db /databases/bakta/db \
     --output bakta_output/ \
     --genus Escherichia --species "coli" \
     --complete \
     --threads 8

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - (positional)
     - Input genome assembly in FASTA format.
   * - ``--db``
     - Path to the Bakta database directory.
   * - ``--output``
     - Output directory for annotation files.
   * - ``--genus`` / ``--species``
     - Taxonomic classification for the organism being annotated.
   * - ``--complete``
     - Flag indicating the assembly represents a complete genome (affects
       feature coordinate handling for circular replicons).
   * - ``--threads``
     - Number of CPU threads to use.
   * - ``--prefix``
     - Prefix for output file names (default derived from input file).
   * - ``--locus-tag``
     - Locus tag prefix for gene identifiers.
   * - ``--min-contig-length``
     - Minimum contig length to annotate (default 1).
   * - ``--keep-contig-headers``
     - Preserve original contig names from the input FASTA.

Expected Output
---------------

Bakta writes multiple annotation files to the output directory:

* ``.gff3`` -- genome annotations in GFF3 format, the most common format
  for downstream tools.
* ``.gbff`` -- GenBank flat file format, suitable for submission to NCBI and
  viewing in genome browsers.
* ``.faa`` -- predicted protein sequences in FASTA format.
* ``.ffn`` -- nucleotide sequences of predicted features in FASTA format.
* ``.embl`` -- annotations in EMBL format for submission to ENA.
* ``.tsv`` -- a tab-separated summary table of all annotated features.
* ``.json`` -- machine-readable annotation results in JSON format.

See Also
--------

* :doc:`prokka` -- alternative prokaryotic annotation pipeline
* :doc:`/tools/assembly/medaka` -- polishing step commonly run before
  annotation
* :doc:`/tools/assembly-qc/busco` -- assess gene-level completeness before
  or after annotation
