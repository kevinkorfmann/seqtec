Krona
=====

Overview
--------

Krona produces interactive, multi-layered pie charts for exploring hierarchical
taxonomic classifications in a web browser. It takes tabular taxonomic data
(such as Kraken2 or Bracken reports) and generates a self-contained HTML file
where users can zoom into any taxonomic level, view proportions, and search for
specific taxa. Krona visualisations are widely used to communicate the
composition of metagenomic samples in publications and presentations.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda krona

After installation, update the NCBI taxonomy database used by Krona:

.. code-block:: bash

   ktUpdateTaxonomy.sh

Basic Usage
-----------

Convert a Kraken2 report to Krona input format and create an interactive HTML
visualisation.

.. code-block:: bash

   # Convert Kraken2 report to Krona format
   kreport2krona.py -r report.txt -o krona_input.txt

   # Create interactive visualization
   ktImportText krona_input.txt -o krona_report.html

The resulting ``krona_report.html`` can be opened directly in any web browser.

To visualise multiple samples in a single chart:

.. code-block:: bash

   kreport2krona.py -r sample1_report.txt -o sample1_krona.txt
   kreport2krona.py -r sample2_report.txt -o sample2_krona.txt
   ktImportText sample1_krona.txt sample2_krona.txt -o combined_krona.html

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-r`` (kreport2krona.py)
     - Input Kraken2 or Bracken report file.
   * - ``-o`` (kreport2krona.py)
     - Output file in Krona-compatible tab-delimited format.
   * - ``-o`` (ktImportText)
     - Output HTML file name.
   * - ``-n`` (ktImportText)
     - Name for the root node of the chart.
   * - ``-q`` (ktImportText)
     - Column number for the query count (default: first column).

Expected Output
---------------

* ``krona_input.txt`` -- intermediate tab-delimited file with read counts and
  taxonomic lineage columns.
* ``krona_report.html`` -- self-contained interactive HTML file. The
  visualisation shows a hierarchical pie chart where each ring represents a
  taxonomic level (domain, phylum, class, order, family, genus, species).
  Users can click to zoom into any taxon and use the search box to highlight
  specific organisms.

See Also
--------

* :doc:`kraken2` -- upstream classifier that produces the reports visualised
  by Krona
* :doc:`bracken` -- refines Kraken2 abundance estimates before visualisation
