BRAKER
======

Overview
--------

BRAKER is a gene prediction pipeline for eukaryotic genomes that combines
GeneMark-ES/ET/EP with AUGUSTUS to produce accurate gene structure annotations.
It can use RNA-seq alignments, protein homology evidence, or both to train and
refine ab initio gene models. BRAKER automates the training of species-specific
parameters for AUGUSTUS, making it accessible for newly sequenced organisms
without existing gene models. It is one of the most widely used tools for
eukaryotic genome annotation and handles intron-exon boundary prediction,
alternative splicing hints, and UTR annotation.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda braker3

Basic Usage
-----------

Run BRAKER with RNA-seq evidence provided as a BAM alignment file.

.. code-block:: bash

   # BRAKER with RNA-seq evidence
   braker.pl --genome=genome.fasta \
     --bam=rnaseq_aligned.bam \
     --species=myspecies \
     --softmasking \
     --cores 8

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag / option
     - Description
   * - ``--genome``
     - Input genome assembly in FASTA format.
   * - ``--bam``
     - RNA-seq reads aligned to the genome in BAM format (for
       evidence-based training).
   * - ``--prot_seq``
     - Protein sequences in FASTA format for homology-based gene finding.
   * - ``--species``
     - Species name used for AUGUSTUS parameter training and storage.
   * - ``--softmasking``
     - Indicate that the genome has been soft-masked (lowercase letters for
       repeats). BRAKER will respect the masking during gene prediction.
   * - ``--cores``
     - Number of CPU threads to use.
   * - ``--gff3``
     - Output gene predictions in GFF3 format (default is GTF).
   * - ``--UTR``
     - Enable UTR prediction (requires RNA-seq evidence).
   * - ``--fungus``
     - Use fungal-specific parameters for GeneMark and AUGUSTUS.
   * - ``--AUGUSTUS_ab_initio``
     - Also produce ab initio predictions (without evidence support) in
       addition to the evidence-based predictions.

Expected Output
---------------

BRAKER writes output to the ``braker/`` directory (or the directory specified
with ``--workingdir``):

* ``braker.gtf`` -- the final gene predictions in GTF format, containing
  gene, transcript, exon, CDS, and optionally UTR features.
* ``braker.gff3`` -- gene predictions in GFF3 format (when ``--gff3`` is
  used).
* ``braker.aa`` -- predicted protein sequences in FASTA format.
* ``braker.codingseq`` -- coding nucleotide sequences in FASTA format.
* ``hintsfile.gff`` -- the compiled hints file used by AUGUSTUS, derived from
  RNA-seq and/or protein evidence.
* ``augustus.hints.gtf`` -- AUGUSTUS predictions using the trained parameters
  and external hints.

See Also
--------

* :doc:`prokka` -- annotation tool for prokaryotic genomes (bacteria and
  archaea)
* :doc:`bakta` -- alternative prokaryotic annotator with comprehensive
  database support
* :doc:`/tools/assembly-qc/busco` -- evaluate annotation completeness using
  conserved gene sets
