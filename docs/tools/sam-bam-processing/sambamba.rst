Sambamba
========

Overview
--------

Sambamba is a high-performance tool for processing BAM and CRAM files, designed
as a drop-in complement to SAMtools with substantially better multi-threading
support. Its most common uses are duplicate marking, sorting, and filtering. By
distributing work across many CPU cores, Sambamba can significantly reduce
wall-clock time for routine BAM processing steps, making it particularly
attractive for large whole-genome sequencing datasets.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda sambamba

Basic Usage
-----------

**Mark PCR / optical duplicates**

.. code-block:: bash

   sambamba markdup -t 8 sample.sorted.bam sample.dedup.bam

**Sort a BAM file by coordinate**

.. code-block:: bash

   sambamba sort -t 8 -o sample.sorted.bam sample.bam

**Filter reads using an expression**

.. code-block:: bash

   sambamba view -t 8 -f bam -F "mapping_quality >= 30 and not duplicate" \
     sample.bam > filtered.bam

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-t THREADS``
     - Number of threads to use for processing.
   * - ``-o FILE``
     - Write output to *FILE*.
   * - ``-f FORMAT``
     - Output format: ``bam``, ``sam``, or ``json``.
   * - ``-F FILTER``
     - A filter expression for selecting reads (e.g.,
       ``"mapping_quality >= 30 and not duplicate"``).
   * - ``--tmpdir DIR``
     - Directory for temporary files during sorting (defaults to the current
       directory).
   * - ``--overflow-list-size INT``
     - Size of the overflow hash table list used during duplicate marking; tune
       for very large files.
   * - ``-l INT``
     - Compression level for BAM output (0--9).

Expected Output
---------------

* ``sambamba markdup`` -- a BAM file with the duplicate FLAG bit (0x400) set on
  identified PCR or optical duplicates. Duplicates are retained by default and
  can be filtered later.
* ``sambamba sort`` -- a coordinate-sorted (or name-sorted with ``-n``) BAM
  file.
* ``sambamba view`` -- filtered reads written to a BAM, SAM, or JSON file
  depending on the ``-f`` option.

See Also
--------

* :doc:`samtools` -- the reference toolkit for SAM/BAM manipulation
* :doc:`picard` -- alternative duplicate marking with detailed duplicate
  metrics output
* :doc:`/data-formats/sam-bam-cram` -- reference for the SAM/BAM/CRAM file
  formats
