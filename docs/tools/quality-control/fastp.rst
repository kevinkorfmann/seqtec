fastp
=====

Overview
--------

fastp is a fast, all-in-one FASTQ preprocessor that performs quality control,
adapter trimming, quality filtering, per-read cutting, and polyG/polyX tail
trimming in a single pass. It automatically detects adapters for both
single-end and paired-end data and produces detailed HTML and JSON reports,
making it a convenient replacement for running separate QC and trimming steps.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda fastp

Basic Usage
-----------

Trim and filter paired-end reads with quality and length thresholds, automatic
adapter detection, and four processing threads.

.. code-block:: bash

   fastp -i sample_R1.fastq.gz -I sample_R2.fastq.gz \
     -o trimmed_R1.fastq.gz -O trimmed_R2.fastq.gz \
     -h report.html -j report.json \
     --qualified_quality_phred 20 \
     --length_required 50 \
     --detect_adapter_for_pe \
     --thread 4

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``-i`` / ``-I``
     - Input FASTQ files for read 1 and read 2 respectively.
   * - ``-o`` / ``-O``
     - Output FASTQ files for read 1 and read 2 after filtering.
   * - ``-h``
     - Path for the HTML QC report.
   * - ``-j``
     - Path for the JSON QC report (machine-readable).
   * - ``--qualified_quality_phred``
     - Minimum Phred quality score to consider a base qualified (default 15).
   * - ``--length_required``
     - Discard reads shorter than this value after trimming (default 15).
   * - ``--detect_adapter_for_pe``
     - Enable automatic adapter detection for paired-end data by overlap
       analysis.
   * - ``--thread``
     - Number of worker threads (default 2, maximum 16).
   * - ``--cut_front`` / ``--cut_tail``
     - Sliding-window quality trimming from the 5' or 3' end.
   * - ``--trim_poly_g``
     - Remove polyG tails common in NovaSeq/NextSeq two-colour chemistry.

Expected Output
---------------

fastp writes the filtered reads to the output FASTQ files specified with
``-o`` / ``-O`` and generates two report files:

* ``report.html`` -- an interactive HTML report with before/after quality
  plots, filtering statistics, adapter content, and insert-size distribution.
* ``report.json`` -- a JSON report containing the same metrics in a
  machine-readable format, suitable for downstream aggregation with
  :doc:`multiqc`.

The report includes read counts before and after filtering, quality score
distributions, base content curves, and a summary of adapter sequences found.

See Also
--------

* :doc:`fastqc` -- standalone quality assessment without trimming
* :doc:`multiqc` -- aggregate fastp JSON reports across samples into a single
  summary
* :doc:`/data-formats/fastq` -- reference for the FASTQ file format
