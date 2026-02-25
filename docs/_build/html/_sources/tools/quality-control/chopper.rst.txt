Chopper
=======

Overview
--------

Chopper is a fast, Rust-based filtering and trimming tool for long-read
sequencing data. It reads from standard input and writes to standard output,
making it easy to integrate into Unix pipelines. Chopper filters reads by
minimum quality score and minimum/maximum length, and can optionally trim a
fixed number of bases from read heads or tails. It is commonly used after
basecalling to remove low-quality or very short nanopore reads before
alignment.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda chopper

Basic Usage
-----------

Filter nanopore reads from a BAM file, keeping only reads with a minimum
average quality of 10 and a minimum length of 1000 bp.

.. code-block:: bash

   # Quality and length filtering for nanopore reads
   samtools fastq reads.bam | \
     chopper --quality 10 --minlength 1000 | \
     gzip > filtered_reads.fastq.gz

   # Check before/after
   echo "Before: $(samtools view -c reads.bam) reads"
   echo "After: $(zcat filtered_reads.fastq.gz | awk 'NR%4==1' | wc -l) reads"

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``--quality`` / ``-q``
     - Minimum average Phred quality score for a read to pass (default 0).
   * - ``--minlength``
     - Discard reads shorter than this value (default 1).
   * - ``--maxlength``
     - Discard reads longer than this value (default unlimited).
   * - ``--headcrop``
     - Trim this many bases from the start of each read.
   * - ``--tailcrop``
     - Trim this many bases from the end of each read.
   * - ``--threads``
     - Number of threads for compression/decompression.
   * - ``--contam``
     - Path to a FASTA file of contaminant sequences to filter against.

Expected Output
---------------

Chopper writes filtered FASTQ records to standard output. In the example
above, the output is piped through ``gzip`` to produce a compressed FASTQ
file (``filtered_reads.fastq.gz``).

There is no separate report file. Use the before/after read-count check
shown above or run :doc:`nanoplot` on the filtered reads to visualise the
effect of filtering.

See Also
--------

* :doc:`nanoplot` -- visualise read length and quality distributions before
  and after filtering
* :doc:`pycoqc` -- run-level quality control for Oxford Nanopore data
* :doc:`fastp` -- equivalent quality filtering and trimming for short-read
  data
* :doc:`/data-formats/fastq` -- reference for the FASTQ file format
