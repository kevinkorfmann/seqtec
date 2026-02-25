Test Datasets
=============

Overview
--------

Before running a full analysis you need small test datasets to validate
your installation and learn each tool's interface. The NCBI Sequence Read
Archive (SRA) is the largest public repository of sequencing data. This
page shows how to download test FASTQ files using **fasterq-dump** (from
the SRA Toolkit) and the Python helper library **pysradb**.

Installation
------------

.. code-block:: bash

   # SRA Toolkit via Conda
   mamba install -c bioconda sra-tools

   # Python alternative
   pip install pysradb

Basic Usage
-----------

Download a single accession
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``fasterq-dump`` converts SRA archives into FASTQ files locally. Use
``--split-files`` so paired-end reads are written to separate R1/R2 files.

.. code-block:: bash

   # Download using fasterq-dump (recommended)
   fasterq-dump --split-files --threads 8 SRR12345678

Batch download
^^^^^^^^^^^^^^

Loop over a list of accessions, compress each FASTQ immediately to save
disk space.

.. code-block:: bash

   # Batch download
   for acc in SRR001 SRR002 SRR003; do
     fasterq-dump --split-files --threads 4 $acc
     gzip ${acc}*.fastq
   done

pysradb (Python alternative)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pysradb`` can download all runs belonging to a study (SRP) accession.

.. code-block:: bash

   # Python alternative
   pip install pysradb
   pysradb download -y -t 8 --out-dir ./data SRP123456

Nanopore test data
^^^^^^^^^^^^^^^^^^

Download a long-read Oxford Nanopore dataset for testing basecalling and
long-read alignment tools.

.. code-block:: bash

   mamba install -c bioconda sra-tools
   prefetch SRR28655382
   fasterq-dump --split-files SRR28655382
   samtools quickcheck SRR28655382.fastq

Key Parameters
--------------

fasterq-dump
^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag
     - Description
   * - ``--split-files``
     - Write paired-end reads into separate ``_1.fastq`` / ``_2.fastq`` files.
   * - ``--split-3``
     - Like ``--split-files`` but also writes unpaired reads to a third file.
   * - ``--threads``
     - Number of threads for decompression (default 6).
   * - ``--outdir``
     - Write output files to this directory.
   * - ``--temp``
     - Temporary directory for intermediate files (set to fast local storage).

pysradb
^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag
     - Description
   * - ``-y``
     - Skip confirmation prompts.
   * - ``-t``
     - Number of parallel download threads.
   * - ``--out-dir``
     - Output directory for downloaded files.

Expected Output
---------------

After downloading a paired-end Illumina run you will see:

.. code-block:: text

   SRR12345678_1.fastq   # Forward reads
   SRR12345678_2.fastq   # Reverse reads

Verify file integrity with a quick read count:

.. code-block:: bash

   wc -l SRR12345678_1.fastq | awk '{print $1/4}'

For the Nanopore test data:

.. code-block:: text

   SRR28655382.fastq     # Long reads in single-end FASTQ

See Also
--------

* :doc:`installation` -- set up Conda environments before downloading data
* :doc:`computing-environment` -- run downloads inside SLURM jobs on HPC
