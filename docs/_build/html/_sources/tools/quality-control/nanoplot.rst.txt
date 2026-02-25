NanoPlot
========

Overview
--------

NanoPlot is a plotting and statistics tool designed for long-read sequencing
data from Oxford Nanopore and PacBio platforms. It generates publication-ready
figures showing read length distributions, quality score distributions,
read-length vs quality scatter plots, and yield-over-time plots. NanoPlot
accepts multiple input formats including FASTQ, BAM, and the
``sequencing_summary.txt`` file produced by the Oxford Nanopore basecaller.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda nanoplot

Basic Usage
-----------

NanoPlot supports several input formats. Choose the one that best matches
your data.

.. code-block:: bash

   # From BAM file (recommended for nanopore)
   NanoPlot --bam reads.bam -o nanoplot_output/ --plots dot kde

   # From FASTQ
   NanoPlot --fastq reads.fastq.gz -o nanoplot_output/ --N50 --loglength

   # From sequencing_summary.txt
   NanoPlot --summary sequencing_summary.txt -o nanoplot_output/

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``--bam``
     - Input BAM file(s) for analysis.
   * - ``--fastq``
     - Input FASTQ file(s) for analysis.
   * - ``--summary``
     - Input sequencing_summary.txt from the Oxford Nanopore basecaller.
   * - ``-o``
     - Output directory for plots and statistics.
   * - ``--plots``
     - Plot types to generate (e.g., ``dot``, ``kde``, ``hex``).
   * - ``--N50``
     - Show the N50 mark in the read length histogram.
   * - ``--loglength``
     - Use a log-transformed x-axis for read length plots.
   * - ``--maxlength``
     - Filter out reads longer than this value.
   * - ``--minlength``
     - Filter out reads shorter than this value.
   * - ``--minqual``
     - Filter out reads with average quality below this value.
   * - ``-t`` / ``--threads``
     - Number of threads for BAM file reading.
   * - ``--title``
     - Custom title for the report.

Expected Output
---------------

NanoPlot creates several files in the output directory:

* ``NanoPlot-report.html`` -- a self-contained HTML report with all figures
  and summary statistics.
* ``NanoStats.txt`` -- a text file with summary statistics including mean
  read length, median read length, N50, mean quality, total bases, and number
  of reads.
* A set of PNG and, optionally, SVG plot files:

  - ``LengthvsQualityScatterPlot`` -- scatter plot of read length vs average
    quality.
  - ``Non_weightedHistogramReadlength`` -- histogram of read lengths.
  - ``WeightedHistogramReadlength`` -- histogram of read lengths weighted by
    number of bases.
  - ``Non_weightedLogTransformed_HistogramReadlength`` -- log-scaled length
    histogram (when ``--loglength`` is used).
  - ``Yield_By_Length`` -- cumulative yield as a function of read length.

See Also
--------

* :doc:`pycoqc` -- alternative long-read QC tool that uses the
  sequencing_summary file
* :doc:`chopper` -- quality and length filtering for long reads
* :doc:`/data-formats/fastq` -- reference for the FASTQ file format
