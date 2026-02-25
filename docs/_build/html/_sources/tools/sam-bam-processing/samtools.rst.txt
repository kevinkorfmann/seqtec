SAMtools
========

Overview
--------

SAMtools is the foundational toolkit for reading, writing, editing, indexing,
and viewing alignments stored in the SAM, BAM, and CRAM formats. It provides
sub-commands for sorting, filtering, merging, and computing statistics on
alignment files and is a dependency of virtually every NGS pipeline. SAMtools
also includes utilities for per-base depth calculation, random sub-sampling, and
fast region-based queries via BAM indices.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda samtools

Basic Usage
-----------

**View the BAM header**

.. code-block:: bash

   samtools view -H sample.bam

**Convert SAM to sorted BAM**

.. code-block:: bash

   samtools sort -@ 8 -o sample.sorted.bam sample.sam

**Index a sorted BAM file**

.. code-block:: bash

   samtools index sample.sorted.bam

**View alignments in a genomic region**

.. code-block:: bash

   samtools view sample.sorted.bam chr1:1000000-2000000

**Filter: keep only properly paired, uniquely mapped reads (MAPQ >= 30)**

.. code-block:: bash

   samtools view -b -f 2 -q 30 sample.sorted.bam > filtered.bam

**Generate alignment statistics**

.. code-block:: bash

   samtools flagstat sample.sorted.bam
   samtools idxstats sample.sorted.bam
   samtools stats sample.sorted.bam > sample.stats.txt

**Calculate per-base depth**

.. code-block:: bash

   samtools depth -a sample.sorted.bam > depth.txt

**Merge multiple BAM files**

.. code-block:: bash

   samtools merge merged.bam sample1.bam sample2.bam sample3.bam

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-@ THREADS``
     - Number of additional threads to use for compression and decompression.
   * - ``-o FILE``
     - Write output to *FILE* instead of standard output.
   * - ``-b``
     - Output in BAM format (used with ``view``).
   * - ``-h``
     - Include the header in SAM output (used with ``view``).
   * - ``-H``
     - Print only the header (used with ``view``).
   * - ``-f FLAG``
     - Keep reads with *all* of the specified FLAG bits set.
   * - ``-F FLAG``
     - Exclude reads with *any* of the specified FLAG bits set.
   * - ``-q INT``
     - Minimum mapping quality (MAPQ) threshold.
   * - ``-a``
     - Output all positions including zero-depth sites (used with ``depth``).
   * - ``-d INT``
     - Maximum per-file depth for ``depth``; 0 means unlimited.

Expected Output
---------------

* ``samtools sort`` -- a coordinate-sorted BAM file.
* ``samtools index`` -- a ``.bai`` (or ``.csi``) index file alongside the BAM.
* ``samtools flagstat`` -- a concise summary of read counts by FLAG category
  printed to standard output.
* ``samtools idxstats`` -- a tab-delimited table of per-reference mapped and
  unmapped read counts.
* ``samtools stats`` -- a comprehensive text report with summary numbers,
  insert-size histograms, base-quality distributions, and more.
* ``samtools depth`` -- a tab-delimited file with columns for chromosome,
  position, and depth.
* ``samtools merge`` -- a single BAM file combining reads from all inputs.

See Also
--------

* :doc:`sambamba` -- a faster alternative for sorting, indexing, and duplicate
  marking using multi-threading
* :doc:`picard` -- Java-based toolkit for duplicate marking and alignment QC
  metrics
* :doc:`deeptools` -- generate normalised coverage tracks and signal heatmaps
  from BAM files
* :doc:`/data-formats/sam-bam-cram` -- reference for the SAM/BAM/CRAM file
  formats
