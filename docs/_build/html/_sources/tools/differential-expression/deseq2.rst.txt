DESeq2
======

Overview
--------

DESeq2 is a widely used R/Bioconductor package for differential gene expression
analysis of RNA-seq count data. It uses a negative binomial generalised linear
model to estimate log-fold changes between experimental conditions and applies
shrinkage estimators for dispersion and fold-change to improve statistical power
and stability, especially for experiments with small sample sizes. DESeq2
handles normalisation internally using a median-of-ratios method that accounts
for differences in library size and RNA composition. It provides Wald tests and
likelihood ratio tests for differential expression, with Benjamini-Hochberg
correction for multiple testing.

Installation
------------

DESeq2 is an R/Bioconductor package. Install it from within R:

.. code-block:: r

   if (!requireNamespace("BiocManager", quietly = TRUE))
       install.packages("BiocManager")
   BiocManager::install("DESeq2")

Basic Usage
-----------

Run a complete differential expression analysis from a count matrix and sample
metadata table.

.. code-block:: r

   library(DESeq2)

   # Load count matrix and sample metadata
   counts <- read.csv("counts.csv", row.names = 1)
   coldata <- read.csv("sample_info.csv", row.names = 1)

   # Create DESeq2 dataset
   dds <- DESeqDataSetFromMatrix(countData = counts,
                                  colData = coldata,
                                  design = ~ condition)

   # Run differential expression analysis
   dds <- DESeq(dds)
   res <- results(dds, contrast = c("condition", "treated", "control"))

   # Filter significant genes (adjusted p-value < 0.05, |log2FC| > 1)
   sig <- subset(res, padj < 0.05 & abs(log2FoldChange) > 1)
   cat("Significant DE genes:", nrow(sig), "\n")

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter / function
     - Description
   * - ``DESeqDataSetFromMatrix()``
     - Create a DESeq2 dataset from a raw count matrix, column metadata data
       frame, and a design formula.
   * - ``design = ~ condition``
     - The design formula specifying the experimental factors to test; can
       include multiple terms (e.g. ``~ batch + condition``).
   * - ``DESeq()``
     - Run the full pipeline: estimate size factors, estimate dispersions,
       fit the negative binomial GLM, and perform Wald tests.
   * - ``results()``
     - Extract a results table for a given contrast or coefficient.
   * - ``contrast``
     - A character vector of length 3 specifying the factor, numerator level,
       and denominator level (e.g. ``c("condition", "treated", "control")``).
   * - ``lfcShrink()``
     - Apply log-fold-change shrinkage using the ``apeglm``, ``ashr``, or
       ``normal`` method for more reliable effect size estimates.
   * - ``plotMA()``
     - Generate an MA plot showing log-fold change versus mean expression.
   * - ``plotPCA()``
     - Plot a PCA of the variance-stabilised or rlog-transformed data for
       sample-level quality assessment.

Expected Output
---------------

The ``results()`` function returns a ``DESeqResults`` data frame with one row
per gene and the following columns:

* ``baseMean`` -- mean of normalised counts across all samples.
* ``log2FoldChange`` -- estimated log2 fold change between conditions.
* ``lfcSE`` -- standard error of the log2 fold change estimate.
* ``stat`` -- Wald test statistic.
* ``pvalue`` -- raw p-value from the Wald test.
* ``padj`` -- Benjamini-Hochberg adjusted p-value (FDR).

The results can be exported as a CSV file:

.. code-block:: r

   write.csv(as.data.frame(res), file = "deseq2_results.csv")

See Also
--------

* :doc:`edger` -- alternative Bioconductor package for differential expression
  using a negative binomial model with different normalisation and dispersion
  estimation strategies
* :doc:`/tools/quantification/featurecounts` -- generate the count matrix from
  aligned BAM files
* :doc:`/tools/quantification/salmon` -- alignment-free quantification whose
  output can be imported via tximport
* :doc:`/tools/quantification/kallisto` -- pseudoalignment-based
  quantification compatible with DESeq2 via tximport
