VCF / BCF
=========

Overview
--------

VCF (Variant Call Format) is the standard file format for describing genetic
variants -- SNPs, insertions, deletions, and structural variants -- relative
to a reference genome. It is produced by every major variant caller (GATK
HaplotypeCaller, DeepVariant, bcftools, FreeBayes) and consumed by
annotation tools, filtering pipelines, and population-genetic analyses.

**BCF** is the binary, BGZF-compressed equivalent of VCF. It is
significantly faster to parse and is the recommended format for large
cohorts. The relationship between VCF and BCF mirrors that of SAM and BAM.

VCF files use the extension ``.vcf`` (plain text) or ``.vcf.gz``
(block-compressed with ``bgzip``). BCF files use ``.bcf``. Both compressed
formats support tabix or CSI indexing for fast regional queries.

Structure
---------

A VCF file has three parts: **meta-information lines**, a **header line**,
and **data lines**.

.. code-block:: text

   ##fileformat=VCFv4.3
   ##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
   ##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
   ##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
   ##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
   ##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
   #CHROM  POS     ID        REF  ALT  QUAL  FILTER  INFO          FORMAT     SAMPLE1
   chr1    12345   rs123456  A    G    99    PASS    DP=50;AF=0.5  GT:DP:GQ   0/1:50:99
   chr1    67890   .         CT   C    85    PASS    DP=40;AF=0.3  GT:DP:GQ   0/1:40:85

Meta-information lines
^^^^^^^^^^^^^^^^^^^^^^

Lines starting with ``##`` define the schema for INFO, FORMAT, FILTER, and
contig fields. They are machine-readable and describe every annotation that
appears in the data section.

Header line
^^^^^^^^^^^

The single line starting with ``#CHROM`` lists the eight mandatory columns
followed by one column per sample.

Data columns
^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 12 18 70

   * - Col
     - Field
     - Description
   * - 1
     - CHROM
     - Chromosome or contig name.
   * - 2
     - POS
     - 1-based position of the variant on the reference.
   * - 3
     - ID
     - Variant identifier (e.g. dbSNP rsID) or ``.`` if unknown.
   * - 4
     - REF
     - Reference allele(s).
   * - 5
     - ALT
     - Alternate allele(s), comma-separated for multi-allelic sites.
   * - 6
     - QUAL
     - Phred-scaled quality score for the variant call.
   * - 7
     - FILTER
     - ``PASS`` if the site passed all filters; otherwise a
       semicolon-separated list of filter names.
   * - 8
     - INFO
     - Semicolon-separated key-value pairs with site-level annotations.
   * - 9
     - FORMAT
     - Colon-separated keys defining the per-sample fields.
   * - 10+
     - SAMPLE
     - Per-sample genotype and annotations matching the FORMAT keys.

Genotype encoding
^^^^^^^^^^^^^^^^^

The **GT** (genotype) field uses indices into the REF/ALT alleles:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Genotype
     - Meaning
   * - ``0/0``
     - Homozygous reference
   * - ``0/1``
     - Heterozygous (one REF, one ALT)
   * - ``1/1``
     - Homozygous alternate
   * - ``1/2``
     - Heterozygous with two different ALT alleles
   * - ``./.``
     - Missing genotype (no call)
   * - ``0|1``
     - Phased heterozygous (``|`` indicates phase is known)

Variant types
^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Type
     - REF
     - ALT
     - Example
   * - SNP
     - ``A``
     - ``G``
     - Single nucleotide change
   * - Insertion
     - ``A``
     - ``ATG``
     - Two bases inserted after position
   * - Deletion
     - ``CT``
     - ``C``
     - One base deleted
   * - MNP
     - ``AT``
     - ``GC``
     - Multi-nucleotide polymorphism
   * - Complex
     - ``ACT``
     - ``GA``
     - Simultaneous insertion and deletion

Working With
------------

Compressing and indexing
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Block-compress with bgzip (NOT gzip)
   bgzip variants.vcf

   # Create a tabix index
   tabix -p vcf variants.vcf.gz

Viewing and querying
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # View VCF header
   bcftools view -h variants.vcf.gz

   # Query a specific region
   bcftools view variants.vcf.gz chr1:10000-50000

   # View only PASS variants
   bcftools view -f PASS variants.vcf.gz

Filtering variants
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Keep only biallelic SNPs with QUAL >= 30 and depth >= 10
   bcftools view -m2 -M2 -v snps variants.vcf.gz \
     | bcftools filter -i 'QUAL>=30 && INFO/DP>=10' -o filtered.vcf.gz -Oz

   # Exclude variants that failed filters
   bcftools view -f PASS variants.vcf.gz -o pass_only.vcf.gz -Oz

Statistics and summary
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Generate variant statistics
   bcftools stats variants.vcf.gz > stats.txt

   # Count variants by type
   bcftools stats variants.vcf.gz | grep '^SN'

Converting VCF to BCF and back
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # VCF to BCF
   bcftools view variants.vcf.gz -Ob -o variants.bcf
   bcftools index variants.bcf

   # BCF to VCF
   bcftools view variants.bcf -Oz -o variants.vcf.gz
   tabix -p vcf variants.vcf.gz

Merging and concatenating
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Merge VCFs from different samples (same sites)
   bcftools merge sample1.vcf.gz sample2.vcf.gz -Oz -o merged.vcf.gz

   # Concatenate VCFs from different regions (same samples)
   bcftools concat chr1.vcf.gz chr2.vcf.gz -Oz -o combined.vcf.gz

Extracting fields
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Extract specific fields as a tab-separated table
   bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t%QUAL\t[%GT]\n' \
     variants.vcf.gz > variants.tsv

See Also
--------

* :doc:`/tools/variant-calling/gatk` -- GATK HaplotypeCaller for germline
  variant calling
* :doc:`/tools/variant-calling/deepvariant` -- deep-learning variant caller
* :doc:`/tools/variant-processing/bcftools` -- the primary VCF/BCF
  manipulation toolkit
* :doc:`/tools/variant-annotation/snpeff` -- functional annotation of VCF
  variants
* :doc:`/tools/variant-annotation/vep` -- Ensembl Variant Effect Predictor
* :doc:`sam-bam-cram` -- the alignment format from which variants are called
* :doc:`bed` -- interval format often used for filtering VCF by region
