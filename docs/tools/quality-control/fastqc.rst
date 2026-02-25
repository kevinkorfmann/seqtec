FastQC
======

Overview
--------

FastQC is a widely used quality control tool that generates a comprehensive
report for raw or trimmed sequencing data. It analyses base quality scores,
GC content, sequence duplication levels, adapter contamination, and other key
metrics. Each module produces a pass/warn/fail flag, giving a rapid overview
of potential problems before downstream processing.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda fastqc

Basic Usage
-----------

Run FastQC on paired-end FASTQ files, using two threads and writing output to
a dedicated results directory.

.. code-block:: bash

   fastqc -t 2 -o results/fastqc/ sample_R1.fastq.gz sample_R2.fastq.gz

The command accepts both compressed (``.gz``) and uncompressed FASTQ files.
Create the output directory beforehand if it does not exist:

.. code-block:: bash

   mkdir -p results/fastqc/
   fastqc -t 2 -o results/fastqc/ sample_R1.fastq.gz sample_R2.fastq.gz

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-o``
     - Directory where output reports will be written.
   * - ``-t``
     - Number of files to process simultaneously (one thread per file).
   * - ``--noextract``
     - Do not uncompress the output ZIP file after creating it.
   * - ``--contaminants``
     - Path to a custom contaminant list to screen against.
   * - ``--adapters``
     - Path to a custom adapter list to screen for adapter content.
   * - ``--limits``
     - Path to a custom limits file for overriding pass/warn/fail thresholds.
   * - ``-f``
     - Force a specific input format (``fastq``, ``bam``, or ``sam``).

Expected Output
---------------

FastQC produces two files per input file:

* ``sample_R1_fastqc.html`` -- a self-contained HTML report viewable in any
  web browser.
* ``sample_R1_fastqc.zip`` -- a ZIP archive containing the HTML report,
  summary text, and individual module data files.

The HTML report contains sections for per-base sequence quality, per-sequence
quality scores, per-base sequence content, GC content distribution, sequence
length distribution, duplicate sequences, overrepresented sequences, and
adapter content.

See Also
--------

* :doc:`fastp` -- all-in-one preprocessing tool that combines QC reporting
  with adapter trimming and quality filtering
* :doc:`multiqc` -- aggregate FastQC reports (and other tool outputs) into a
  single summary report
* :doc:`/data-formats/fastq` -- reference for the FASTQ file format
