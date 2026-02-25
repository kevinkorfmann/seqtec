BUSCO
=====

Overview
--------

BUSCO (Benchmarking Universal Single-Copy Orthologs) assesses genome assembly
and annotation completeness by searching for a set of highly conserved
single-copy genes expected to be present in a given lineage. It reports the
fraction of these marker genes found as complete, duplicated, fragmented, or
missing, providing a biologically meaningful measure of assembly quality that
complements purely statistical metrics like N50. BUSCO supports genome,
transcriptome, and protein-level assessments and includes lineage-specific
databases spanning bacteria, archaea, fungi, plants, and animals.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda busco

Basic Usage
-----------

Evaluate a polished bacterial assembly for gene completeness using the
Enterobacterales lineage database.

.. code-block:: bash

   busco -i medaka_output/consensus.fasta \
     -o busco_output/ \
     -m genome \
     -l enterobacterales_odb10 \
     --cpu 8

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-i``
     - Input sequence file (genome FASTA, transcriptome FASTA, or protein
       FASTA).
   * - ``-o``
     - Output directory name for BUSCO results.
   * - ``-m``
     - Assessment mode: ``genome``, ``transcriptome``, or ``proteins``.
   * - ``-l``
     - Lineage dataset to use (e.g. ``enterobacterales_odb10``,
       ``mammalia_odb10``). Use ``busco --list-datasets`` to see all
       available lineages.
   * - ``--cpu``
     - Number of CPU threads to use.
   * - ``--auto-lineage``
     - Automatically detect the most appropriate lineage dataset.
   * - ``--auto-lineage-prok``
     - Automatic lineage selection restricted to prokaryotic datasets.
   * - ``-f``
     - Force overwrite of existing output directory.
   * - ``--download_path``
     - Path where lineage databases are stored or will be downloaded.

Expected Output
---------------

BUSCO writes results to the specified output directory:

* ``short_summary.specific.<lineage>.<output>.txt`` -- a concise text
  summary reporting the number and percentage of complete (single-copy and
  duplicated), fragmented, and missing BUSCOs.
* ``full_table.tsv`` -- a detailed table listing each BUSCO marker gene and
  its status (Complete, Duplicated, Fragmented, or Missing).
* ``missing_busco_list.tsv`` -- list of BUSCO IDs that were not found.
* ``busco_sequences/`` -- directory containing the nucleotide and protein
  sequences of identified BUSCO genes.

A high-quality bacterial assembly typically shows >95% complete BUSCOs with
very few fragmented or missing genes.

See Also
--------

* :doc:`quast` -- complementary assembly evaluation based on contiguity and
  reference alignment metrics
* :doc:`/tools/assembly/medaka` -- polishing tool often used before running
  BUSCO to improve completeness
* :doc:`/tools/annotation/bakta` -- genome annotation that can be evaluated
  with BUSCO in protein mode
