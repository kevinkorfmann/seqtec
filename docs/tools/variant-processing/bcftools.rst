BCFtools
========

Overview
--------

BCFtools is a high-performance toolkit for manipulating variant calls stored in
VCF and BCF format. It provides sub-commands for filtering, merging, splitting,
subsetting, normalising, and computing statistics on variant files. BCFtools
uses streaming and indexing strategies that allow it to process large
whole-genome VCFs efficiently with low memory usage. It is the variant-file
counterpart to SAMtools and shares the same HTSlib backend for reading and
writing compressed, indexed genomic data files.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda bcftools

Basic Usage
-----------

**Quality filtering**

Apply minimum quality and depth filters to a VCF file.

.. code-block:: bash

   bcftools filter -i 'QUAL>=20 && INFO/DP>=10' \
     clair3_output/merge_output.vcf.gz \
     -Oz -o filtered.vcf.gz

**Separate SNPs and indels**

.. code-block:: bash

   bcftools view -v snps filtered.vcf.gz -Oz -o snps.vcf.gz
   bcftools view -v indels filtered.vcf.gz -Oz -o indels.vcf.gz

**Generate statistics**

.. code-block:: bash

   bcftools stats filtered.vcf.gz > variant_stats.txt
   bcftools stats snps.vcf.gz > snp_stats.txt

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``filter -i EXPR``
     - Include only records matching the expression (e.g.
       ``'QUAL>=20 && INFO/DP>=10'``).
   * - ``filter -e EXPR``
     - Exclude records matching the expression.
   * - ``view -v TYPE``
     - Select variant types: ``snps``, ``indels``, ``mnps``, or ``other``.
   * - ``view -s SAMPLE``
     - Subset the VCF to specific samples.
   * - ``view -r REGION``
     - Restrict output to a genomic region (e.g. ``chr1:1000-2000``).
   * - ``-Oz``
     - Write output as bgzip-compressed VCF.
   * - ``-Ob``
     - Write output as BCF (binary VCF).
   * - ``-o FILE``
     - Output file path.
   * - ``stats``
     - Compute per-sample and per-site variant statistics.
   * - ``merge``
     - Merge multiple VCF/BCF files from non-overlapping sample sets.
   * - ``norm``
     - Left-align and normalise indels; split multi-allelic sites.
   * - ``query -f FORMAT``
     - Extract specific fields in a custom output format.

Expected Output
---------------

* ``filtered.vcf.gz`` -- a compressed VCF containing only variants that pass
  the specified filter criteria.
* ``snps.vcf.gz`` / ``indels.vcf.gz`` -- VCF files separated by variant type.
* ``variant_stats.txt`` -- a comprehensive text report including counts of
  SNPs, indels, MNPs, transitions/transversions ratio (Ts/Tv), per-sample
  statistics, indel length distributions, and quality score distributions.
  This file can be visualised with ``plot-vcfstats``:

.. code-block:: bash

   plot-vcfstats variant_stats.txt -p stats_plots/

See Also
--------

* :doc:`/tools/variant-calling/gatk` -- GATK variant calling and VQSR
  filtering upstream of BCFtools processing
* :doc:`/tools/variant-calling/clair3` -- long-read variant caller whose
  output can be filtered with BCFtools
* :doc:`/tools/variant-annotation/vep` -- annotate filtered variants with
  functional consequences
* :doc:`/tools/sam-bam-processing/samtools` -- companion toolkit for BAM/CRAM
  file manipulation
