BEDTools
========

Overview
--------

BEDTools is the standard toolkit for genomic interval arithmetic. It provides
fast, set-theoretic operations -- intersection, union, complement, merging, and
more -- on BED, BAM, VCF, and GFF/GTF files. BEDTools is essential for tasks
such as identifying overlapping genomic features, filtering regions against
blacklists, computing genome-wide coverage, and measuring similarity between
interval sets with the Jaccard statistic.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda bedtools

Basic Usage
-----------

**Intersect peaks with gene promoters**

.. code-block:: bash

   bedtools intersect -a peaks.bed -b promoters.bed -wa -wb > overlap.bed

**Find peaks that do NOT overlap with blacklist regions**

.. code-block:: bash

   bedtools intersect -a peaks.bed -b blacklist.bed -v > clean_peaks.bed

**Merge overlapping intervals**

.. code-block:: bash

   bedtools merge -i sorted_peaks.bed -d 100 > merged.bed

**Find the closest gene to each peak**

.. code-block:: bash

   bedtools closest -a peaks.bed -b genes.bed -d > closest.bed

**Compute genome-wide coverage from a BAM file**

.. code-block:: bash

   bedtools genomecov -ibam sample.bam -bg > coverage.bedgraph

**Generate windows across the genome**

.. code-block:: bash

   bedtools makewindows -g genome.sizes -w 10000 > windows.bed

**Compute Jaccard similarity between two sets of intervals**

.. code-block:: bash

   bedtools jaccard -a set1.bed -b set2.bed

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-a``
     - The "query" file (BED/BAM/VCF/GFF).
   * - ``-b``
     - The "subject" file(s) to compare against.
   * - ``-wa``
     - Write the original entry from ``-a`` for each overlap.
   * - ``-wb``
     - Write the original entry from ``-b`` for each overlap.
   * - ``-v``
     - Report entries in ``-a`` that have *no* overlap with ``-b``.
   * - ``-d INT``
     - Maximum distance between features to merge (used with ``merge``);
       features within this distance are combined into a single interval.
   * - ``-f FLOAT``
     - Minimum overlap required as a fraction of ``-a`` (e.g., ``0.50`` for
       50 %).
   * - ``-r``
     - Require the overlap fraction to be reciprocal for both ``-a`` and
       ``-b``.
   * - ``-s``
     - Require that features are on the same strand.
   * - ``-bg``
     - Report depth in bedGraph format (used with ``genomecov``).
   * - ``-g``
     - Genome file providing chromosome sizes (required by ``makewindows``,
       ``complement``, etc.).
   * - ``-w INT``
     - Window size in bp (used with ``makewindows``).

Expected Output
---------------

* ``intersect`` -- a BED file listing features (or feature pairs with ``-wa
  -wb``) that overlap between the two inputs. With ``-v``, only non-overlapping
  entries from ``-a`` are reported.
* ``merge`` -- a BED file of merged intervals where overlapping or nearby
  features have been collapsed.
* ``closest`` -- a BED file pairing each ``-a`` feature with the nearest ``-b``
  feature; the ``-d`` flag appends the distance as an extra column.
* ``genomecov`` -- a bedGraph file of per-base or per-bin coverage across the
  genome.
* ``makewindows`` -- a BED file of fixed-size, non-overlapping (or sliding)
  windows tiling the genome.
* ``jaccard`` -- a single-line summary with the intersection size, union size,
  and Jaccard index.

See Also
--------

* :doc:`/tools/sam-bam-processing/samtools` -- prepare sorted and indexed BAM
  files used as input by several BEDTools sub-commands
* :doc:`/tools/sam-bam-processing/deeptools` -- compute normalised coverage
  tracks and heatmaps from BAM/bigWig files
* :doc:`/data-formats/bed` -- reference for the BED interval format
* :doc:`/data-formats/sam-bam-cram` -- reference for the SAM/BAM/CRAM file
  formats
* :doc:`/data-formats/bigwig-bedgraph` -- reference for the bigWig and
  bedGraph coverage formats
* :doc:`/data-formats/vcf-bcf` -- reference for the VCF/BCF variant format
