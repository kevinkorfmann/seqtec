Scanpy
======

Overview
--------

Scanpy is a scalable Python framework for analysing single-cell gene expression
data, developed at the Theis Lab. It provides a complete workflow covering
quality control, normalisation, highly variable gene selection, dimensionality
reduction (PCA, UMAP, t-SNE), graph-based clustering (Leiden, Louvain),
differential expression, and trajectory inference. Scanpy stores all data in
the AnnData format, which efficiently handles large datasets and integrates
tightly with the broader scverse ecosystem including scvi-tools, squidpy, and
muon.

Installation
------------

.. code-block:: bash

   pip install scanpy

For Leiden clustering support (recommended):

.. code-block:: bash

   pip install scanpy leidenalg

Basic Usage
-----------

Load a 10x Cell Ranger output matrix, filter low-quality cells, and run the
standard processing and clustering pipeline.

.. code-block:: python

   import scanpy as sc

   adata = sc.read_10x_mtx("filtered_feature_bc_matrix/")

   # QC
   sc.pp.filter_cells(adata, min_genes=200)
   sc.pp.filter_genes(adata, min_cells=3)
   adata.var["mt"] = adata.var_names.str.startswith("MT-")
   sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)
   adata = adata[adata.obs.pct_counts_mt < 20].copy()

   # Processing
   sc.pp.normalize_total(adata, target_sum=1e4)
   sc.pp.log1p(adata)
   sc.pp.highly_variable_genes(adata, n_top_genes=2000)
   sc.tl.pca(adata)
   sc.pp.neighbors(adata, n_pcs=20)
   sc.tl.umap(adata)
   sc.tl.leiden(adata, resolution=0.5)

   sc.pl.umap(adata, color="leiden")
   adata.write("processed.h5ad")

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Function / parameter
     - Description
   * - ``sc.pp.filter_cells(min_genes)``
     - Remove cells with fewer than the specified number of detected genes.
   * - ``sc.pp.filter_genes(min_cells)``
     - Remove genes detected in fewer than the specified number of cells.
   * - ``sc.pp.calculate_qc_metrics``
     - Compute per-cell and per-gene quality metrics (total counts, gene
       counts, mitochondrial fraction).
   * - ``sc.pp.normalize_total(target_sum)``
     - Normalise each cell so total counts equal ``target_sum`` (typically
       10,000).
   * - ``sc.pp.log1p``
     - Apply log1p (natural logarithm of 1 + x) transformation.
   * - ``sc.pp.highly_variable_genes(n_top_genes)``
     - Select the top N highly variable genes for downstream analysis.
   * - ``sc.tl.pca``
     - Perform PCA; by default uses the highly variable genes.
   * - ``sc.pp.neighbors(n_pcs)``
     - Build a k-nearest-neighbours graph using the specified number of
       principal components.
   * - ``sc.tl.leiden(resolution)``
     - Cluster cells using the Leiden algorithm. Higher resolution yields more
       clusters.
   * - ``sc.tl.umap``
     - Compute a UMAP embedding for visualisation.

Expected Output
---------------

The processing pipeline produces an ``AnnData`` object (saved as
``processed.h5ad``) containing:

* ``adata.X`` -- normalised and log-transformed expression matrix.
* ``adata.raw`` -- a snapshot of the data before filtering on highly variable
  genes (if ``adata.raw`` is set).
* ``adata.obs["leiden"]`` -- cluster assignments for every cell.
* ``adata.obsm["X_pca"]`` -- PCA coordinates.
* ``adata.obsm["X_umap"]`` -- UMAP coordinates.
* ``adata.var["highly_variable"]`` -- boolean mask marking selected genes.

The ``sc.pl.umap()`` call produces a UMAP scatter plot coloured by Leiden
cluster identity. Plots can be saved to files with the ``save`` parameter
(e.g., ``sc.pl.umap(adata, color="leiden", save="_clusters.png")``).

See Also
--------

* :doc:`seurat` -- R equivalent for single-cell analysis with a similar
  workflow
* :doc:`cellranger` -- upstream pipeline that generates count matrices loaded
  by Scanpy
* :doc:`starsolo` -- open-source alternative for generating count matrices
