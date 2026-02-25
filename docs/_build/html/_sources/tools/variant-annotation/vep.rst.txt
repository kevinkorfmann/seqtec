VEP (Variant Effect Predictor)
==============================

Overview
--------

The Ensembl Variant Effect Predictor (VEP) annotates genetic variants with
their predicted functional consequences on genes, transcripts, and protein
sequences. For each variant it reports the affected gene, transcript, protein
position, amino acid change, SIFT and PolyPhen pathogenicity predictions,
regulatory region overlaps, and allele frequencies from population databases.
VEP supports VCF input and can write annotated output in VCF, tab-delimited, or
JSON format. It uses a local cache for fast offline annotation and can be
extended with plugins for additional data sources such as CADD scores, dbNSFP,
and LOFTEE.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda ensembl-vep

After installation, download the annotation cache for your reference assembly:

.. code-block:: bash

   vep_install -a cf -s homo_sapiens -y GRCh38 -c /databases/vep/

Basic Usage
-----------

Annotate a filtered VCF with comprehensive functional annotations.

.. code-block:: bash

   vep --input_file filtered.vcf.gz \
     --output_file annotated.vcf.gz \
     --vcf --compress_output bgzip \
     --cache --dir_cache /databases/vep/ \
     --assembly GRCh38 \
     --everything \
     --fork 4

The ``--everything`` flag enables all available annotation fields including
SIFT, PolyPhen, allele frequencies, regulatory annotations, and more.

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``--input_file``
     - Path to the input VCF or variant file.
   * - ``--output_file``
     - Path for the annotated output file.
   * - ``--vcf``
     - Write output in VCF format (annotations added to the INFO field as
       CSQ).
   * - ``--compress_output bgzip``
     - Compress the output file with bgzip.
   * - ``--cache``
     - Use the local annotation cache instead of querying the Ensembl API.
   * - ``--dir_cache``
     - Path to the directory containing the VEP cache files.
   * - ``--assembly``
     - Genome assembly version (e.g. ``GRCh38`` or ``GRCh37``).
   * - ``--everything``
     - Enable all annotation fields: SIFT, PolyPhen, allele frequencies,
       regulatory features, and more.
   * - ``--fork``
     - Number of parallel forked processes for faster annotation.
   * - ``--pick``
     - Report only the most severe consequence per variant rather than all
       affected transcripts.
   * - ``--plugin``
     - Load a VEP plugin for additional annotations (e.g. CADD, LOFTEE).

Expected Output
---------------

* ``annotated.vcf.gz`` -- a VCF file with a ``CSQ`` field in the INFO column
  containing pipe-delimited annotation values for each variant-transcript
  pair. Annotations include: gene symbol, transcript ID, consequence type
  (e.g. missense_variant, synonymous_variant, frameshift_variant), protein
  position, amino acid change, SIFT score, PolyPhen score, and population
  allele frequencies.
* ``annotated.vcf.gz_summary.html`` -- an HTML summary report with variant
  class distributions, consequence type counts, and annotation statistics.

See Also
--------

* :doc:`snpeff` -- alternative variant annotation tool with built-in gene
  databases
* :doc:`/tools/variant-calling/gatk` -- GATK variant calling workflow that
  produces VCFs for annotation
* :doc:`/tools/variant-processing/bcftools` -- filter annotated VCFs by
  consequence or annotation fields
