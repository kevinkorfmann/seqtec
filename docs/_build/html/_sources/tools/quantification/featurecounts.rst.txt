featureCounts
=============

Overview
--------

featureCounts is a fast and efficient read counting program from the Subread
package that assigns aligned reads (or read pairs) to genomic features such as
genes, exons, or promoters using a gene annotation file in GTF or SAF format.
It supports multi-threaded execution and can process multiple BAM files in a
single run, producing a unified count matrix suitable for downstream
differential expression analysis. featureCounts handles both single-end and
paired-end data, supports strand-specific counting, and provides summary
statistics on assignment success rates.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda subread

Basic Usage
-----------

Count read pairs for each gene across multiple BAM files.

.. code-block:: bash

   featureCounts -T 8 -p --countReadPairs \
     -a genes.gtf \
     -o counts.txt \
     sample1.bam sample2.bam sample3.bam

For single-end data, omit the ``-p`` and ``--countReadPairs`` flags:

.. code-block:: bash

   featureCounts -T 8 \
     -a genes.gtf \
     -o counts.txt \
     sample1.bam sample2.bam

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-a``
     - Path to the gene annotation file in GTF or SAF format.
   * - ``-o``
     - Output file path for the count matrix.
   * - ``-T``
     - Number of threads to use.
   * - ``-p``
     - Indicate that input data is paired-end.
   * - ``--countReadPairs``
     - Count fragments (read pairs) rather than individual reads.
   * - ``-s``
     - Strand-specificity: ``0`` for unstranded, ``1`` for forward stranded,
       ``2`` for reverse stranded.
   * - ``-t``
     - Feature type to count (default ``exon``); must match the third column
       of the GTF.
   * - ``-g``
     - Attribute used for grouping features into meta-features (default
       ``gene_id``).
   * - ``-Q``
     - Minimum mapping quality threshold for counting a read.
   * - ``--primary``
     - Count only primary alignments (ignore secondary and supplementary).
   * - ``-B``
     - Require both ends of a read pair to be aligned for counting.

Expected Output
---------------

* ``counts.txt`` -- a tab-delimited count matrix with gene metadata columns
  (Geneid, Chr, Start, End, Strand, Length) followed by one count column per
  input BAM file. Each row represents a gene (or meta-feature) and each count
  value is the number of reads or fragments assigned to that gene.
* ``counts.txt.summary`` -- a summary table showing the number of reads
  assigned, unassigned (ambiguous, multi-mapping, no features, unmapped), and
  other categories for each input file.

See Also
--------

* :doc:`htseq` -- alternative read counting tool with per-read overlap
  resolution modes
* :doc:`salmon` -- alignment-free quantification at the transcript level
* :doc:`kallisto` -- pseudoalignment-based transcript quantification
* :doc:`/tools/differential-expression/deseq2` -- differential expression
  analysis using featureCounts output
