HTSeq
=====

Overview
--------

HTSeq is a Python framework for working with high-throughput sequencing data
that includes htseq-count, a widely used tool for counting reads mapped to
genomic features. Given a sorted BAM file and a GTF annotation, htseq-count
assigns each read (or read pair) to a gene based on its overlap with annotated
exons. It provides multiple overlap resolution modes to handle reads that span
feature boundaries or overlap multiple genes. HTSeq produces a simple
gene-by-count table that serves as direct input for differential expression
tools such as DESeq2 and edgeR.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda htseq

Basic Usage
-----------

Count reads per gene from a coordinate-sorted BAM file.

.. code-block:: bash

   htseq-count -f bam -r pos -s reverse \
     -t exon -i gene_id \
     sample.sorted.bam genes.gtf > counts.txt

For multiple samples, run htseq-count separately on each BAM file and merge
the results into a count matrix.

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-f``
     - Input format: ``bam`` or ``sam``.
   * - ``-r``
     - Sort order of the input file: ``pos`` for coordinate-sorted or
       ``name`` for name-sorted.
   * - ``-s``
     - Strand-specificity: ``yes`` for forward stranded, ``reverse`` for
       reverse stranded, or ``no`` for unstranded.
   * - ``-t``
     - Feature type to use from the GTF (default ``exon``).
   * - ``-i``
     - GTF attribute to use as the feature ID (default ``gene_id``).
   * - ``-m`` / ``--mode``
     - Overlap resolution mode: ``union`` (default), ``intersection-strict``,
       or ``intersection-nonempty``.
   * - ``--nonunique``
     - How to handle reads mapping to multiple features: ``none`` (discard)
       or ``all`` (count for each feature).
   * - ``-a``
     - Minimum alignment quality threshold (default 10).
   * - ``--additional-attr``
     - Include additional GTF attributes in the output (e.g. gene_name).

Expected Output
---------------

* Standard output (redirected to ``counts.txt``) -- a two-column tab-delimited
  file with the gene identifier in the first column and the raw read count in
  the second column. The last five lines contain special counters:

  - ``__no_feature`` -- reads not overlapping any feature.
  - ``__ambiguous`` -- reads overlapping multiple features.
  - ``__too_low_aQual`` -- reads below the alignment quality threshold.
  - ``__not_aligned`` -- unmapped reads.
  - ``__alignment_not_unique`` -- reads with multiple alignments.

See Also
--------

* :doc:`featurecounts` -- faster multi-threaded alternative for read counting
  with built-in multi-BAM support
* :doc:`salmon` -- alignment-free transcript-level quantification
* :doc:`kallisto` -- pseudoalignment-based transcript quantification
* :doc:`/tools/differential-expression/deseq2` -- differential expression
  analysis using htseq-count output
* :doc:`/tools/differential-expression/edger` -- alternative differential
  expression framework
