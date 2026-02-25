h5ad / AnnData
==============

Overview
--------

The **h5ad** format is an HDF5-based file format designed for storing
annotated data matrices, particularly **single-cell RNA-seq** (scRNA-seq) and
other single-cell omics data. It is the native file format of the
`AnnData <https://anndata.readthedocs.io/>`_ Python library, which is the
core data structure for the **Scanpy** ecosystem -- the most widely used
Python framework for single-cell analysis.

h5ad files store not just the count matrix, but all associated metadata,
dimensionality reductions, clustering results, and analysis outputs in a
single, self-contained file. A typical scRNA-seq experiment with 10 000
cells and 30 000 genes produces an h5ad file of approximately 200--500 MB.

The format is used in virtually every step of single-cell analysis: from
loading raw counts through quality control, normalisation, dimensionality
reduction, clustering, differential expression, and trajectory inference.

Structure
---------

An AnnData object (and its h5ad file on disk) has a well-defined structure
with several interconnected components:

.. code-block:: text

   AnnData object
   +-- .X             # Main data matrix (cells x genes)
   +-- .obs           # Observation (cell) metadata  [DataFrame]
   +-- .var           # Variable (gene) metadata      [DataFrame]
   +-- .uns           # Unstructured annotations       [dict]
   +-- .obsm          # Observation matrices           [dict of arrays]
   +-- .varm          # Variable matrices              [dict of arrays]
   +-- .obsp          # Observation pairwise           [dict of sparse matrices]
   +-- .layers        # Alternative matrix layers      [dict of matrices]
   +-- .raw           # Raw (unprocessed) data         [AnnData]

Components
^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 15 20 65

   * - Attribute
     - Shape / type
     - Description
   * - ``.X``
     - ``(n_obs, n_vars)``
     - The main data matrix. Typically raw counts or normalised expression
       values. Can be dense (NumPy array) or sparse (scipy CSR/CSC matrix).
   * - ``.obs``
     - ``(n_obs,)`` DataFrame
     - Cell-level metadata: barcodes, sample IDs, cluster labels, QC
       metrics (``n_genes``, ``total_counts``, ``pct_mito``), cell-type
       annotations.
   * - ``.var``
     - ``(n_vars,)`` DataFrame
     - Gene-level metadata: gene symbols, Ensembl IDs, ``highly_variable``
       flags, mean expression, dispersion.
   * - ``.uns``
     - dict
     - Unstructured data: colour palettes, UMAP parameters, marker gene
       rankings, analysis logs, sample-level information.
   * - ``.obsm``
     - dict of arrays
     - Cell embeddings: ``X_pca``, ``X_umap``, ``X_tsne``,
       ``X_diffmap``. Each array has shape ``(n_obs, n_components)``.
   * - ``.varm``
     - dict of arrays
     - Gene-level embeddings: PCA loadings (``PCs``).
   * - ``.obsp``
     - dict of sparse matrices
     - Cell-cell pairwise data: ``connectivities`` and ``distances``
       graphs used for clustering (Leiden, Louvain).
   * - ``.layers``
     - dict of matrices
     - Alternative representations of ``.X``: ``counts`` (raw),
       ``log1p`` (log-normalised), ``spliced``, ``unspliced`` (RNA
       velocity).
   * - ``.raw``
     - AnnData
     - Snapshot of the data before gene filtering, used for differential
       expression on the full gene set.

HDF5 on-disk layout
^^^^^^^^^^^^^^^^^^^^

The h5ad file maps directly to HDF5 groups and datasets:

.. code-block:: text

   /                          # Root
   /X                         # Main matrix (dense or sparse)
   /obs                       # Cell metadata (stored as HDF5 group with columns)
   /var                       # Gene metadata
   /uns                       # Nested dictionaries
   /obsm/X_pca                # PCA embedding
   /obsm/X_umap               # UMAP embedding
   /obsp/connectivities       # Neighbour graph
   /obsp/distances            # Distance matrix
   /layers/counts             # Raw count layer
   /raw                       # Pre-filtering snapshot

Sparse matrices are stored in CSR or CSC format with ``data``, ``indices``,
and ``indptr`` datasets.

Working With
------------

Reading and writing h5ad files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python3 -c "
   import scanpy as sc

   # Read an h5ad file
   adata = sc.read_h5ad('pbmc3k.h5ad')

   # Inspect the object
   print(adata)
   print(adata.obs.head())
   print(adata.var.head())

   # Write to h5ad
   adata.write('pbmc3k_processed.h5ad')

   # Write with compression
   adata.write('pbmc3k_compressed.h5ad', compression='gzip')
   "

Basic single-cell workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python3 -c "
   import scanpy as sc

   adata = sc.read_h5ad('raw_counts.h5ad')

   # Quality control
   sc.pp.filter_cells(adata, min_genes=200)
   sc.pp.filter_genes(adata, min_cells=3)
   adata.var['mt'] = adata.var_names.str.startswith('MT-')
   sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], inplace=True)
   adata = adata[adata.obs.pct_counts_mt < 20, :]

   # Normalise and log-transform
   adata.layers['counts'] = adata.X.copy()
   sc.pp.normalize_total(adata, target_sum=1e4)
   sc.pp.log1p(adata)

   # Feature selection and dimensionality reduction
   sc.pp.highly_variable_genes(adata, n_top_genes=2000)
   sc.pp.pca(adata, n_comps=50)
   sc.pp.neighbors(adata, n_pcs=30)
   sc.tl.umap(adata)
   sc.tl.leiden(adata, resolution=0.5)

   adata.write('processed.h5ad')
   print(adata)
   "

Inspecting h5ad from the command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Inspect HDF5 structure
   h5ls -r pbmc3k.h5ad

   # View file size and compression
   h5stat pbmc3k.h5ad

Converting from other formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python3 -c "
   import scanpy as sc

   # From 10x MEX format (Cell Ranger output)
   adata = sc.read_10x_mtx('filtered_feature_bc_matrix/')
   adata.write('from_10x.h5ad')

   # From 10x HDF5 format
   adata = sc.read_10x_h5('filtered_feature_bc_matrix.h5')
   adata.write('from_10x_h5.h5ad')

   # From CSV/TSV count matrix
   adata = sc.read_csv('counts.csv').T  # genes x cells -> cells x genes
   adata.write('from_csv.h5ad')
   "

Converting to/from Seurat (R)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Using the anndataR or SeuratDisk package in R
   Rscript -e '
   library(Seurat)
   library(SeuratDisk)

   # h5ad to h5Seurat to Seurat
   Convert("processed.h5ad", dest="h5seurat", overwrite=TRUE)
   seurat_obj <- LoadH5Seurat("processed.h5Seurat")
   '

Backed mode for large datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python3 -c "
   import anndata as ad

   # Open in backed mode (reads from disk on demand, low memory)
   adata = ad.read_h5ad('large_dataset.h5ad', backed='r')
   print(adata.obs.head())
   # Access a subset without loading the full matrix
   subset = adata[adata.obs['cell_type'] == 'T cell', :].to_memory()
   "

See Also
--------

* :doc:`/tools/single-cell/scanpy` -- the primary analysis framework for
  h5ad data
* :doc:`/tools/single-cell/cellranger` -- upstream tool that produces the
  raw count matrices
* :doc:`mex-10x` -- the sparse matrix format output by Cell Ranger (converted
  to h5ad for analysis)
* :doc:`/tools/single-cell/seurat` -- R-based single-cell analysis framework
  with interoperability via SeuratDisk
