SAM / BAM / CRAM
================

Overview
--------

SAM (Sequence Alignment/Map), BAM, and CRAM are the standard formats for
storing sequencing reads that have been aligned to a reference genome. They
are produced by every major aligner (BWA-MEM2, STAR, Minimap2, HISAT2) and
consumed by virtually every downstream tool -- from variant callers to
coverage calculators.

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Format
     - Extension
     - Description
   * - **SAM**
     - ``.sam``
     - Human-readable plain text. Useful for inspection but too large for
       storage.
   * - **BAM**
     - ``.bam``
     - Binary, BGZF-compressed SAM. The de facto working format -- fast to
       read and supports indexing.
   * - **CRAM**
     - ``.cram``
     - Reference-based compression of BAM. Achieves 40--60 % smaller files
       by encoding only the differences from the reference.

BAM and CRAM files require a companion **index** (``.bai`` / ``.csi`` /
``.crai``) for random access by genomic coordinate.

Structure
---------

A SAM file has two sections: a **header** (lines starting with ``@``) and
**alignment records** (one tab-separated line per read).

.. code-block:: text

   @HD VN:1.6  SO:coordinate
   @SQ SN:chr1 LN:248956422
   @RG ID:sample1 SM:sample1 PL:ILLUMINA
   read001  99  chr1  10050  60  151M  =  10250  351  ACGTACGT...  JJJJJJJJ...
   read001  147 chr1  10250  60  151M  =  10050  -351 TGCATGCA...  JJJJJJJJ...

Header section
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Tag
     - Purpose
   * - ``@HD``
     - File-level metadata: format version (``VN``), sort order (``SO``).
   * - ``@SQ``
     - Reference sequence dictionary: name (``SN``) and length (``LN``) of
       each chromosome.
   * - ``@RG``
     - Read group: sample name (``SM``), platform (``PL``), library (``LB``).
       Critical for multi-sample calling.
   * - ``@PG``
     - Program record: which tool produced this file and with what arguments.

Alignment records
^^^^^^^^^^^^^^^^^

Each alignment line has 11 mandatory fields:

.. list-table::
   :header-rows: 1
   :widths: 10 18 72

   * - Col
     - Field
     - Description
   * - 1
     - QNAME
     - Read name.
   * - 2
     - FLAG
     - Bitwise flag encoding read properties (see below).
   * - 3
     - RNAME
     - Reference sequence name (e.g. ``chr1``).
   * - 4
     - POS
     - 1-based leftmost mapping position.
   * - 5
     - MAPQ
     - Mapping quality (Phred-scaled probability the position is wrong).
   * - 6
     - CIGAR
     - Alignment description string (see below).
   * - 7
     - RNEXT
     - Reference for the mate (``=`` if same chromosome).
   * - 8
     - PNEXT
     - Mate's mapping position.
   * - 9
     - TLEN
     - Template/insert length.
   * - 10
     - SEQ
     - Read sequence.
   * - 11
     - QUAL
     - Base quality string (same Phred+33 encoding as FASTQ).

FLAG field
^^^^^^^^^^

The FLAG is a sum of bit values. Common flags:

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Bit
     - Decimal
     - Meaning
   * - 0x1
     - 1
     - Read is paired
   * - 0x2
     - 2
     - Both reads mapped in a proper pair
   * - 0x4
     - 4
     - Read is unmapped
   * - 0x8
     - 8
     - Mate is unmapped
   * - 0x10
     - 16
     - Read mapped to reverse strand
   * - 0x20
     - 32
     - Mate mapped to reverse strand
   * - 0x40
     - 64
     - First in pair (R1)
   * - 0x80
     - 128
     - Second in pair (R2)
   * - 0x100
     - 256
     - Secondary alignment
   * - 0x400
     - 1024
     - PCR or optical duplicate
   * - 0x800
     - 2048
     - Supplementary alignment

In the example above, ``99 = 1 + 2 + 32 + 64`` means: paired, proper pair,
mate on reverse strand, first in pair. ``147 = 1 + 2 + 16 + 128`` means:
paired, proper pair, this read on reverse strand, second in pair.

