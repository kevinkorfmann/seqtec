kallisto
========

Overview
--------

kallisto is an ultrafast RNA-seq quantification tool that uses pseudoalignment
to estimate transcript-level abundances without performing traditional read
alignment. Instead of mapping reads to a reference genome, kallisto determines
which transcripts each read is compatible with using a transcriptome de Bruijn
graph index. This approach achieves quantification speeds orders of magnitude
faster than alignment-based methods while maintaining comparable accuracy.
kallisto also supports bootstrap resampling to estimate technical variance in
abundance estimates, which can be leveraged by downstream tools such as sleuth
for differential expression analysis.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda kallisto

Basic Usage
-----------

**Build an index from a transcriptome FASTA**

.. code-block:: bash

   kallisto index -i transcripts.idx transcriptome.fa

**Quantify paired-end reads with bootstraps**

.. code-block:: bash

   kallisto quant -i transcripts.idx -o output/ \
     -b 100 -t 8 \
     sample_R1.fastq.gz sample_R2.fastq.gz

For single-end reads, provide the estimated fragment length and standard
deviation:

.. code-block:: bash

   kallisto quant -i transcripts.idx -o output/ \
     --single -l 200 -s 30 -t 8 \
     sample.fastq.gz

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``index -i``
     - Output path for the kallisto index file.
   * - ``quant -i``
     - Path to the pre-built kallisto index.
   * - ``-o``
     - Output directory for quantification results.
   * - ``-b``
     - Number of bootstrap samples for estimating technical variance.
   * - ``-t``
     - Number of threads to use.
   * - ``--single``
     - Enable single-end read mode (requires ``-l`` and ``-s``).
   * - ``-l``
     - Estimated average fragment length (for single-end reads).
   * - ``-s``
     - Estimated standard deviation of fragment length (for single-end reads).
   * - ``--rf-stranded``
     - Reads are from a reverse-stranded library (e.g. dUTP method).
   * - ``--fr-stranded``
     - Reads are from a forward-stranded library.
   * - ``--plaintext``
     - Write output in plain text instead of HDF5 format.

Expected Output
---------------

kallisto writes the following files to the output directory:

* ``abundance.tsv`` -- a tab-delimited file with columns for target ID,
  transcript length, effective length, estimated counts (est_counts), and
  transcripts per million (TPM).
* ``abundance.h5`` -- an HDF5 file containing the abundance estimates and
  bootstrap replicates (when ``-b`` is used), readable by sleuth and other
  downstream tools.
* ``run_info.json`` -- a JSON file recording the kallisto version, index used,
  number of processed reads, percentage of pseudoaligned reads, and run
  parameters.

See Also
--------

* :doc:`salmon` -- quasi-mapping-based quantification tool with built-in GC
  and sequence bias correction
* :doc:`featurecounts` -- alignment-based gene-level counting from BAM files
* :doc:`/tools/differential-expression/deseq2` -- differential expression
  analysis using count data from kallisto (via tximport)
