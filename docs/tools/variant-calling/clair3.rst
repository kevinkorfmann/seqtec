Clair3
======

Overview
--------

Clair3 is a deep-learning-based variant caller designed specifically for
long-read sequencing data from Oxford Nanopore Technologies (ONT) and PacBio
platforms. It uses a pileup-based neural network followed by a full-alignment
model to call germline SNPs and indels with high accuracy. Clair3 ships with
pre-trained models for various sequencing platforms and chemistries, making it
straightforward to deploy on both Nanopore simplex and duplex data as well as
PacBio HiFi reads. It supports multi-threaded execution and can process
whole-genome datasets efficiently.

Installation
------------

.. code-block:: bash

   mamba create -n clair3 -c bioconda clair3

Activate the environment before running:

.. code-block:: bash

   conda activate clair3

Basic Usage
-----------

Call variants from ONT reads aligned to a reference genome.

.. code-block:: bash

   run_clair3.sh \
     --bam_fn=aligned.sorted.bam \
     --ref_fn=reference.fna \
     --output=clair3_output/ \
     --threads=8 \
     --platform="ont" \
     --model_path="${CONDA_PREFIX}/bin/models/ont" \
     --sample_name=sample1 \
     --include_all_ctgs

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``--bam_fn``
     - Path to the sorted and indexed BAM file.
   * - ``--ref_fn``
     - Path to the reference FASTA file (must be indexed).
   * - ``--output``
     - Output directory for variant calls and intermediate files.
   * - ``--threads``
     - Number of CPU threads to use.
   * - ``--platform``
     - Sequencing platform: ``ont`` for Oxford Nanopore, ``hifi`` for PacBio
       HiFi, or ``ilmn`` for Illumina.
   * - ``--model_path``
     - Path to the pre-trained model directory matching the sequencing
       platform and chemistry.
   * - ``--sample_name``
     - Sample name to embed in the VCF header.
   * - ``--include_all_ctgs``
     - Call variants on all contigs, not just those matching ``chr`` naming
       conventions.
   * - ``--bed_fn``
     - Restrict variant calling to regions defined in a BED file.
   * - ``--qual``
     - Minimum variant quality score threshold (default 2).

Expected Output
---------------

Clair3 writes its results to the specified output directory:

* ``merge_output.vcf.gz`` -- the final merged VCF containing all called SNPs
  and indels with quality scores and genotype information.
* ``merge_output.vcf.gz.tbi`` -- tabix index for the merged VCF.
* ``pileup.vcf.gz`` -- intermediate pileup model calls before full-alignment
  refinement.
* ``full_alignment.vcf.gz`` -- calls from the full-alignment model for
  candidate variants.
* ``log/`` -- directory containing run logs and timing information.

See Also
--------

* :doc:`gatk` -- GATK HaplotypeCaller for short-read germline variant calling
* :doc:`deepvariant` -- another deep-learning variant caller supporting
  multiple sequencing platforms
* :doc:`/tools/variant-processing/bcftools` -- filter and process the VCF
  output from Clair3
