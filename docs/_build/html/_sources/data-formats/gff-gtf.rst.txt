GFF / GTF
=========

Overview
--------

GFF (General Feature Format) and GTF (Gene Transfer Format) are tab-delimited
formats for describing genomic features -- genes, transcripts, exons, CDS
regions, UTRs, and other annotations. They are the standard output of genome
annotation pipelines and the required input for RNA-seq quantification,
spliced alignment, and functional analysis.

The two formats share the same nine-column layout but differ in how the
**attributes column** (column 9) is structured:

.. list-table::
   :header-rows: 1
   :widths: 15 20 65

   * - Format
     - Also known as
     - Attribute style
   * - **GTF**
     - GFF2 / GFF2.5
     - Key-value pairs: ``gene_id "ENSG..."; gene_name "DDX11L1";``
   * - **GFF3**
     - GFF version 3
     - Key=value pairs: ``ID=gene0;Name=DDX11L1;biotype=lncRNA``

GTF is used predominantly by **GENCODE**, **Ensembl**, and tools in the
RNA-seq ecosystem (STAR, featureCounts, HTSeq, StringTie). GFF3 is the
official sequence ontology standard and is preferred by **NCBI RefSeq** and
many non-model organism databases.

.. important::

   Both GFF and GTF use **1-based, fully closed** coordinates. The interval
   covering bases 1 through 100 is written as ``start=1  end=100``. This
   differs from BED, which uses 0-based, half-open coordinates.

Structure
---------

Both formats use nine tab-separated columns:

.. code-block:: text

   chr1  HAVANA  gene        11869  14409  .  +  .  gene_id "ENSG00000223972"; gene_name "DDX11L1";
   chr1  HAVANA  transcript  11869  14409  .  +  .  gene_id "ENSG00000223972"; transcript_id "ENST00000456328";
   chr1  HAVANA  exon        11869  12227  .  +  .  gene_id "ENSG00000223972"; transcript_id "ENST00000456328";
   chr1  HAVANA  exon        12613  12721  .  +  .  gene_id "ENSG00000223972"; transcript_id "ENST00000456328";
   chr1  HAVANA  exon        13221  14409  .  +  .  gene_id "ENSG00000223972"; transcript_id "ENST00000456328";

Column definitions
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 8 18 74

   * - Col
     - Field
     - Description
   * - 1
     - seqname
     - Chromosome or contig name (e.g. ``chr1``).
   * - 2
     - source
     - Annotation source or program (e.g. ``HAVANA``, ``ENSEMBL``).
   * - 3
     - feature
     - Feature type: ``gene``, ``transcript``, ``exon``, ``CDS``, ``UTR``,
       ``start_codon``, ``stop_codon``, etc.
   * - 4
     - start
     - Start position (1-based, inclusive).
   * - 5
     - end
     - End position (1-based, inclusive).
   * - 6
     - score
     - Numeric score or ``.`` if not applicable.
   * - 7
     - strand
     - ``+`` (forward), ``-`` (reverse), or ``.`` (unstranded).
   * - 8
     - frame
     - Reading frame for CDS features: ``0``, ``1``, ``2``, or ``.``.
   * - 9
     - attributes
     - Semicolon-separated key-value pairs (format differs between GTF and
       GFF3).

GTF vs GFF3 attributes
^^^^^^^^^^^^^^^^^^^^^^^

**GTF (GFF2) style:**

.. code-block:: text

   gene_id "ENSG00000223972"; transcript_id "ENST00000456328"; gene_name "DDX11L1"; gene_biotype "lncRNA";

* Keys and values separated by a space.
* Values enclosed in double quotes.
* Entries terminated by a semicolon.
* ``gene_id`` and ``transcript_id`` are mandatory.

**GFF3 style:**

.. code-block:: text

   ID=gene-DDX11L1;Name=DDX11L1;gene_id=ENSG00000223972;gene_biotype=lncRNA

* Key=value pairs separated by semicolons (no trailing semicolon).
* Values are **not** quoted.
* ``ID`` provides a unique identifier for the feature.
* ``Parent`` links child features (exons, CDS) to their parent (transcript,
  gene).
* Hierarchical relationships are explicit through ``ID``/``Parent`` links.

Feature hierarchy
^^^^^^^^^^^^^^^^^

Annotations follow a nested hierarchy:

.. code-block:: text

   gene
     transcript (mRNA)
       exon
       CDS
       five_prime_UTR
       three_prime_UTR

In GTF, the hierarchy is implicit -- features are grouped by shared
``gene_id`` and ``transcript_id`` values. In GFF3, the hierarchy is explicit
through ``ID`` and ``Parent`` attributes.

Working With
------------

Downloading annotations
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # GENCODE human GTF (widely used for RNA-seq)
   wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_44/gencode.v44.annotation.gtf.gz

   # NCBI RefSeq GFF3
   wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.gff.gz

Extracting specific features
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Extract only gene-level features from a GTF
   awk '$3 == "gene"' annotation.gtf > genes_only.gtf

   # Extract protein-coding genes
   awk '$3 == "gene" && /gene_biotype "protein_coding"/' annotation.gtf > protein_coding.gtf

   # Extract exon coordinates as a BED file (converting 1-based to 0-based)
   awk 'BEGIN{OFS="\t"} $3=="exon" {print $1, $4-1, $5, ".", ".", $7}' \
     annotation.gtf > exons.bed

Using with RNA-seq aligners
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # STAR genome generation with GTF
   STAR --runMode genomeGenerate \
     --genomeDir star_index/ \
     --genomeFastaFiles reference.fa \
     --sjdbGTFfile annotation.gtf \
     --runThreadN 8

   # HISAT2 with splice sites extracted from GTF
   hisat2_extract_splice_sites.py annotation.gtf > splice_sites.txt
   hisat2_extract_exons.py annotation.gtf > exons.txt

Counting reads per gene
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # featureCounts (from Subread package)
   featureCounts -a annotation.gtf -o counts.txt \
     -T 8 -p --countReadPairs aligned.sorted.bam

   # HTSeq
   htseq-count -f bam -r pos -s reverse \
     aligned.sorted.bam annotation.gtf > counts.txt

Converting between formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # GFF3 to GTF with gffread
   gffread annotation.gff3 -T -o annotation.gtf

   # GTF to GFF3
   gffread annotation.gtf -o annotation.gff3

   # Convert GTF to BED12 (transcript models)
   gtfToGenePred annotation.gtf /dev/stdout \
     | genePredToBed /dev/stdin > transcripts.bed

Sorting GTF/GFF files
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Sort by chromosome and start position
   sort -k1,1 -k4,4n annotation.gtf > sorted.gtf

See Also
--------

* :doc:`/tools/quantification/featurecounts` -- count reads using GTF
  annotations
* :doc:`/tools/quantification/htseq` -- alternative read counting tool
* :doc:`/tools/annotation/prokka` -- prokaryotic annotation producing GFF3
* :doc:`bed` -- simpler interval format (0-based, half-open coordinates)
* :doc:`fasta` -- the reference genome that annotations describe
* :doc:`sam-bam-cram` -- alignment format used together with GTF for
  quantification
