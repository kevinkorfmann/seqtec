Guppy
=====

Overview
--------

Guppy was Oxford Nanopore Technologies' (ONT) production basecaller for
converting raw nanopore signal data into nucleotide sequences. It supported
multiple basecalling models (fast, high-accuracy, super-accuracy) and could
perform barcoding, adapter trimming, and alignment as part of the basecalling
pipeline. Guppy has been superseded by Dorado, which offers improved accuracy
and performance. Guppy remains relevant for reprocessing older datasets and
for environments where Dorado has not yet been adopted.

.. note::

   Guppy is deprecated and is being replaced by Dorado. New projects should
   use Dorado for basecalling. See :doc:`dorado` for the recommended workflow.

Installation
------------

Guppy is distributed through the ONT Community portal and is not available via
Bioconda. Download the appropriate package from the
`ONT Community site <https://community.nanoporetech.com/>`_ (requires a login).

After downloading, extract and add to your ``PATH``:

.. code-block:: bash

   tar -xzf ont-guppy_<version>_linux64.tar.gz
   export PATH=$PWD/ont-guppy/bin:$PATH

GPU-accelerated basecalling requires a CUDA-capable GPU and the corresponding
CUDA toolkit.

Basic Usage
-----------

Basecall a directory of POD5 or FAST5 files using a super-accuracy model on
GPU.

.. code-block:: bash

   guppy_basecaller -i pod5_dir/ -s output/ \
     --config dna_r10.4.1_e8.2_400bps_sup.cfg \
     --device cuda:0 \
     --recursive

The output directory will contain FASTQ files (one per batch) and a
sequencing summary file.

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-i``
     - Input directory containing raw signal files (POD5 or FAST5).
   * - ``-s``
     - Output directory for basecalled FASTQ files and summary.
   * - ``--config``
     - Basecalling configuration file (e.g.,
       ``dna_r10.4.1_e8.2_400bps_sup.cfg``). Must match the flow cell and kit
       chemistry.
   * - ``--device``
     - GPU device to use (``cuda:0``, ``cuda:0,1`` for multiple GPUs, or
       ``auto``).
   * - ``--recursive``
     - Recursively search the input directory for signal files.
   * - ``--num_callers``
     - Number of parallel basecalling processes (CPU mode).
   * - ``--gpu_runners_per_device``
     - Number of neural network runners per GPU (tuning parameter for
       throughput).
   * - ``--chunks_per_runner``
     - Number of signal chunks per runner (affects GPU memory usage).
   * - ``--compress_fastq``
     - Compress output FASTQ files with gzip.
   * - ``--barcode_kits``
     - Barcode kit name(s) for demultiplexing during basecalling.
   * - ``--min_qscore``
     - Minimum quality score threshold for the pass/fail split.

Expected Output
---------------

Guppy creates a structured output directory:

* ``output/pass/`` -- FASTQ files for reads that meet the minimum quality
  score threshold.
* ``output/fail/`` -- FASTQ files for reads below the quality threshold.
* ``output/sequencing_summary.txt`` -- tab-delimited file with per-read
  statistics including read ID, run ID, channel, start time, duration,
  sequence length, and mean quality score.
* ``output/guppy_basecaller_log*.log`` -- basecalling log files.

If barcoding is enabled, reads are further separated into subdirectories named
by barcode (e.g., ``barcode01/``, ``barcode02/``).

See Also
--------

* :doc:`dorado` -- the recommended replacement for Guppy with improved
  basecalling accuracy
* :doc:`/tools/quality-control/nanoplot` -- quality assessment of basecalling
  output
* :doc:`/tools/quality-control/pycoqc` -- QC report from the sequencing
  summary file produced by Guppy
