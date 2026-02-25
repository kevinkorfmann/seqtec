Dorado
======

Overview
--------

Dorado is Oxford Nanopore Technologies' (ONT) current basecaller for
converting raw electrical signal data into nucleotide sequences. It replaces
the legacy Guppy basecaller and provides improved accuracy through updated
neural network architectures. Dorado natively reads POD5 files (ONT's current
raw data format) and outputs aligned or unaligned BAM files with per-read
quality scores and move tables. It supports multiple accuracy tiers (fast,
high-accuracy, super-accuracy) and can perform modified base detection
(e.g., 5mC, 6mA methylation) during basecalling.

Installation
------------

Download the latest Dorado release from the
`Oxford Nanopore Technologies GitHub <https://github.com/nanoporetech/dorado>`_.
Pre-compiled binaries are available for Linux (x86_64, aarch64) and macOS.

.. code-block:: bash

   # Example for Linux x86_64
   wget https://github.com/nanoporetech/dorado/releases/latest/download/dorado-<version>-linux-x64.tar.gz
   tar -xzf dorado-<version>-linux-x64.tar.gz
   export PATH=$PWD/dorado-<version>-linux-x64/bin:$PATH

Dorado requires a CUDA-capable GPU for optimal performance, though CPU-only
execution is supported.

Basic Usage
-----------

Download a basecalling model and run basecalling on a directory of POD5 files.

.. code-block:: bash

   # Download basecalling model
   dorado download --model dna_r10.4.1_e8.2_400bps_sup@v5.0.0

   # Basecall POD5 files
   dorado basecaller dna_r10.4.1_e8.2_400bps_sup@v5.0.0 \
     pod5_dir/ \
     --device cuda:0 \
     > calls.bam

   # Convert to FASTQ if needed
   samtools fastq calls.bam | gzip > reads.fastq.gz

For modified base calling (e.g., 5mC CpG methylation):

.. code-block:: bash

   dorado basecaller dna_r10.4.1_e8.2_400bps_sup@v5.0.0 \
     pod5_dir/ \
     --device cuda:0 \
     --modified-bases 5mCG_5hmCG \
     > calls_modbase.bam

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``--model``
     - Basecalling model to download or use (e.g.,
       ``dna_r10.4.1_e8.2_400bps_sup@v5.0.0``). Must match the flow cell and
       kit chemistry.
   * - ``--device``
     - Compute device (``cuda:0``, ``cuda:all``, or ``cpu``).
   * - ``--modified-bases``
     - Detect modified bases during basecalling (e.g., ``5mCG_5hmCG`` for
       5-methylcytosine and 5-hydroxymethylcytosine in CpG context).
   * - ``--emit-moves``
     - Include move table information in the output BAM (useful for signal-level
       analysis).
   * - ``--min-qscore``
     - Minimum quality score threshold; reads below this are filtered out.
   * - ``--recursive``
     - Recursively search input directories for POD5 files.
   * - ``--batchsize``
     - Number of reads per batch (affects GPU memory usage).
   * - ``--reference``
     - Reference FASTA for direct alignment during basecalling (outputs aligned
       BAM).

Expected Output
---------------

* ``calls.bam`` -- unaligned BAM file containing basecalled reads with quality
  scores, read group information, and optional modified base tags. Each record
  corresponds to one nanopore read.
* ``reads.fastq.gz`` -- FASTQ file converted from the BAM output (if the
  conversion step is run).

When ``--reference`` is provided, the output is an aligned, sorted BAM file
that can be indexed directly with ``samtools index``.

See Also
--------

* :doc:`guppy` -- legacy ONT basecaller (superseded by Dorado)
* :doc:`/tools/quality-control/nanoplot` -- quality assessment of nanopore
  basecalling output
* :doc:`/tools/quality-control/chopper` -- length and quality filtering of
  nanopore reads
* :doc:`/tools/alignment/minimap2` -- long-read aligner for mapping basecalled
  reads to a reference
