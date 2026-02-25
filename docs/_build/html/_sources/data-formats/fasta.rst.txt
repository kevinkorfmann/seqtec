FASTA
=====

Overview
--------

FASTA is the simplest and most widely used format for representing nucleotide
or protein sequences. Unlike FASTQ, it carries **no quality information** --
only a header line and the sequence itself. FASTA files serve as the standard
format for:

* **Reference genomes** (e.g. ``GRCh38.fa``)
* **Transcript sequences** (e.g. ``gencode.v44.transcripts.fa``)
* **Protein databases** (e.g. UniProt FASTA downloads)
* **De novo assembly contigs** and scaffolds
* **Consensus sequences** from multiple-sequence alignment

FASTA files use the extensions ``.fa``, ``.fasta``, ``.fna`` (nucleotide),
or ``.faa`` (amino acid). They are plain-text and are frequently compressed
with ``gzip`` or block-compressed with ``bgzip`` for indexed random access.

Structure
---------

A FASTA file consists of one or more records. Each record starts with a
``>`` header line followed by one or more lines of sequence:

.. code-block:: text

   >chr1 Homo sapiens chromosome 1
   NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
   NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNGATAATCTACTACTACTCAG
   TGGCCAACACCTGATCCTGACAGCTGGAGTAAGGAACCTGAAGTCCCTA
   AAACTCATCAATGTTCTTTAGAGACTTACCAGGACCACTTCGTGAGGGA
   >chr2 Homo sapiens chromosome 2
   NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
   AGAGATCAGCTCAGGAGAGTCTCTTGAAGAAATCTGATTCACTGTATGG

**Header line (starts with** ``>`` **)**
   Everything after ``>`` up to the first whitespace is the **sequence
   identifier** (e.g. ``chr1``). The remainder of the line is a free-text
   description (e.g. ``Homo sapiens chromosome 1``).

**Sequence lines**
   Contain the actual nucleotide (A, C, G, T, N) or amino acid characters.
   Lines are typically wrapped at 60 or 80 characters, although single-line
   sequences are also valid.

FASTA index (``.fai``)
^^^^^^^^^^^^^^^^^^^^^^

Tools such as ``samtools`` and ``bedtools`` require a FASTA index to perform
random access into a reference genome. The index is a tab-separated file with
one row per sequence:

.. code-block:: text

   chr1  248956422  112  80  81
   chr2  242193529  253404903  80  81

Columns: name, length, byte offset, bases per line, bytes per line.

Working With
------------

Indexing a reference
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Create a .fai index (required by most aligners and variant callers)
   samtools faidx reference.fa

   # Block-compress and index for fast random access
   bgzip reference.fa            # produces reference.fa.gz
   samtools faidx reference.fa.gz

Extracting a region
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Extract chr1:10000-20000 from an indexed FASTA
   samtools faidx reference.fa chr1:10000-20000

Counting sequences and total bases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Count the number of sequences
   grep -c '^>' reference.fa

   # Count total bases (excluding headers and newlines)
   grep -v '^>' reference.fa | tr -d '\n' | wc -c

Creating aligner indices
^^^^^^^^^^^^^^^^^^^^^^^^

Most aligners build their own index from the FASTA reference:

.. code-block:: bash

   # BWA-MEM2 index
   bwa-mem2 index reference.fa

   # STAR genome generate for RNA-seq
   STAR --runMode genomeGenerate \
     --genomeDir star_index/ \
     --genomeFastaFiles reference.fa \
     --sjdbGTFfile genes.gtf \
     --runThreadN 8

   # HISAT2 index
   hisat2-build reference.fa hisat2_index/genome

Getting genome information
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Create a genome file (chromosome sizes) from the index
   cut -f1,2 reference.fa.fai > chrom.sizes

   # Generate a sequence dictionary (required by GATK / Picard)
   samtools dict reference.fa -o reference.dict

See Also
--------

* :doc:`fastq` -- sequence format that includes per-base quality scores
* :doc:`sam-bam-cram` -- alignment format that maps reads against a FASTA
  reference
* :doc:`/tools/alignment/bwa-mem2` -- short-read aligner that requires a
  FASTA reference index
* :doc:`/tools/sam-bam-processing/samtools` -- ``samtools faidx`` for indexing
  and region extraction
* :doc:`/tools/assembly/spades` -- de novo assembler that produces FASTA
  contigs
