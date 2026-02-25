DeepVariant
===========

Overview
--------

DeepVariant is a deep-learning variant caller developed by Google that
reimagines variant calling as an image classification problem. It converts read
pileups around candidate variant sites into tensor representations and uses a
convolutional neural network to classify each site as homozygous reference,
heterozygous, or homozygous alternate. DeepVariant supports whole-genome
sequencing (WGS), whole-exome sequencing (WES), and PacBio HiFi data through
dedicated model types. It consistently achieves top accuracy in benchmarking
studies such as the PrecisionFDA Truth Challenges and requires no manual tuning
of quality filters.

Installation
------------

DeepVariant is best run via its official Docker image, which bundles all
dependencies and pre-trained models:

.. code-block:: bash

   docker pull google/deepvariant:1.6.0

Alternatively, a Singularity/Apptainer image can be used on HPC systems where
Docker is not available.

Basic Usage
-----------

Run DeepVariant on whole-genome sequencing data using Docker.

.. code-block:: bash

   docker run -v $(pwd):/input -v $(pwd)/output:/output \
     google/deepvariant:1.6.0 \
     /opt/deepvariant/bin/run_deepvariant \
     --model_type=WGS \
     --ref=/input/reference.fa \
     --reads=/input/sample.sorted.bam \
     --output_vcf=/output/sample.vcf.gz \
     --num_shards=8

Ensure the reference FASTA has an accompanying ``.fai`` index and the BAM file
is sorted and indexed before running.

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``--model_type``
     - Sequencing type: ``WGS`` for whole-genome, ``WES`` for whole-exome,
       ``PACBIO`` for PacBio HiFi, or ``ONT_R104`` for Nanopore R10.4.
   * - ``--ref``
     - Path to the reference genome FASTA file.
   * - ``--reads``
     - Path to the sorted, indexed BAM or CRAM file.
   * - ``--output_vcf``
     - Path for the output VCF file.
   * - ``--output_gvcf``
     - Path for an optional gVCF output with reference confidence blocks.
   * - ``--num_shards``
     - Number of parallel shards for the make_examples step (controls
       parallelism).
   * - ``--regions``
     - Restrict calling to specific genomic regions (BED file or region
       string).
   * - ``--intermediate_results_dir``
     - Directory for intermediate files; useful for debugging or
       re-running individual stages.

Expected Output
---------------

* ``sample.vcf.gz`` -- a compressed VCF file containing SNP and indel calls
  with genotype quality (GQ), genotype likelihoods (GL/PL), and read depth
  (DP) annotations.
* ``sample.vcf.gz.tbi`` -- tabix index for the output VCF.
* ``sample.g.vcf.gz`` -- optional gVCF output (when ``--output_gvcf`` is
  specified) for downstream joint genotyping with GLnexus.
* ``sample.visual_report.html`` -- an HTML quality report summarising variant
  statistics and model confidence.

See Also
--------

* :doc:`gatk` -- GATK HaplotypeCaller for traditional short-read variant
  calling with VQSR filtering
* :doc:`clair3` -- deep-learning variant caller optimised for long-read ONT
  and PacBio data
* :doc:`freebayes` -- haplotype-based Bayesian caller with a simpler
  single-step workflow
* :doc:`/tools/variant-processing/bcftools` -- filter and process VCF output
