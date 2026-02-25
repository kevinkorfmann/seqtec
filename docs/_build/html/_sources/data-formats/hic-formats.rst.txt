Hi-C Formats
============

Overview
--------

Hi-C experiments capture three-dimensional genome organization by measuring
physical proximity between genomic loci. The resulting contact matrices are
stored in specialized formats optimized for multi-resolution queries.

.hic Format
-----------

The ``.hic`` format (Juicer/Juicebox) stores contact matrices at multiple
resolutions in a single compressed file.

.. code-block:: bash

   # Create .hic file from valid pairs
   java -jar juicer_tools.jar pre \
     valid_pairs.txt output.hic hg38

   # Dump contacts at 10kb resolution
   java -jar juicer_tools.jar dump observed KR \
     output.hic chr1 chr1 BP 10000 chr1_contacts.txt

.cool / .mcool Format
---------------------

The ``.cool`` format (cooler) stores contact matrices in HDF5. Multi-resolution
``.mcool`` files contain matrices at several bin sizes.

.. code-block:: bash

   # Create .cool from pairs file
   cooler cload pairs -c1 2 -p1 3 -c2 4 -p2 5 \
     hg38.chrom.sizes:10000 pairs.txt output.cool

   # Generate multi-resolution .mcool
   cooler zoomify output.cool -o output.mcool

   # Balance (normalize) a cooler
   cooler balance output.cool

Working with Hi-C Data in Python
---------------------------------

.. code-block:: python

   import cooler

   clr = cooler.Cooler("output.mcool::resolutions/10000")
   matrix = clr.matrix(balance=True).fetch("chr1:0-5000000")
   print(matrix.shape)

Key Differences
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Feature
     - .hic
     - .cool / .mcool
   * - Library
     - Juicer Tools (Java)
     - cooler (Python)
   * - Storage
     - Custom binary
     - HDF5
   * - Multi-resolution
     - Built-in
     - .mcool container
   * - Normalization
     - KR, VC, VC_SQRT
     - ICE (iterative correction)

See Also
--------

- :doc:`bed` -- BED format for genomic intervals
- :doc:`bigwig-bedgraph` -- Coverage track formats
