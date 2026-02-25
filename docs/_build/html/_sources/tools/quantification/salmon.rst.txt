Salmon
======

Overview
--------

Salmon is a fast and bias-aware RNA-seq quantification tool that estimates
transcript-level abundances using selective alignment (mapping-based mode) or
quasi-mapping. It accounts for common biases in RNA-seq data including fragment
GC content bias, positional bias, and sequence-specific bias through its
built-in correction models. Salmon can also operate in alignment-based mode,
taking a pre-aligned BAM file as input. Its speed and accuracy make it a
standard choice in RNA-seq pipelines, and its output integrates directly with
tximport for gene-level summarisation and downstream differential expression
analysis with DESeq2 or edgeR.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda salmon

Basic Usage
-----------

**Build a transcriptome index**

.. code-block:: bash

   salmon index -t transcriptome.fa -i salmon_index -p 8

**Quantify paired-end reads with selective alignment**

.. code-block:: bash

   salmon quant -i salmon_index -l A \
     -1 sample_R1.fastq.gz -2 sample_R2.fastq.gz \
     -p 8 --validateMappings \
     -o salmon_output/

The ``-l A`` flag enables automatic library type detection.

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``index -t``
     - Path to the transcriptome FASTA for building the index.
   * - ``index -i``
     - Output path for the Salmon index directory.
   * - ``quant -i``
     - Path to the pre-built Salmon index.
   * - ``-l``
     - Library type (``A`` for automatic detection, or explicit types such as
       ``ISR``, ``ISF``, ``IU``).
   * - ``-1`` / ``-2``
     - Paired-end read files (forward and reverse).
   * - ``-r``
     - Single-end read file.
   * - ``-p``
     - Number of threads to use.
   * - ``--validateMappings``
     - Enable selective alignment for improved mapping accuracy.
   * - ``-o``
     - Output directory for quantification results.
   * - ``--gcBias``
     - Enable GC bias correction (recommended for most datasets).
   * - ``--seqBias``
     - Enable sequence-specific bias correction.
   * - ``--numBootstraps``
     - Number of bootstrap samples for variance estimation.

Expected Output
---------------

Salmon writes the following files to the output directory:

* ``quant.sf`` -- the primary output file: a tab-delimited table with columns
  for transcript name, length, effective length, TPM (transcripts per million),
  and estimated read counts (NumReads).
* ``quant.genes.sf`` -- gene-level quantification (when a gene map is
  provided).
* ``aux_info/`` -- directory containing auxiliary information including the
  observed library type, fragment length distribution, bias correction
  parameters, and the equivalence class file.
* ``cmd_info.json`` -- a JSON file recording the exact command and parameters
  used for the run.
* ``logs/`` -- directory containing log files with mapping rate and run
  statistics.

See Also
--------

* :doc:`kallisto` -- pseudoalignment-based quantification tool with bootstrap
  support
* :doc:`featurecounts` -- alignment-based gene-level counting from BAM files
* :doc:`/tools/differential-expression/deseq2` -- differential expression
  analysis using Salmon counts (via tximport)
* :doc:`/tools/differential-expression/edger` -- alternative differential
  expression framework compatible with Salmon output
