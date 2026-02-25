Medaka
======

Overview
--------

Medaka is a neural-network-based polishing tool from Oxford Nanopore
Technologies that improves the consensus accuracy of draft assemblies produced
from Nanopore reads. It aligns the original reads back to the draft assembly
and applies a recurrent neural network to predict a more accurate consensus
sequence. Medaka provides pre-trained models matched to specific basecalling
configurations (chemistry, pore type, and basecaller version), and its
``medaka_polisher`` pipeline wraps alignment, inference, and consensus
generation into a single command.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda medaka

Basic Usage
-----------

Polish a Flye assembly using the reads that produced it, selecting a model
that matches the basecalling configuration.

.. code-block:: bash

   medaka_polisher -i filtered_reads.fastq.gz \
     -d flye_output/assembly.fasta \
     -o medaka_output/ \
     -m r1041_e82_400bps_sup_v5.0.0 \
     --bacteria \
     --threads 8

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``-i``
     - Input reads in FASTQ or FASTA format (the same reads used for
       assembly).
   * - ``-d``
     - Draft assembly to be polished (FASTA format).
   * - ``-o``
     - Output directory for the polished consensus.
   * - ``-m``
     - Medaka model name matching the basecalling configuration (e.g.
       ``r1041_e82_400bps_sup_v5.0.0``). Use ``medaka --list_models``
       to see available models.
   * - ``--bacteria``
     - Apply settings optimised for bacterial genomes.
   * - ``--threads``
     - Number of CPU threads to use for alignment and inference.
   * - ``-b``
     - Inference batch size (higher values use more GPU memory but run
       faster).

Expected Output
---------------

Medaka writes its results to the specified output directory:

* ``consensus.fasta`` -- the polished consensus assembly in FASTA format.
  This is the primary output for downstream analysis.
* Intermediate BAM alignment files used during the polishing process.
* Log files with details of model inference and consensus calling.

The polished ``consensus.fasta`` typically shows measurable improvements in
identity when compared to a reference, particularly at homopolymer sites where
Nanopore reads are most error-prone.

See Also
--------

* :doc:`flye` -- long-read assembler commonly used upstream of Medaka
* :doc:`canu` -- alternative long-read assembler whose output can also be
  polished with Medaka
* :doc:`/tools/assembly-qc/quast` -- compare polished and unpolished
  assemblies against a reference
