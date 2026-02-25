Bismark
=======

Overview
--------

Bismark is a dedicated aligner and methylation caller for bisulfite-treated
sequencing (BS-seq) data. Bisulfite treatment converts unmethylated cytosines
to uracils (read as thymines after PCR), while methylated cytosines remain
unchanged. Bismark handles the resulting sequence complexity by aligning reads
against an in-silico bisulfite-converted reference genome using either Bowtie2
or HISAT2 as the underlying aligner. After alignment, the methylation
extractor determines the methylation state of every cytosine in CpG, CHG, and
CHH contexts, producing per-base methylation calls for downstream analysis.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda bismark

Bismark requires Bowtie2 (installed as a dependency) and Samtools.

Basic Usage
-----------

**Step 1 -- Prepare the genome**

Build the bisulfite-converted genome index (one-time step per reference).

.. code-block:: bash

   bismark_genome_preparation /ref/

**Step 2 -- Align bisulfite-treated reads**

.. code-block:: bash

   bismark --genome /ref/ \
     -1 trimmed_R1.fastq.gz -2 trimmed_R2.fastq.gz \
     --parallel 4 -o bismark_output/

**Step 3 -- Remove duplicates**

.. code-block:: bash

   deduplicate_bismark --bam bismark_output/sample.bam

**Step 4 -- Extract methylation calls**

.. code-block:: bash

   bismark_methylation_extractor --paired-end --comprehensive \
     --CX --cytosine_report --genome_folder /ref/ \
     -o methylation/ bismark_output/sample.deduplicated.bam

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``--genome``
     - Path to the directory containing the Bismark-prepared reference genome.
   * - ``-1`` / ``-2``
     - Paired-end input FASTQ files (Read 1 and Read 2).
   * - ``--parallel``
     - Number of parallel Bismark instances to run (each uses multiple Bowtie2
       threads).
   * - ``-o``
     - Output directory for alignment or extraction results.
   * - ``--non_directional``
     - Align to all four possible bisulfite-converted strands (required for
       some library protocols such as PBAT).
   * - ``--paired-end``
     - Input data is paired-end (used in the methylation extractor).
   * - ``--comprehensive``
     - Merge context-specific methylation output into a single comprehensive
       file.
   * - ``--CX``
     - Report methylation for all cytosine contexts (CpG, CHG, CHH), not just
       CpG.
   * - ``--cytosine_report``
     - Generate a genome-wide cytosine methylation report with coverage
       information for every cytosine position.
   * - ``--genome_folder``
     - Path to the reference genome folder (used by the methylation extractor
       for generating the cytosine report).

Expected Output
---------------

**Alignment step:**

* ``sample_bismark_bt2_pe.bam`` -- BAM file with aligned reads and
  methylation call tags (XM tag).
* ``sample_bismark_bt2_PE_report.txt`` -- alignment summary with mapping
  efficiency and cytosine methylation percentages.

**Deduplication step:**

* ``sample.deduplicated.bam`` -- BAM file with PCR duplicates removed.
* Deduplication report with the number and percentage of duplicates removed.

**Methylation extraction step:**

* ``CpG_context_sample.deduplicated.txt`` -- per-read methylation calls for
  CpG sites.
* ``sample.deduplicated.CX_report.txt`` -- genome-wide cytosine report with
  columns for chromosome, position, strand, methylated count, unmethylated
  count, context, and trinucleotide context.
* ``sample.deduplicated.bedGraph.gz`` -- bedGraph file of CpG methylation
  percentages.
* ``sample.deduplicated.bismark.cov.gz`` -- coverage file with methylation
  percentage and read counts per CpG.

See Also
--------

* :doc:`macs2` -- peak calling for ChIP-seq and ATAC-seq epigenomic assays
* :doc:`/tools/quality-control/fastp` -- adapter trimming and quality filtering
  of bisulfite-seq reads before alignment
* :doc:`/tools/sam-bam-processing/picard` -- additional duplicate marking and
  BAM processing utilities
