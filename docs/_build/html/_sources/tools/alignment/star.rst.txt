STAR
====

Overview
--------

STAR (Spliced Transcripts Alignment to a Reference) is a fast RNA-seq aligner
that discovers splice junctions during alignment, making it the standard
choice for mapping RNA-seq reads to a reference genome. STAR uses an uncompressed
suffix array index for rapid seed finding and supports two-pass alignment
for improved novel junction detection. It can output gene-level read counts
directly, which is convenient for differential expression workflows.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda star

Basic Usage
-----------

STAR requires a genome index to be generated before alignment. The index
incorporates known splice junctions from a GTF annotation file.

.. code-block:: bash

   # Generate genome index
   STAR --runMode genomeGenerate \
     --genomeDir star_index/ \
     --genomeFastaFiles reference.fa \
     --sjdbGTFfile genes.gtf \
     --runThreadN 8

   # Align RNA-seq reads
   STAR --runMode alignReads \
     --genomeDir star_index/ \
     --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
     --readFilesCommand zcat \
     --outSAMtype BAM SortedByCoordinate \
     --quantMode GeneCounts \
     --outFileNamePrefix sample_ \
     --runThreadN 8

.. note::

   Genome index generation requires substantial memory. For the human genome,
   allocate at least 32 GB of RAM. Use ``--genomeSAindexNbases`` to reduce
   memory requirements for smaller genomes.

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``--runMode``
     - Operation mode: ``genomeGenerate`` for indexing, ``alignReads`` for
       alignment (default).
   * - ``--genomeDir``
     - Path to the genome index directory.
   * - ``--genomeFastaFiles``
     - Reference genome FASTA file(s) (for index generation).
   * - ``--sjdbGTFfile``
     - Gene annotation in GTF format (provides known splice junctions).
   * - ``--readFilesIn``
     - Input FASTQ file(s). For paired-end, supply read 1 and read 2
       separated by a space.
   * - ``--readFilesCommand``
     - Command to decompress input files (e.g., ``zcat`` for ``.gz``).
   * - ``--outSAMtype``
     - Output format. ``BAM SortedByCoordinate`` produces a sorted BAM
       directly.
   * - ``--quantMode``
     - ``GeneCounts`` outputs a gene-level count table alongside the BAM.
   * - ``--outFileNamePrefix``
     - Prefix for all output file names.
   * - ``--runThreadN``
     - Number of threads.
   * - ``--twopassMode Basic``
     - Enable STAR's two-pass mode for improved novel splice junction
       detection.
   * - ``--sjdbOverhang``
     - Read length minus 1 (default 100). Set to match your read length for
       optimal sensitivity.
   * - ``--outSAMattributes``
     - SAM attributes to include (e.g., ``NH HI AS NM MD``).

Expected Output
---------------

With the parameters above, STAR produces the following files (all prefixed
with ``sample_``):

* ``sample_Aligned.sortedByCoord.out.bam`` -- coordinate-sorted BAM file of
  aligned reads.
* ``sample_ReadsPerGene.out.tab`` -- gene-level read counts (when
  ``--quantMode GeneCounts`` is set). Columns correspond to unstranded,
  sense-strand, and antisense-strand counts.
* ``sample_Log.final.out`` -- alignment summary statistics including total
  reads, uniquely mapped reads, multi-mapped reads, and splice junction
  counts.
* ``sample_Log.out`` -- detailed run log.
* ``sample_SJ.out.tab`` -- splice junctions detected during alignment.

Index the BAM file for downstream use:

.. code-block:: bash

   samtools index sample_Aligned.sortedByCoord.out.bam

See Also
--------

* :doc:`/tools/quality-control/fastqc` -- quality control before alignment
* :doc:`/tools/quality-control/multiqc` -- aggregate STAR log files across
  samples
* :doc:`/tools/quantification/index` -- transcript-level and gene-level
  quantification tools
* :doc:`/tools/differential-expression/index` -- differential expression
  analysis tools
* :doc:`/data-formats/fastq` -- reference for the FASTQ file format
* :doc:`/data-formats/sam-bam-cram` -- reference for the SAM/BAM/CRAM
  alignment format
* :doc:`/data-formats/gff-gtf` -- reference for the GTF annotation format
