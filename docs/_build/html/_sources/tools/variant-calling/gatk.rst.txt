GATK
====

Overview
--------

The Genome Analysis Toolkit (GATK) is the industry-standard software suite for
variant discovery in high-throughput sequencing data, developed by the Broad
Institute. Its best-practices workflow centres on HaplotypeCaller for per-sample
variant calling in GVCF mode, followed by joint genotyping across a cohort with
GenotypeGVCFs. GATK provides Variant Quality Score Recalibration (VQSR) for
machine-learning-based filtering that leverages known variant resources such as
HapMap and dbSNP to separate true variants from artefacts. The toolkit handles
both SNPs and indels and integrates seamlessly with Picard for preprocessing
steps like duplicate marking and base quality score recalibration.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda gatk4

Basic Usage
-----------

**Step 1 -- Call variants per sample in GVCF mode**

.. code-block:: bash

   gatk HaplotypeCaller \
     -R reference.fa \
     -I sample.dedup.bam \
     -O sample.g.vcf.gz \
     -ERC GVCF

**Step 2 -- Combine GVCFs from multiple samples**

.. code-block:: bash

   gatk CombineGVCFs \
     -R reference.fa \
     -V sample1.g.vcf.gz -V sample2.g.vcf.gz \
     -O combined.g.vcf.gz

**Step 3 -- Joint genotyping**

.. code-block:: bash

   gatk GenotypeGVCFs \
     -R reference.fa \
     -V combined.g.vcf.gz \
     -O genotyped.vcf.gz

**Step 4 -- Variant Quality Score Recalibration (SNPs)**

.. code-block:: bash

   gatk VariantRecalibrator \
     -R reference.fa -V genotyped.vcf.gz \
     --resource:hapmap,known=false,training=true,truth=true,prior=15.0 hapmap.vcf.gz \
     --resource:dbsnp,known=true,training=false,truth=false,prior=2.0 dbsnp.vcf.gz \
     -an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR \
     -mode SNP -O snp_recal --tranches-file snp_tranches

**Step 5 -- Apply VQSR filtering**

.. code-block:: bash

   gatk ApplyVQSR \
     -R reference.fa -V genotyped.vcf.gz \
     --recal-file snp_recal --tranches-file snp_tranches \
     --truth-sensitivity-filter-level 99.5 -mode SNP \
     -O filtered.vcf.gz

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``-R``
     - Path to the reference genome FASTA (must be indexed with ``.fai`` and
       ``.dict`` files).
   * - ``-I``
     - Input BAM or CRAM file (should be sorted, indexed, and duplicate-marked).
   * - ``-O``
     - Output file path for variants.
   * - ``-ERC GVCF``
     - Emit a GVCF with per-site confidence for both variant and reference
       positions, enabling joint genotyping later.
   * - ``-V``
     - Input VCF or GVCF file(s); repeat for multiple samples.
   * - ``--resource``
     - Known variant resource with truth/training/prior annotations for VQSR.
   * - ``-an``
     - Annotation feature to use in the VQSR Gaussian model (e.g. ``QD``,
       ``MQ``, ``FS``).
   * - ``-mode``
     - Recalibration mode: ``SNP`` or ``INDEL``.
   * - ``--truth-sensitivity-filter-level``
     - Sensitivity threshold for the VQSR tranche filter (e.g. 99.5).

Expected Output
---------------

* ``sample.g.vcf.gz`` -- per-sample GVCF containing variant calls and
  reference confidence blocks.
* ``combined.g.vcf.gz`` -- multi-sample GVCF merging all individual GVCFs.
* ``genotyped.vcf.gz`` -- joint-genotyped VCF with genotype likelihoods for
  every sample at every variant site.
* ``snp_recal`` / ``snp_tranches`` -- VQSR model and tranche files used by
  ApplyVQSR.
* ``filtered.vcf.gz`` -- final VCF with VQSR filter annotations in the FILTER
  column (PASS or sensitivity tranche labels).

See Also
--------

* :doc:`freebayes` -- haplotype-based variant caller with a simpler single-step
  workflow
* :doc:`deepvariant` -- deep-learning variant caller from Google
* :doc:`/tools/variant-annotation/vep` -- annotate called variants with
  functional consequences
* :doc:`/tools/variant-processing/bcftools` -- filter and manipulate VCF files
  post-calling
