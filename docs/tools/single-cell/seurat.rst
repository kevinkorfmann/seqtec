Seurat
======

Overview
--------

Seurat is a comprehensive R toolkit for single-cell RNA-seq analysis, developed
by the Satija Lab at the New York Genome Center. It provides functions for
quality control filtering, normalisation, feature selection, dimensionality
reduction (PCA, UMAP, t-SNE), graph-based clustering, differential expression
testing, and multi-modal data integration. Seurat is one of the most widely
adopted frameworks in the single-cell community and supports a broad range of
assay types including scRNA-seq, CITE-seq, spatial transcriptomics, and
scATAC-seq.

Installation
------------

Install Seurat from CRAN within an R session:

.. code-block:: r

   install.packages("Seurat")

For the latest development version:

.. code-block:: r

   remotes::install_github("satijalab/seurat", ref = "develop")

Basic Usage
-----------

Load a 10x Cell Ranger output matrix, perform quality control filtering, and
run the standard clustering workflow.

.. code-block:: r

   library(Seurat)

   # Load 10x data
   data <- Read10X(data.dir = "filtered_feature_bc_matrix/")
   obj <- CreateSeuratObject(counts = data, min.cells = 3, min.features = 200)

   # QC and filtering
   obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = "^MT-")
   obj <- subset(obj, nFeature_RNA > 200 & nFeature_RNA < 5000 & percent.mt < 20)

   # Standard workflow
   obj <- NormalizeData(obj) |>
     FindVariableFeatures() |>
     ScaleData() |>
     RunPCA() |>
     FindNeighbors(dims = 1:20) |>
     FindClusters(resolution = 0.5) |>
     RunUMAP(dims = 1:20)

   DimPlot(obj, reduction = "umap", label = TRUE)

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Function / parameter
     - Description
   * - ``min.cells``
     - Minimum number of cells a gene must be detected in to be retained
       (passed to ``CreateSeuratObject``).
   * - ``min.features``
     - Minimum number of genes a cell must express to be retained.
   * - ``PercentageFeatureSet``
     - Calculates the percentage of counts from a gene set (e.g.,
       mitochondrial genes matching ``^MT-``).
   * - ``NormalizeData``
     - Log-normalises counts per cell (default: ``LogNormalize`` with a scale
       factor of 10,000).
   * - ``FindVariableFeatures``
     - Selects highly variable genes (default: top 2,000 by variance
       stabilising transformation).
   * - ``ScaleData``
     - Centres and scales expression values; optionally regresses out
       confounding variables.
   * - ``RunPCA``
     - Performs principal component analysis on the scaled variable features.
   * - ``FindNeighbors(dims = 1:20)``
     - Constructs a shared nearest-neighbour graph using the specified PCA
       dimensions.
   * - ``FindClusters(resolution)``
     - Identifies cell clusters using the Louvain or Leiden algorithm. Higher
       resolution produces more clusters.
   * - ``RunUMAP(dims = 1:20)``
     - Computes a UMAP embedding for visualisation using the specified PCA
       dimensions.

Expected Output
---------------

The standard workflow produces a Seurat object stored in memory with the
following key slots:

* ``obj[["RNA"]]@counts`` -- original count matrix.
* ``obj[["RNA"]]@data`` -- normalised expression values.
* ``obj[["RNA"]]@scale.data`` -- scaled expression matrix.
* ``obj@reductions$pca`` -- PCA coordinates.
* ``obj@reductions$umap`` -- UMAP coordinates.
* ``obj@meta.data$seurat_clusters`` -- cluster assignments for every cell.

Common output files written to disk:

* ``DimPlot()`` generates a UMAP scatter plot coloured by cluster identity.
* ``saveRDS(obj, "seurat_object.rds")`` saves the entire analysis for later
  reloading.

See Also
--------

* :doc:`scanpy` -- Python equivalent for single-cell analysis, producing
  comparable results
* :doc:`cellranger` -- upstream pipeline that generates the count matrices
  loaded by Seurat
* :doc:`starsolo` -- open-source alternative for generating count matrices
