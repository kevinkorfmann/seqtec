BigWig / bedGraph
=================

Overview
--------

BigWig and bedGraph are formats for storing **continuous numerical data**
across genomic coordinates. They are used to represent:

* **Read coverage** (depth of sequencing across the genome)
* **Signal tracks** (ChIP-seq enrichment, ATAC-seq accessibility)
* **Normalized scores** (RPKM, CPM, log2 fold-change)
* **Conservation scores** (phastCons, phyloP)
* **GC content** and other per-base statistics

These formats are essential for **genome browser visualisation** (IGV, UCSC
Genome Browser, JBrowse) and for computing signal matrices around genomic
features (e.g. heatmaps of ChIP-seq signal at promoters).

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Format
     - Extension
     - Description
   * - **bedGraph**
     - ``.bedGraph``, ``.bg``
     - Human-readable, tab-delimited text. Four columns: chrom, start, end,
       value. Uses 0-based, half-open coordinates (same as BED).
   * - **BigWig**
     - ``.bw``, ``.bigWig``
     - Compressed binary version of bedGraph. Indexed for fast random
       access. The preferred format for large datasets and genome browsers.

Structure
---------

bedGraph format
^^^^^^^^^^^^^^^

bedGraph is a simple four-column tab-delimited format:

.. code-block:: text

   chr1  0      1000   0.0
   chr1  1000   1050   3.5
   chr1  1050   1200   12.8
   chr1  1200   1350   8.2
   chr1  1350   2000   0.0

Each line defines a genomic interval and its associated value. Intervals
are non-overlapping and typically consecutive. Regions with a value of zero
may be omitted to save space.

.. list-table::
   :header-rows: 1
   :widths: 10 20 70

   * - Col
     - Field
     - Description
   * - 1
     - chrom
     - Chromosome name.
   * - 2
     - chromStart
     - Start position (0-based, inclusive).
   * - 3
     - chromEnd
     - End position (exclusive).
   * - 4
     - value
     - Signal value (integer or float).

BigWig format
^^^^^^^^^^^^^

BigWig is a binary, indexed format that stores the same data as bedGraph but
in a compressed R-tree structure. It cannot be read as plain text but
supports efficient random access for any genomic region. BigWig files are
typically 5--20x smaller than the equivalent bedGraph.

The internal structure consists of:

1. **Header** -- magic number, version, chromosome list.
2. **Zoom levels** -- pre-computed summaries at multiple resolutions for fast
   rendering at different scales.
3. **Data blocks** -- compressed intervals with values, organised in an
   R-tree index for fast regional queries.

Working With
------------

Generating coverage tracks from BAM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The most common way to create BigWig files is with ``bamCoverage`` from
**deepTools**:

.. code-block:: bash

   # Basic coverage track
   bamCoverage -b aligned.sorted.bam -o coverage.bw \
     --binSize 10 --normalizeUsing RPKM -p 8

   # CPM-normalised track (reads per million)
   bamCoverage -b aligned.sorted.bam -o coverage_cpm.bw \
     --binSize 10 --normalizeUsing CPM -p 8

   # Extend reads to estimated fragment size (ChIP-seq)
   bamCoverage -b chip.sorted.bam -o chip.bw \
     --binSize 10 --extendReads 200 --normalizeUsing RPKM -p 8

Comparing signal between samples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Log2 ratio of ChIP over Input
   bamCompare -b1 chip.sorted.bam -b2 input.sorted.bam \
     -o log2ratio.bw --binSize 50 -p 8

   # Subtract input from ChIP
   bamCompare -b1 chip.sorted.bam -b2 input.sorted.bam \
     -o subtracted.bw --ratio subtract --binSize 50 -p 8

Computing signal matrices and heatmaps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Compute matrix of signal around TSS
   computeMatrix reference-point \
     -S chip.bw input.bw \
     -R genes.bed \
     --referencePoint TSS \
     -a 3000 -b 3000 \
     -o matrix.gz -p 8

   # Plot as a heatmap
   plotHeatmap -m matrix.gz -o heatmap.png \
     --colorMap RdBu_r --whatToShow 'heatmap and colorbar'

   # Plot as a profile
   plotProfile -m matrix.gz -o profile.png

Converting between formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # bedGraph to BigWig (requires chromosome sizes file)
   bedGraphToBigWig coverage.bedGraph chrom.sizes coverage.bw

   # BigWig to bedGraph
   bigWigToBedGraph coverage.bw coverage.bedGraph

   # Generate chrom.sizes from a FASTA index
   cut -f1,2 reference.fa.fai > chrom.sizes

Generating bedGraph from BAM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Genome-wide coverage as bedGraph
   bedtools genomecov -ibam aligned.sorted.bam -bg > coverage.bedGraph

   # Sort the bedGraph (required before conversion to BigWig)
   sort -k1,1 -k2,2n coverage.bedGraph > coverage.sorted.bedGraph

Extracting values from BigWig
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Extract signal values for specific regions
   bigWigAverageOverBed coverage.bw regions.bed output.tab

   # Get signal summary (mean, min, max) for a region
   bigWigSummary coverage.bw chr1 10000 20000 10

Viewing in genome browsers
^^^^^^^^^^^^^^^^^^^^^^^^^^^

BigWig files can be loaded directly into:

* **IGV** -- drag and drop the ``.bw`` file or use ``File > Load from File``.
* **UCSC Genome Browser** -- host the file on a web server and add a custom
  track line.
* **JBrowse** -- add as a BigWig track in the configuration.

See Also
--------

* :doc:`/tools/sam-bam-processing/deeptools` -- ``bamCoverage``,
  ``bamCompare``, ``computeMatrix``, and ``plotHeatmap``
* :doc:`/tools/epigenomics/macs2` -- peak caller that produces bedGraph
  signal tracks
* :doc:`/tools/visualization/igv` -- genome browser for viewing BigWig files
* :doc:`bed` -- the interval format that bedGraph extends
* :doc:`sam-bam-cram` -- the alignment format from which coverage is computed
