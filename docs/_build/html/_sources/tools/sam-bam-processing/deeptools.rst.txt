deepTools
=========

Overview
--------

deepTools is a suite of Python-based tools for exploring deep-sequencing data.
It converts BAM files into normalised coverage tracks (bigWig), computes
sample-to-sample correlations, and generates publication-ready heatmaps and
profile plots of signal enrichment around genomic features. deepTools is widely
used in ChIP-seq, ATAC-seq, and RNA-seq workflows for visual quality control and
downstream analysis of read coverage.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda deeptools

Basic Usage
-----------

**Generate a normalised coverage track (RPKM)**

.. code-block:: bash

   bamCoverage -b sample.bam -o sample.bw \
     --normalizeUsing RPKM --binSize 10 -p 8

**Compute correlation between replicates**

.. code-block:: bash

   multiBamSummary bins -b rep1.bam rep2.bam rep3.bam \
     -o results.npz -p 8
   plotCorrelation -in results.npz --corMethod spearman \
     -o correlation_heatmap.pdf --plotFileFormat pdf

**Generate a heatmap of signal around TSS**

.. code-block:: bash

   computeMatrix reference-point -S chip.bw input.bw \
     -R genes.bed -a 3000 -b 3000 -o matrix.gz
   plotHeatmap -m matrix.gz -o heatmap.pdf

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-b``
     - Input BAM file(s).
   * - ``-o``
     - Output file (bigWig, matrix, or plot depending on the sub-command).
   * - ``-p THREADS``
     - Number of processors to use.
   * - ``--normalizeUsing``
     - Normalisation method for ``bamCoverage``: ``RPKM``, ``CPM``, ``BPM``,
       ``RPGC``, or ``None``.
   * - ``--binSize INT``
     - Length in bases of the output bins (default: 50).
   * - ``--effectiveGenomeSize INT``
     - Mappable genome size, required when using ``RPGC`` normalisation.
   * - ``-S``
     - Input bigWig score file(s) for ``computeMatrix``.
   * - ``-R``
     - BED or GTF file of regions for ``computeMatrix``.
   * - ``-a / -b``
     - Distance in bp downstream (``-a``) and upstream (``-b``) of the
       reference point in ``computeMatrix reference-point``.
   * - ``--corMethod``
     - Correlation method for ``plotCorrelation``: ``spearman`` or ``pearson``.

Expected Output
---------------

* ``bamCoverage`` -- a bigWig (``.bw``) file containing normalised per-bin
  coverage values, suitable for genome-browser visualisation.
* ``multiBamSummary`` -- a compressed NumPy archive (``.npz``) storing the
  read-count matrix across genomic bins for all input BAM files.
* ``plotCorrelation`` -- a PDF (or PNG/SVG) heatmap or scatterplot showing
  pairwise sample correlations.
* ``computeMatrix`` -- a gzipped matrix file used as input for
  ``plotHeatmap`` and ``plotProfile``.
* ``plotHeatmap`` -- a PDF (or PNG/SVG) heatmap of signal intensity around the
  specified genomic features.

See Also
--------

* :doc:`samtools` -- prerequisite for BAM indexing before running deepTools
* :doc:`/tools/interval-operations/bedtools` -- prepare BED region files used
  as input to ``computeMatrix``
* :doc:`/data-formats/sam-bam-cram` -- reference for the SAM/BAM/CRAM file
  formats
* :doc:`/data-formats/bigwig-bedgraph` -- reference for the bigWig and
  bedGraph coverage formats
* :doc:`/data-formats/bed` -- reference for the BED interval format
