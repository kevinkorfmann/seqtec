BED
===

Overview
--------

BED (Browser Extensible Data) is a tab-delimited format for describing
genomic intervals. It is used throughout bioinformatics to represent
regions of interest such as:

* Genes, exons, and promoter regions
* ChIP-seq peaks and regulatory elements
* Target capture regions for exome sequencing
* Blacklisted or masked regions
* Structural variant breakpoints

BED files are compact, human-readable, and supported by nearly every genomic
tool. They are the primary input for ``bedtools`` and are accepted by IGV,
UCSC Genome Browser, samtools, GATK, and many other programs.

.. important::

   BED uses **0-based, half-open** coordinates. The start position is
   zero-based (the first base of a chromosome is 0) and the end position is
   exclusive. An interval covering the first 1 000 bases of chr1 is written
   as ``chr1  0  1000``. This differs from GFF/GTF and VCF, which use
   1-based, fully-closed coordinates.

Structure
---------

BED files come in several levels of detail. The first three columns are
mandatory; additional columns add information.

BED3 -- minimal interval
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   # BED3: chromosome, start, end
   chr1  1000  2000
   chr1  3000  4500

Three columns: **chrom**, **chromStart** (0-based, inclusive), and
**chromEnd** (exclusive). The interval ``chr1  1000  2000`` covers bases
1000 through 1999 (1 000 bases total).

BED6 -- adding name, score, and strand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   # BED6: adds name, score, strand
   chr1  1000  2000  peak1  500  +
   chr1  3000  4500  peak2  300  -

.. list-table::
   :header-rows: 1
   :widths: 10 20 70

   * - Col
     - Field
     - Description
   * - 4
     - name
     - Feature name or identifier.
   * - 5
     - score
     - Integer 0--1000 (e.g. peak enrichment score).
   * - 6
     - strand
     - ``+`` (forward), ``-`` (reverse), or ``.`` (unstranded).

BED12 -- transcript models
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   # BED12: adds thickStart, thickEnd, itemRgb, blockCount,
   #         blockSizes, blockStarts (used for transcript models)
   chr1  11873  14409  NR_046018  0  +  11873  11873  0  3  354,109,1189,  0,739,1347,

.. list-table::
   :header-rows: 1
   :widths: 10 20 70

   * - Col
     - Field
     - Description
   * - 7
     - thickStart
     - Start of the thick drawing region (e.g. CDS start).
   * - 8
     - thickEnd
     - End of the thick drawing region (e.g. CDS end).
   * - 9
     - itemRgb
     - RGB colour value for display (``0`` = black).
   * - 10
     - blockCount
     - Number of blocks (exons).
   * - 11
     - blockSizes
     - Comma-separated list of block sizes.
   * - 12
     - blockStarts
     - Comma-separated list of block start positions relative to
       chromStart.

In the example above the transcript ``NR_046018`` has **3 exons** of sizes
354, 109, and 1189 bp. The exon start positions relative to the transcript
start (11873) are 0, 739, and 1347.

Coordinate system comparison
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 25 25 30

   * - Format
     - System
     - First base
     - Interval [1, 100]
   * - **BED**
     - 0-based, half-open
     - 0
     - ``chr1  0  100``
   * - **GFF / GTF**
     - 1-based, closed
     - 1
     - ``chr1  1  100``
   * - **VCF**
     - 1-based
     - 1
     - ``POS = 1``
   * - **SAM**
     - 1-based
     - 1
     - ``POS = 1``

Working With
------------

Basic bedtools operations
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Find overlapping intervals between two BED files
   bedtools intersect -a peaks.bed -b promoters.bed > overlap.bed

   # Subtract one set of intervals from another
   bedtools subtract -a regions.bed -b blacklist.bed > clean.bed

   # Merge overlapping intervals
   sort -k1,1 -k2,2n regions.bed | bedtools merge > merged.bed

   # Compute the complement (gaps) relative to a genome
   bedtools complement -i regions.bed -g chrom.sizes > gaps.bed

Extracting sequences
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Get FASTA sequences for BED intervals
   bedtools getfasta -fi reference.fa -bed regions.bed -fo regions.fa

Coverage and depth
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Count reads overlapping each interval
   bedtools coverage -a targets.bed -b aligned.sorted.bam > coverage.bed

   # Compute genome-wide coverage histogram
   bedtools genomecov -ibam aligned.sorted.bam -bg > coverage.bedgraph

Sorting BED files
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Sort by chromosome and start position
   sort -k1,1 -k2,2n unsorted.bed > sorted.bed

Slop (extend) intervals
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Extend each interval by 500 bp on both sides
   bedtools slop -i peaks.bed -g chrom.sizes -b 500 > extended.bed

   # Extend 2 kb upstream only (strand-aware)
   bedtools slop -i genes.bed -g chrom.sizes -l 2000 -r 0 -s > promoters.bed

Filtering BAM by BED regions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Keep only reads overlapping target regions
   samtools view -b -L targets.bed aligned.sorted.bam > on_target.bam

See Also
--------

* :doc:`/tools/interval-operations/bedtools` -- the comprehensive BED
  manipulation toolkit
* :doc:`gff-gtf` -- 1-based annotation format (related but different
  coordinate system)
* :doc:`bigwig-bedgraph` -- continuous signal format derived from BED-like
  intervals
* :doc:`vcf-bcf` -- variant format that can be filtered using BED regions
* :doc:`/tools/sam-bam-processing/samtools` -- ``samtools view -L`` for
  region-based BAM filtering
