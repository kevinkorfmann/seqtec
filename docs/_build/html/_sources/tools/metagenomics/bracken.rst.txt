Bracken
=======

Overview
--------

Bracken (Bayesian Reestimation of Abundance with KrakEN) refines taxonomic
abundance estimates from Kraken2 classification reports. Kraken2 assigns reads
to the lowest common ancestor when k-mers match multiple taxa, which can
inflate counts at higher taxonomic levels. Bracken uses a Bayesian model built
from the read-length distribution of each genome in the database to
probabilistically redistribute reads from higher-level taxa down to species
(or genus) level, producing more accurate relative abundance estimates.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda bracken

Basic Usage
-----------

Build the Bracken database (a one-time step per Kraken2 database and read
length), then estimate species-level abundance from a Kraken2 report.

.. code-block:: bash

   # Build Bracken database (one-time)
   bracken-build -d kraken2_db/ -t 8 -k 35 -l 1000

   # Estimate species abundance
   bracken -d kraken2_db/ \
     -i report.txt \
     -o bracken_output.txt \
     -r 1000 -l S -t 10

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-d``
     - Path to the Kraken2 database directory (must contain the Bracken
       database files after running ``bracken-build``).
   * - ``-i``
     - Input Kraken2 report file (the ``--report`` output from Kraken2).
   * - ``-o``
     - Output file for re-estimated abundance values.
   * - ``-r``
     - Read length used during sequencing (must match the ``-l`` value used
       when building the Bracken database).
   * - ``-l``
     - Taxonomic level for re-estimation: ``S`` (species), ``G`` (genus),
       ``F`` (family), ``O`` (order), ``C`` (class), ``P`` (phylum),
       ``D`` (domain).
   * - ``-t``
     - Minimum number of reads assigned to a taxon to include it in the
       output. Taxa below this threshold are excluded.

Expected Output
---------------

* ``bracken_output.txt`` -- tab-delimited file with columns for taxon name,
  taxonomy ID, taxonomy level, Kraken-assigned reads, added reads (from
  redistribution), new total reads, and fraction of total reads. Each row
  represents one taxon at the requested level.
* ``bracken_output.txt_bracken_species.kreport`` -- an updated Kraken-style
  report reflecting the re-estimated abundances, suitable for downstream
  visualisation tools.

See Also
--------

* :doc:`kraken2` -- the upstream classifier that produces the input report for
  Bracken
* :doc:`krona` -- interactive taxonomic visualisation of Bracken or Kraken2
  results
