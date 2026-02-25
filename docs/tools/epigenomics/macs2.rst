MACS2
=====

Overview
--------

MACS2 (Model-based Analysis of ChIP-Seq) is the standard peak caller for
ChIP-seq and ATAC-seq experiments. It identifies regions of the genome where
sequencing reads are significantly enriched compared to background, modelling
the shift between forward and reverse strand reads to improve spatial
resolution. MACS2 supports both narrow peak calling (e.g., transcription factor
binding sites, ATAC-seq open chromatin) and broad peak calling (e.g., histone
modifications like H3K27me3 or H3K36me3). It uses a dynamic Poisson
distribution to capture local biases in the genome and reports peaks with
associated p-values and q-values.

Installation
------------

.. code-block:: bash

   mamba install -c bioconda macs2

Basic Usage
-----------

**ATAC-seq peak calling**

For ATAC-seq data, use ``--nomodel`` with ``--shift`` and ``--extsize`` to
centre reads on the Tn5 cut site.

.. code-block:: bash

   macs2 callpeak -t sample.filtered.bam \
     -f BAMPE -g hs \
     --nomodel --shift -100 --extsize 200 \
     -n sample --outdir macs2_output/ \
     -q 0.01

**ChIP-seq peak calling with input control**

.. code-block:: bash

   macs2 callpeak -t treatment.bam -c input.bam \
     -f BAMPE -g hs \
     -n chip_sample --outdir macs2_output/ \
     -q 0.05

**Broad peak calling (e.g., H3K27me3)**

.. code-block:: bash

   macs2 callpeak -t treatment.bam -c input.bam \
     -f BAMPE -g hs --broad \
     -n broad_sample --outdir macs2_output/

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-t``
     - Treatment (enriched) BAM file.
   * - ``-c``
     - Control (input) BAM file. Optional for ATAC-seq; recommended for
       ChIP-seq.
   * - ``-f``
     - Input format (``BAMPE`` for paired-end BAM, ``BAM`` for single-end).
       ``BAMPE`` uses actual fragment sizes from paired reads.
   * - ``-g``
     - Effective genome size (``hs`` for human, ``mm`` for mouse, or a numeric
       value).
   * - ``-n``
     - Name prefix for output files.
   * - ``--outdir``
     - Output directory for results.
   * - ``-q``
     - Minimum FDR (q-value) cutoff for peak detection (default: 0.05).
   * - ``--nomodel``
     - Do not build the shifting model; use ``--extsize`` instead. Required
       for ATAC-seq.
   * - ``--shift``
     - Shift read positions by this many bases (use ``-100`` with
       ``--extsize 200`` for ATAC-seq to centre on cut sites).
   * - ``--extsize``
     - Extend reads to this fragment size when ``--nomodel`` is set.
   * - ``--broad``
     - Call broad peaks (gapped peaks) instead of narrow peaks. Use for
       diffuse histone marks.

Expected Output
---------------

For narrow peak calling:

* ``sample_peaks.narrowPeak`` -- BED6+4 format file listing each peak with
  chromosome, start, end, name, score, strand, signal value, p-value, q-value,
  and summit offset.
* ``sample_summits.bed`` -- BED file with the single-base-pair summit position
  of each peak.
* ``sample_peaks.xls`` -- tab-delimited spreadsheet with detailed peak
  statistics.
* ``sample_treat_pileup.bdg`` -- treatment pileup signal in bedGraph format.
* ``sample_control_lambda.bdg`` -- local background lambda in bedGraph format.

For broad peak calling, ``sample_peaks.broadPeak`` and
``sample_peaks.gappedPeak`` replace the narrowPeak output.

See Also
--------

* :doc:`bismark` -- bisulfite sequencing alignment and methylation calling for
  epigenomic analysis
* :doc:`/tools/sam-bam-processing/deeptools` -- signal track generation and
  visualisation of ChIP-seq and ATAC-seq data
* :doc:`/tools/interval-operations/bedtools` -- manipulate peak BED files
  (intersect, merge, closest)
