SnpEff
======

Overview
--------

SnpEff is a fast variant annotation and functional effect prediction tool that
classifies genetic variants by their impact on known genes and proteins. Given a
VCF file and a genome database, SnpEff reports the affected gene, transcript,
exon or intron location, amino acid change, and predicted impact category (HIGH,
MODERATE, LOW, or MODIFIER) for each variant. It bundles pre-built annotation
databases for thousands of genomes and can annotate a whole-genome VCF in
minutes. SnpEff is often used together with SnpSift, which provides utilities
for filtering and extracting fields from annotated VCFs.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda snpsift

This installs both SnpEff and SnpSift.

Basic Usage
-----------

**Download the annotation database**

.. code-block:: bash

   snpEff download GRCh38.105

**Annotate variants**

.. code-block:: bash

   snpEff ann GRCh38.105 variants.vcf.gz > annotated.vcf

The annotation is added to the INFO field of each VCF record as an ``ANN``
tag containing pipe-delimited fields for allele, effect, impact, gene name,
gene ID, feature type, transcript ID, biotype, and HGVS notation.

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``ann``
     - Annotate variants (primary sub-command).
   * - ``download``
     - Download a pre-built annotation database by name.
   * - ``-v``
     - Verbose output for logging and debugging.
   * - ``-canon``
     - Report annotations only for canonical transcripts.
   * - ``-noStats``
     - Skip generation of the HTML summary statistics file.
   * - ``-csvStats``
     - Write statistics in CSV format instead of HTML.
   * - ``-no-downstream``
     - Do not annotate downstream gene variants.
   * - ``-no-upstream``
     - Do not annotate upstream gene variants.
   * - ``-no-intergenic``
     - Do not annotate intergenic variants.
   * - ``-dataDir``
     - Path to the directory containing SnpEff databases.

Expected Output
---------------

* Standard output -- an annotated VCF with ``ANN`` fields in the INFO column
  describing the predicted effect of each variant on overlapping genes and
  transcripts. Each annotation includes: allele, annotation type (e.g.
  missense_variant, stop_gained), putative impact (HIGH/MODERATE/LOW/MODIFIER),
  gene name, gene ID, feature type, feature ID, transcript biotype, rank,
  HGVS.c, HGVS.p, cDNA position, CDS position, and protein position.
* ``snpEff_genes.txt`` -- a tab-delimited gene-level summary listing the
  number and types of variants affecting each gene.
* ``snpEff_summary.html`` -- an HTML report with variant type distributions,
  impact counts, and quality summaries.

See Also
--------

* :doc:`vep` -- Ensembl Variant Effect Predictor with extensive plugin support
  and population frequency annotations
* :doc:`/tools/variant-processing/bcftools` -- filter annotated VCFs by impact
  or annotation fields using SnpSift or bcftools query
* :doc:`/tools/variant-calling/gatk` -- upstream variant calling with GATK
  HaplotypeCaller
