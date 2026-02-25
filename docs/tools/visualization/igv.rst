IGV
===

Overview
--------

The Integrative Genomics Viewer (IGV) is a high-performance desktop
application for interactive visualisation of genomic data, developed by the
Broad Institute. It displays aligned reads (BAM/CRAM), variant calls (VCF),
signal tracks (bigWig, bedGraph), peak calls (BED, narrowPeak), and many other
genomic file formats against a reference genome. IGV is widely used for visual
inspection of alignments, variant validation, and generation of publication-
quality screenshots. It also supports a batch scripting interface for automated
visualisation of multiple genomic regions.

Installation
------------

Download from the `Broad Institute IGV page <https://igv.org/doc/desktop/>`_,
or install via Bioconda:

.. code-block:: bash

   mamba install -c bioconda igv

Basic Usage
-----------

**Prepare files for IGV**

BAM and VCF files must be sorted and indexed before loading into IGV.

.. code-block:: bash

   samtools sort aligned.bam -o aligned.sorted.bam
   samtools index aligned.sorted.bam
   bcftools sort variants.vcf.gz -Oz -o variants.sorted.vcf.gz
   bcftools index variants.sorted.vcf.gz

**Launch IGV**

.. code-block:: bash

   igv.sh

Load files through the GUI (File > Load from File) or by passing them as
command-line arguments.

**Batch scripting**

IGV supports batch scripts for automated screenshots and navigation. Save the
following as ``igv_batch.txt`` and run it with
``igv.sh -b igv_batch.txt``:

.. code-block:: bash

   new
   genome hg38
   load aligned.sorted.bam
   load variants.sorted.vcf.gz
   goto chr17:43044295-43125483
   snapshot brca1_region.png
   goto chr13:32315474-32400266
   snapshot brca2_region.png
   goto chr7:117559590-117711986
   snapshot cftr_region.png

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Flag / option
     - Description
   * - ``-b``
     - Run a batch script file for automated visualisation.
   * - ``-g``
     - Reference genome to load on startup (e.g., ``hg38``, ``mm10``).
   * - ``--igvDirectory``
     - Override the default IGV preferences directory.

**Batch script commands:**

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Command
     - Description
   * - ``new``
     - Reset the session, clearing all loaded tracks.
   * - ``genome``
     - Load a reference genome (e.g., ``hg38``).
   * - ``load``
     - Load a data file (BAM, VCF, BED, bigWig, etc.).
   * - ``goto``
     - Navigate to a genomic region (``chr:start-end``) or gene name.
   * - ``snapshot``
     - Save the current view as a PNG image.
   * - ``snapshotDirectory``
     - Set the output directory for snapshot images.
   * - ``sort``
     - Sort alignments (``base``, ``strand``, ``quality``,
       ``insertSize``).
   * - ``collapse`` / ``expand`` / ``squish``
     - Change track display mode.
   * - ``maxPanelHeight``
     - Set the maximum pixel height for alignment panels.
   * - ``exit``
     - Close IGV after batch processing.

Expected Output
---------------

**Interactive session:**

IGV displays aligned reads as coloured horizontal bars against the reference
genome. Variants are highlighted with colour-coded mismatches, insertions, and
deletions. Coverage tracks show read depth across each region.

**Batch script output:**

* ``brca1_region.png`` -- screenshot of the BRCA1 locus on chromosome 17.
* ``brca2_region.png`` -- screenshot of the BRCA2 locus on chromosome 13.
* ``cftr_region.png`` -- screenshot of the CFTR locus on chromosome 7.

Screenshots capture all loaded tracks at the specified genomic coordinates and
are saved in the current working directory (or the directory set by
``snapshotDirectory``).

See Also
--------

* :doc:`/tools/sam-bam-processing/samtools` -- sort and index BAM files before
  loading into IGV
* :doc:`/tools/variant-processing/bcftools` -- sort and index VCF files before
  loading into IGV
* :doc:`/tools/sam-bam-processing/deeptools` -- generate bigWig signal tracks
  for visualisation in IGV
