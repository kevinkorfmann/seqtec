Picard
======

Overview
--------

Picard is a set of Java command-line tools maintained by the Broad Institute for
manipulating high-throughput sequencing data. It is best known for marking PCR
duplicates and collecting a wide range of alignment quality metrics. Picard
integrates tightly with GATK-based variant-calling pipelines and produces
detailed metrics files that can be visualised with tools such as MultiQC.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda picard

Basic Usage
-----------

**Mark PCR duplicates**

.. code-block:: bash

   java -jar picard.jar MarkDuplicates \
     I=sample.sorted.bam \
     O=sample.dedup.bam \
     M=sample.dup_metrics.txt \
     REMOVE_DUPLICATES=false

**Collect alignment summary metrics**

.. code-block:: bash

   java -jar picard.jar CollectAlignmentSummaryMetrics \
     R=reference.fa I=sample.dedup.bam O=alignment_metrics.txt

**Collect insert size distribution**

.. code-block:: bash

   java -jar picard.jar CollectInsertSizeMetrics \
     I=sample.dedup.bam O=insert_metrics.txt H=insert_hist.pdf

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``I``
     - Input BAM or SAM file.
   * - ``O``
     - Output BAM or metrics file.
   * - ``M``
     - Duplication metrics output file (used with ``MarkDuplicates``).
   * - ``R``
     - Reference FASTA file (required by several collectors).
   * - ``REMOVE_DUPLICATES``
     - If ``true``, discard duplicate reads from the output BAM instead of only
       flagging them (default: ``false``).
   * - ``H``
     - Histogram PDF output file (used with ``CollectInsertSizeMetrics``).
   * - ``VALIDATION_STRINGENCY``
     - How strictly to validate the input (``STRICT``, ``LENIENT``, or
       ``SILENT``). Set to ``LENIENT`` or ``SILENT`` to skip non-critical
       format warnings.
   * - ``CREATE_INDEX``
     - If ``true``, create a BAM index file alongside the output BAM (default:
       ``false``).

Expected Output
---------------

* ``MarkDuplicates`` -- a BAM file with duplicate FLAG bits set (or removed)
  and a tab-delimited metrics file reporting the number and fraction of
  duplicates per library.
* ``CollectAlignmentSummaryMetrics`` -- a text file with statistics for each
  read category (paired, unpaired, first-of-pair, second-of-pair) including
  total reads, aligned reads, mismatch rate, and more.
* ``CollectInsertSizeMetrics`` -- a text metrics file and an accompanying PDF
  histogram showing the distribution of insert sizes for paired-end libraries.

See Also
--------

* :doc:`samtools` -- lightweight alternative for basic BAM operations such as
  sorting, indexing, and simple filtering
* :doc:`sambamba` -- faster multi-threaded duplicate marking
* :doc:`deeptools` -- generate coverage tracks and quality heatmaps from
  processed BAM files
* :doc:`/data-formats/sam-bam-cram` -- reference for the SAM/BAM/CRAM file
  formats
