Entrez Direct
=============

Overview
--------

Entrez Direct (EDirect) is a set of NCBI command-line utilities for searching
and retrieving records from all Entrez databases, including SRA, GEO, PubMed,
Gene, and Nucleotide. The core commands -- ``esearch``, ``efetch``,
``elink``, and ``efilter`` -- can be piped together in Unix fashion to build
complex queries without writing API code. EDirect is essential for
programmatic discovery of public sequencing datasets, metadata extraction, and
automated literature searches in bioinformatics workflows.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda entrez-direct

Optionally set an NCBI API key for higher request rates (10 requests/second
instead of 3):

.. code-block:: bash

   export NCBI_API_KEY=your_api_key_here

Basic Usage
-----------

**Search SRA for ATAC-seq experiments**

.. code-block:: bash

   esearch -db sra -query "ATAC-seq[Strategy] AND Homo sapiens[Organism]" | \
     efetch -format runinfo | head -5

**Search GEO for scRNA-seq datasets**

.. code-block:: bash

   esearch -db gds -query "scRNA-seq AND Homo sapiens AND 2024[PDAT]" | \
     efetch -format summary | head -20

**Retrieve FASTA sequences from Nucleotide**

.. code-block:: bash

   esearch -db nucleotide -query "BRCA1 Homo sapiens[Organism] mRNA" | \
     efetch -format fasta | head -20

**Link from a GEO dataset to SRA runs**

.. code-block:: bash

   esearch -db gds -query "GSE123456" | \
     elink -target sra | \
     efetch -format runinfo

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-db`` (esearch)
     - Entrez database to search (``sra``, ``gds``, ``pubmed``, ``nucleotide``,
       ``gene``, etc.).
   * - ``-query`` (esearch)
     - Search query using Entrez query syntax. Supports field tags (e.g.,
       ``[Organism]``, ``[Strategy]``, ``[PDAT]``).
   * - ``-format`` (efetch)
     - Output format (``runinfo``, ``summary``, ``fasta``, ``xml``,
       ``docsum``, ``abstract``, etc.).
   * - ``-target`` (elink)
     - Target database for cross-database linking.
   * - ``-batch``
     - Process records in batch mode for large result sets.
   * - ``-retmax`` (esearch)
     - Maximum number of records to retrieve (default: 20 for efetch).

Expected Output
---------------

Output varies by database and format:

* **SRA runinfo** -- comma-separated table with columns for Run, ReleaseDate,
  LoadDate, spots, bases, avgLength, size_MB, download_path, Experiment,
  LibraryStrategy, LibrarySource, LibraryLayout, Platform, Model, SRAStudy,
  BioProject, BioSample, SampleName, and Organism.
* **GEO summary** -- text summaries of datasets including title, description,
  platform, and sample counts.
* **FASTA** -- nucleotide or protein sequences in standard FASTA format.
* **XML / DocSum** -- structured metadata records suitable for parsing.

All output is written to standard output, making it easy to pipe to downstream
tools or redirect to files.

See Also
--------

* :doc:`sra-toolkit` -- download FASTQ files from SRA using accessions
  discovered with Entrez Direct
