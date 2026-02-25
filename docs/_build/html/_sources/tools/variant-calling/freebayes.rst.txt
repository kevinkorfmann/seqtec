FreeBayes
=========

Overview
--------

FreeBayes is a haplotype-based Bayesian variant caller for detecting SNPs,
indels, MNPs, and complex events from short-read sequencing data. Unlike
position-level callers, FreeBayes considers the haplotype context surrounding
each variant site, improving accuracy in regions with clustered polymorphisms.
It works directly from a sorted BAM file and a reference genome without
requiring a multi-step GVCF workflow, making it a straightforward choice for
single-sample and small-cohort variant calling. FreeBayes supports pooled
sequencing, polyploid genomes, and population-level priors.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda freebayes

Basic Usage
-----------

Call variants from a single sorted BAM file with minimum quality filters.

.. code-block:: bash

   freebayes -f reference.fa \
     -b sample.sorted.bam \
     --min-mapping-quality 20 \
     --min-base-quality 20 \
     > variants.vcf

For multi-sample calling, supply multiple BAM files or a BAM list:

.. code-block:: bash

   freebayes -f reference.fa \
     -L bam_list.txt \
     --min-mapping-quality 20 \
     --min-base-quality 20 \
     > cohort_variants.vcf

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``-f``
     - Path to the reference FASTA file (must be indexed with ``.fai``).
   * - ``-b``
     - Input BAM file (sorted and indexed).
   * - ``-L``
     - File containing a list of BAM paths, one per line.
   * - ``--min-mapping-quality``
     - Exclude alignments with mapping quality below this threshold.
   * - ``--min-base-quality``
     - Exclude alleles supported by bases with quality below this threshold.
   * - ``--min-alternate-count``
     - Require at least this many observations of an alternate allele.
   * - ``--min-alternate-fraction``
     - Require the alternate allele to comprise at least this fraction of
       observations.
   * - ``--ploidy``
     - Assumed ploidy of the sample (default 2).
   * - ``--targets``
     - BED file restricting variant calling to specified regions.
   * - ``--gvcf``
     - Emit a gVCF with reference confidence records.

Expected Output
---------------

* ``variants.vcf`` -- a standard VCF file containing all called variants with
  genotype fields (GT, DP, AO, RO, QA, GL), quality scores, and INFO
  annotations describing allele observations, mapping qualities, and strand
  bias metrics.

The output can be compressed and indexed for downstream use:

.. code-block:: bash

   bgzip variants.vcf
   tabix -p vcf variants.vcf.gz

See Also
--------

* :doc:`gatk` -- GATK HaplotypeCaller with GVCF joint-genotyping workflow for
  large cohorts
* :doc:`deepvariant` -- deep-learning variant caller from Google
* :doc:`/tools/variant-processing/bcftools` -- filter and manipulate VCF
  output from FreeBayes
* :doc:`/tools/variant-annotation/vep` -- annotate called variants with
  functional consequences
