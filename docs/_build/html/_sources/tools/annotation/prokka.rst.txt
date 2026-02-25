Prokka
======

Overview
--------

Prokka is a widely used command-line tool for rapid annotation of prokaryotic
genomes. It coordinates several external feature-prediction tools -- including
Prodigal for coding sequences, Aragorn for tRNAs, RNAmmer for rRNAs, and
SignalP for signal peptides -- and produces standardised output files suitable
for database submission and downstream analysis. Prokka is fast, typically
annotating a bacterial genome in under ten minutes, and requires no external
database download beyond its bundled reference data.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda prokka

Basic Usage
-----------

Annotate a consensus assembly, specifying the output directory, file prefix,
and organism taxonomy.

.. code-block:: bash

   prokka consensus.fasta \
     --outdir prokka_output/ \
     --prefix sample \
     --genus Escherichia --species "coli" \
     --cpus 8

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - (positional)
     - Input genome assembly in FASTA format.
   * - ``--outdir``
     - Output directory for all annotation files.
   * - ``--prefix``
     - Prefix used for output file names (e.g. ``sample``).
   * - ``--genus`` / ``--species``
     - Organism taxonomy used for annotation and output metadata.
   * - ``--cpus``
     - Number of CPU threads to use.
   * - ``--kingdom``
     - Annotation kingdom: ``Bacteria`` (default), ``Archaea``, or
       ``Viruses``.
   * - ``--locustag``
     - Locus tag prefix for gene identifiers.
   * - ``--compliant``
     - Force GenBank/ENA/DDBJ compliance in output files.
   * - ``--rfam``
     - Enable searching for ncRNAs using the Rfam database (slower but
       more comprehensive).
   * - ``--proteins``
     - Path to a trusted protein FASTA or GenBank file for first-pass
       annotation against a custom database.

Expected Output
---------------

Prokka writes output files to the specified directory, all sharing the
prefix given with ``--prefix``:

* ``sample.gff`` -- annotations in GFF3 format with the genome sequence
  appended.
* ``sample.gbk`` -- annotations in GenBank format.
* ``sample.faa`` -- predicted protein sequences in FASTA format.
* ``sample.ffn`` -- nucleotide sequences of predicted features in FASTA
  format.
* ``sample.fna`` -- input genome sequence (may be re-named).
* ``sample.tsv`` -- a tab-separated summary of all annotated features.
* ``sample.txt`` -- a plain-text statistics summary with counts of each
  feature type.
* ``sample.log`` -- the Prokka log file with runtime details.

See Also
--------

* :doc:`bakta` -- newer prokaryotic annotator with a more comprehensive
  and regularly updated database
* :doc:`/tools/assembly/medaka` -- polishing step commonly run before
  annotation
* :doc:`/tools/assembly-qc/busco` -- assess gene-level completeness of the
  annotated assembly
