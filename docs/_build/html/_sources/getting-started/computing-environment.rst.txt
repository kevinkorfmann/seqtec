Computing Environment
=====================

Overview
--------

Most bioinformatics work runs on Linux, either on a local workstation or a
shared High-Performance Computing (HPC) cluster. This page covers the
essential Linux commands you will use daily when processing sequencing data and
shows how to submit jobs with the SLURM workload manager.

Installation
------------

No additional installation is needed -- the commands below use standard
Linux utilities together with bioinformatics tools installed through Conda
(see :doc:`installation`).

Basic Usage
-----------

Essential Linux one-liners
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Count reads in a FASTQ file (4 lines per read)
   wc -l sample.fastq | awk '{print $1/4}'

   # Extract chromosome 1 alignments from a BAM file
   samtools view -b input.bam chr1 > chr1.bam

   # Sort a BED file and merge overlapping intervals
   sort -k1,1 -k2,2n peaks.bed | bedtools merge > merged.bed

   # View the first few records of a gzipped VCF
   zcat variants.vcf.gz | grep -v "^#" | head -20

   # Monitor disk usage of a project directory
   du -sh /data/project/*

Submitting a SLURM job
^^^^^^^^^^^^^^^^^^^^^^^

Write a SLURM batch script to run a BWA-MEM2 alignment on a cluster.

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=bwa_align
   #SBATCH --output=logs/bwa_%j.out
   #SBATCH --error=logs/bwa_%j.err
   #SBATCH --cpus-per-task=16
   #SBATCH --mem=32G
   #SBATCH --time=06:00:00
   #SBATCH --partition=standard

   source activate wgs_pipeline

   bwa-mem2 mem -t 16 \
     /ref/GRCh38.fa \
     sample_R1.fastq.gz sample_R2.fastq.gz \
     | samtools sort -@ 4 -o sample.sorted.bam -

   samtools index sample.sorted.bam

Save this as ``align.sh`` and submit it:

.. code-block:: bash

   sbatch align.sh

Key Parameters
--------------

SLURM directives
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Directive
     - Description
   * - ``--job-name``
     - Human-readable name shown by ``squeue``.
   * - ``--cpus-per-task``
     - Number of CPU cores allocated to the job.
   * - ``--mem``
     - Total memory for the job (e.g. ``32G``).
   * - ``--time``
     - Maximum wall-clock time (``HH:MM:SS``).
   * - ``--partition``
     - Cluster partition / queue to submit to.
   * - ``--output`` / ``--error``
     - Paths for stdout / stderr logs (``%j`` expands to the job ID).

Useful SLURM commands
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Command
     - Description
   * - ``sbatch script.sh``
     - Submit a batch job.
   * - ``squeue -u $USER``
     - List your running and pending jobs.
   * - ``scancel <job_id>``
     - Cancel a job.
   * - ``sacct -j <job_id> --format=Elapsed,MaxRSS``
     - Check elapsed time and peak memory after a job finishes.

Expected Output
---------------

After ``sbatch align.sh`` succeeds you will find:

* ``logs/bwa_<jobid>.out`` -- stdout from BWA-MEM2 and samtools.
* ``logs/bwa_<jobid>.err`` -- stderr, including timing information.
* ``sample.sorted.bam`` -- coordinate-sorted BAM file.
* ``sample.sorted.bam.bai`` -- BAM index.

See Also
--------

* :doc:`installation` -- install Miniforge and create Conda environments
* :doc:`test-datasets` -- download test data to run on your cluster
* :doc:`../infrastructure/singularity-apptainer` -- run containers on HPC
  systems where Docker is not available
