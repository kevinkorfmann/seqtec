SRA Toolkit
===========

Overview
--------

The SRA Toolkit is a collection of command-line utilities from NCBI for
downloading, converting, and validating data from the Sequence Read Archive
(SRA). Its primary tool, ``fasterq-dump``, extracts FASTQ files from SRA
accessions with multi-threaded performance, replacing the older ``fastq-dump``.
The toolkit also provides ``prefetch`` for downloading SRA files in advance,
``vdb-validate`` for verifying data integrity, and Aspera-based upload
utilities for submitting data to NCBI.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda sra-tools

After installation, configure the toolkit (sets the cache directory and
accepts NCBI terms):

.. code-block:: bash

   vdb-config --interactive

Basic Usage
-----------

**Download a single run**

.. code-block:: bash

   # Download using fasterq-dump (recommended)
   fasterq-dump --split-files --threads 8 SRR12345678

**Batch download multiple runs**

.. code-block:: bash

   for acc in SRR001 SRR002 SRR003; do
     fasterq-dump --split-files --threads 4 $acc
     gzip ${acc}*.fastq
   done

**Prefetch before extracting (recommended for large files)**

.. code-block:: bash

   prefetch SRR12345678
   fasterq-dump --split-files --threads 8 SRR12345678

**Submit data via Aspera**

.. code-block:: bash

   ascp -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh \
     -QT -l 1000m -k 1 \
     sample_R1.fastq.gz sample_R2.fastq.gz \
     subasp@upload.ncbi.nlm.nih.gov:uploads/your_folder/

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``--split-files``
     - Write paired-end reads to separate files (``_1.fastq`` and
       ``_2.fastq``).
   * - ``--split-3``
     - Like ``--split-files`` but also writes unpaired reads to a third file.
   * - ``--threads``
     - Number of threads for ``fasterq-dump`` (default: 6).
   * - ``--outdir``
     - Output directory for extracted FASTQ files.
   * - ``--temp``
     - Temporary directory for intermediate files (requires substantial disk
       space).
   * - ``--progress``
     - Show a progress bar during extraction.
   * - ``--skip-technical``
     - Skip technical reads (e.g., barcodes) and output only biological reads.
   * - ``-X`` (prefetch)
     - Maximum file size to download in KB (default: 20 GB).

Expected Output
---------------

For a paired-end run (e.g., ``SRR12345678``):

* ``SRR12345678_1.fastq`` -- Read 1 FASTQ file.
* ``SRR12345678_2.fastq`` -- Read 2 FASTQ file.

After compression:

* ``SRR12345678_1.fastq.gz`` / ``SRR12345678_2.fastq.gz``

For single-end runs, a single ``SRR12345678.fastq`` file is produced. The
``prefetch`` command downloads an ``.sra`` file to the local cache
(``~/ncbi/`` by default), which ``fasterq-dump`` then converts to FASTQ.

See Also
--------

* :doc:`entrez-direct` -- search NCBI databases (SRA, GEO) to discover
  accession numbers before downloading
* :doc:`/tools/quality-control/fastqc` -- quality-check downloaded FASTQ files
* :doc:`/tools/quality-control/fastp` -- trim and filter downloaded reads
  before alignment
