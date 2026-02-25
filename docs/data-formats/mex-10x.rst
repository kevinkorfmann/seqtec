MEX / 10x Format
================

Overview
--------

The MEX (Market Exchange) format is a sparse matrix representation used by
**10x Genomics Cell Ranger** and **STARsolo** to store single-cell gene
expression count data. Because scRNA-seq count matrices are extremely
sparse -- typically more than 90 % of entries are zero -- MEX stores only the
non-zero values, achieving dramatic space savings over dense formats.

The 10x MEX output consists of **three files** in a directory (commonly named
``filtered_feature_bc_matrix/`` or ``raw_feature_bc_matrix/``):

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - File
     - Contents
   * - ``matrix.mtx.gz``
     - Sparse count matrix in Matrix Market coordinate format.
   * - ``barcodes.tsv.gz``
     - Cell barcodes (one per line, corresponding to matrix columns).
   * - ``features.tsv.gz``
     - Gene/feature information (corresponding to matrix rows).

This three-file bundle is the primary interchange format between upstream
processing (Cell Ranger, STARsolo, Alevin, Kallisto-BUStools) and downstream
analysis frameworks (Scanpy, Seurat, Bioconductor/SingleCellExperiment).

Structure
---------

matrix.mtx
^^^^^^^^^^

The matrix file follows the `Matrix Market coordinate format
<https://math.nist.gov/MatrixMarket/formats.html>`_:

.. code-block:: text

   %%MatrixMarket matrix coordinate integer general
   %
   33538 7374 12890567
   1 1 3
   32 1 1
   51 1 5
   134 1 2
   245 2 1
   ...

* **Line 1** -- Header declaring the format (coordinate, integer, general).
* **Line 2** -- Optional comment lines starting with ``%``.
* **Line 3** -- Dimensions: ``n_features  n_barcodes  n_nonzero_entries``.
* **Remaining lines** -- One triplet per non-zero entry:
  ``feature_index  barcode_index  count``.

Indices are **1-based** (the first feature and first barcode are numbered 1).

barcodes.tsv
^^^^^^^^^^^^^

One cell barcode per line:

.. code-block:: text

   AAACCCAAGAAACACT-1
   AAACCCAAGAAACCAT-1
   AAACCCAAGAAACTGT-1
   AAACCCAAGAAAGCGA-1
   ...

The ``-1`` suffix is a GEM well identifier appended by Cell Ranger. The
number of lines equals the number of columns in the matrix.

features.tsv
^^^^^^^^^^^^^

Tab-separated file with gene/feature metadata:

.. code-block:: text

   ENSG00000243485  MIR1302-2HG  Gene Expression
   ENSG00000237613  FAM138A      Gene Expression
   ENSG00000186092  OR4F5        Gene Expression
   ENSG00000238009  AL627309.1   Gene Expression
   ...

Columns:

.. list-table::
   :header-rows: 1
   :widths: 10 25 65

   * - Col
     - Field
     - Description
   * - 1
     - Feature ID
     - Ensembl gene ID or feature identifier.
   * - 2
     - Feature name
     - Gene symbol or feature name.
   * - 3
     - Feature type
     - ``Gene Expression``, ``Antibody Capture`` (CITE-seq),
       ``CRISPR Guide Capture`` (Perturb-seq), ``Multiplexing Capture``
       (cell hashing), etc.

The number of lines equals the number of rows in the matrix.

Filtered vs raw matrices
^^^^^^^^^^^^^^^^^^^^^^^^^

Cell Ranger outputs **two** versions of the MEX directory:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Directory
     - Description
   * - ``raw_feature_bc_matrix/``
     - Contains **all** barcodes detected (including empty droplets). May
       have hundreds of thousands of columns.
   * - ``filtered_feature_bc_matrix/``
     - Contains only barcodes that Cell Ranger classified as real cells.
       This is the starting point for most analyses.

Working With
------------

Loading into Scanpy (Python)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python3 -c "
   import scanpy as sc

   # Load from the three-file MEX directory
   adata = sc.read_10x_mtx(
       'filtered_feature_bc_matrix/',
       var_names='gene_symbols',    # use gene symbols as variable names
       cache=True                    # cache for faster re-loading
   )
   print(adata)
   # AnnData object with n_obs x n_vars = 7374 x 33538

   # Save as h5ad for faster future access
   adata.write('counts.h5ad')
   "

Loading into Seurat (R)
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   Rscript -e '
   library(Seurat)

   # Load from the three-file MEX directory
   counts <- Read10X(data.dir = "filtered_feature_bc_matrix/")
   seurat_obj <- CreateSeuratObject(counts = counts, project = "my_project")
   print(seurat_obj)
   '

Loading into Bioconductor (R)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   Rscript -e '
   library(DropletUtils)

   # Load as SingleCellExperiment
   sce <- read10xCounts("filtered_feature_bc_matrix/")
   print(sce)
   '

Inspecting MEX files from the command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Count the number of barcodes (cells)
   zcat filtered_feature_bc_matrix/barcodes.tsv.gz | wc -l

   # Count the number of features (genes)
   zcat filtered_feature_bc_matrix/features.tsv.gz | wc -l

   # View the matrix header (dimensions and non-zero count)
   zcat filtered_feature_bc_matrix/matrix.mtx.gz | head -3

   # View the first few features
   zcat filtered_feature_bc_matrix/features.tsv.gz | head -5

Loading STARsolo output
^^^^^^^^^^^^^^^^^^^^^^^

STARsolo produces the same three-file format:

.. code-block:: bash

   python3 -c "
   import scanpy as sc

   # STARsolo output directory structure
   adata = sc.read_10x_mtx(
       'Solo.out/Gene/filtered/',
       var_names='gene_symbols'
   )
   adata.write('starsolo_counts.h5ad')
   "

Loading multi-modal data (CITE-seq)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When the features.tsv file contains multiple feature types (e.g. Gene
Expression and Antibody Capture), they must be separated:

.. code-block:: bash

   python3 -c "
   import scanpy as sc
   import muon as mu

   # Read as a MuData object (multi-modal)
   mdata = mu.read_10x_mtx('filtered_feature_bc_matrix/')
   print(mdata)
   # MuData object with 'rna' and 'prot' modalities
   "

See Also
--------

* :doc:`/tools/single-cell/cellranger` -- the upstream pipeline that produces
  MEX output
* :doc:`/tools/single-cell/starsolo` -- alternative single-cell aligner with
  MEX output
* :doc:`h5ad-anndata` -- the h5ad format that MEX data is typically converted
  into
* :doc:`/tools/single-cell/scanpy` -- Python framework for analysing
  single-cell data