.. tip::

   Use the `Picard explain flags <https://broadinstitute.github.io/picard/explain-flags.html>`_
   web tool or ``samtools flags 99`` to decode any FLAG value.

CIGAR strings
^^^^^^^^^^^^^

The CIGAR (Compact Idiosyncratic Gapped Alignment Report) string describes
how the read aligns to the reference:

.. list-table::
   :header-rows: 1
   :widths: 10 40 50

   * - Op
     - Name
     - Meaning
   * - ``M``
     - Match / mismatch
     - Aligned (consumed from both read and reference)
   * - ``I``
     - Insertion
     - Bases in read not in reference
   * - ``D``
     - Deletion
     - Bases in reference not in read
   * - ``N``
     - Skipped region
     - Intron in RNA-seq spliced alignment
   * - ``S``
     - Soft clip
     - Bases present in read but not aligned
   * - ``H``
     - Hard clip
     - Bases removed from read entirely

Examples:

* ``151M`` -- simple end-to-end alignment of 151 bp
* ``50M2I99M`` -- 50 bp match, 2 bp insertion, 99 bp match
* ``75M5000N76M`` -- spliced RNA-seq read spanning a 5 kb intron
* ``5S146M`` -- 5 soft-clipped bases at the start

MAPQ scores
^^^^^^^^^^^^

Mapping quality (MAPQ) is a Phred-scaled estimate of the probability that
the alignment position is incorrect:

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - MAPQ
     - Error rate
     - Interpretation
   * - 0
     - 1 in 1
     - Multi-mapped; position unreliable
   * - 20
     - 1 in 100
     - Moderately confident
   * - 30
     - 1 in 1 000
     - High confidence
   * - 60
     - 1 in 1 000 000
     - Unique alignment (BWA-MEM2 max)
   * - 255
     - --
     - Not available (used by some tools)

Most variant callers require ``MAPQ >= 20`` or higher.

Working With
------------

Converting and sorting
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Convert SAM to sorted BAM
   samtools sort -@ 8 -o aligned.sorted.bam aligned.sam

   # Index the BAM
   samtools index aligned.sorted.bam

Viewing alignments
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # View header
   samtools view -H aligned.sorted.bam

   # View alignments in a specific region
   samtools view aligned.sorted.bam chr1:10000-20000

   # View only properly paired reads with MAPQ >= 30
   samtools view -f 2 -q 30 aligned.sorted.bam

Flagstat and idxstats
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Summary alignment statistics
   samtools flagstat aligned.sorted.bam

   # Per-chromosome read counts
   samtools idxstats aligned.sorted.bam

Marking duplicates
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Mark PCR duplicates with samtools
   samtools markdup aligned.sorted.bam dedup.bam

   # Or with Picard
   picard MarkDuplicates \
     I=aligned.sorted.bam \
     O=dedup.bam \
     M=dup_metrics.txt

Converting BAM to CRAM
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Compress BAM into CRAM (requires reference FASTA)
   samtools view -C -T reference.fa -o aligned.cram aligned.sorted.bam
   samtools index aligned.cram

Computing depth and coverage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Per-base depth
   samtools depth -a aligned.sorted.bam > depth.txt

   # Coverage summary
   samtools coverage aligned.sorted.bam

See Also
--------

* :doc:`/tools/sam-bam-processing/samtools` -- the primary toolkit for SAM/BAM/CRAM
  manipulation
* :doc:`/tools/sam-bam-processing/sambamba` -- fast BAM processing with
  multithreading
* :doc:`/tools/sam-bam-processing/picard` -- duplicate marking and BAM
  validation
* :doc:`/tools/sam-bam-processing/deeptools` -- coverage tracks and QC plots
  from BAM files
* :doc:`/tools/alignment/bwa-mem2` -- short-read aligner producing SAM output
* :doc:`fastq` -- the raw read format that is aligned to produce SAM/BAM
* :doc:`vcf-bcf` -- variant calls derived from BAM alignments
