FASTQ
=====

Overview
--------

FASTQ is the universal file format for storing raw sequencing reads together
with their per-base quality scores. Every Illumina, PacBio, and Oxford
Nanopore sequencing run produces FASTQ files (or an intermediate format that
is converted to FASTQ). It is the starting point for virtually every NGS
analysis pipeline -- from quality control and trimming through alignment,
assembly, and quantification.

FASTQ files are plain-text and typically compressed with **gzip**
(``*.fastq.gz`` or ``*.fq.gz``). A single whole-genome sequencing experiment
at 30x coverage produces roughly 60--90 GB of compressed FASTQ data.

Structure
---------

Each read occupies exactly **four lines**:

.. code-block:: text

   @NB501234:45:H3YTNBGX3:1:11101:24563:1038 1:N:0:ACGTACGT
   NTGCAAGCAGTTCAGGATCAGTCGAGACTTCAATGTCGATCTACGTAGC
   +
   #AAFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

**Line 1 -- Header (starts with** ``@`` **)**
   Contains the read identifier. In the Illumina convention the fields are
   colon-separated:

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Field
        - Meaning
      * - ``NB501234``
        - Instrument name
      * - ``45``
        - Run ID
      * - ``H3YTNBGX3``
        - Flowcell ID
      * - ``1``
        - Lane
      * - ``11101``
        - Tile number
      * - ``24563``
        - X coordinate on tile
      * - ``1038``
        - Y coordinate on tile

   After the space, ``1:N:0:ACGTACGT`` encodes: read number (``1`` = R1,
   ``2`` = R2), filter flag (``N`` = not filtered), control bits, and the
   index/barcode sequence.

**Line 2 -- Sequence**
   The nucleotide sequence of the read. Characters are A, C, G, T, and N
   (undetermined base).

**Line 3 -- Separator (** ``+`` **)**
   A literal ``+`` character. It may optionally repeat the header but this is
   rarely done in modern files.

**Line 4 -- Quality string**
   One ASCII character per base encoding the Phred quality score.

Phred quality encoding
^^^^^^^^^^^^^^^^^^^^^^

Modern instruments use the **Sanger / Phred+33** encoding. The quality score
for a base is computed as:

.. code-block:: text

   Q = -10 * log10(P_error)

The score is stored as the character with ASCII code ``Q + 33``. Common
values:

.. list-table::
   :header-rows: 1
   :widths: 15 15 30 40

   * - ASCII
     - Q
     - Error rate
     - Interpretation
   * - ``!``
     - 0
     - 1 in 1
     - Worst quality
   * - ``#``
     - 2
     - 1 in 1.6
     - Very poor
   * - ``+``
     - 10
     - 1 in 10
     - Low quality
   * - ``5``
     - 20
     - 1 in 100
     - Acceptable
   * - ``?``
     - 30
     - 1 in 1 000
     - Good
   * - ``I``
     - 40
     - 1 in 10 000
     - Excellent (Illumina max)
   * - ``J``
     - 41
     - 1 in 12 589
     - NovaSeq 6000 max

Paired-end conventions
^^^^^^^^^^^^^^^^^^^^^^

Paired-end libraries produce **two FASTQ files** (or an interleaved file).
The standard naming convention is:

.. code-block:: text

   sample_R1.fastq.gz   # forward reads  (read 1)
   sample_R2.fastq.gz   # reverse reads  (read 2)

Reads at the same position in both files form a pair. Tools such as
``fastp`` and ``BWA-MEM2`` accept the two files as positional arguments and
preserve pairing automatically:

.. code-block:: bash

   fastp \
     -i sample_R1.fastq.gz -I sample_R2.fastq.gz \
     -o sample_R1.trimmed.fq.gz -O sample_R2.trimmed.fq.gz

Working With
------------

Counting reads
^^^^^^^^^^^^^^

Because every read occupies exactly four lines, the total number of reads in
a FASTQ file is the line count divided by four:

.. code-block:: bash

   # Count reads in a gzipped FASTQ
   echo $(( $(zcat sample_R1.fastq.gz | wc -l) / 4 ))

Viewing the first reads
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Show the first two reads
   zcat sample_R1.fastq.gz | head -8

Quality inspection
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Run FastQC on paired-end files
   fastqc sample_R1.fastq.gz sample_R2.fastq.gz -o qc_reports/

Quality trimming and adapter removal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Trim with fastp
   fastp \
     -i sample_R1.fastq.gz -I sample_R2.fastq.gz \
     -o sample_R1.trimmed.fq.gz -O sample_R2.trimmed.fq.gz \
     --detect_adapter_for_pe \
     --qualified_quality_phred 20 \
     --length_required 50

Subsetting reads
^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Extract the first 1 million reads with seqtk
   seqtk sample -s42 sample_R1.fastq.gz 1000000 \
     | gzip > sample_R1.sub.fq.gz

Converting from BAM back to FASTQ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Extract reads from a BAM file
   samtools fastq -1 sample_R1.fq.gz -2 sample_R2.fq.gz \
     -0 /dev/null -s /dev/null -n input.bam

See Also
--------

* :doc:`/tools/quality-control/fastqc` -- per-base quality visualisation
* :doc:`/tools/quality-control/fastp` -- all-in-one trimming and QC
* :doc:`/tools/quality-control/multiqc` -- aggregate QC reports
* :doc:`/tools/quality-control/nanoplot` -- quality plots for long-read FASTQ
* :doc:`fasta` -- related sequence-only format (no quality scores)
* :doc:`sam-bam-cram` -- the alignment format that FASTQ reads are mapped into
