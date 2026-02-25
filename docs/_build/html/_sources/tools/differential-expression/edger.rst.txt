edgeR
=====

Overview
--------

edgeR is an R/Bioconductor package for differential expression analysis of
count-based data from RNA-seq and other high-throughput sequencing assays. It
models count data with the negative binomial distribution and estimates
gene-wise dispersions using an empirical Bayes approach that shares information
across genes, providing robust results even with small sample sizes. edgeR
supports multiple testing frameworks including exact tests for pairwise
comparisons, generalised linear models (GLMs) with likelihood ratio tests, and
quasi-likelihood F-tests. It uses TMM (trimmed mean of M-values) normalisation
to account for compositional differences between libraries.

Installation
------------

edgeR is an R/Bioconductor package. Install it from within R:

.. code-block:: r

   if (!requireNamespace("BiocManager", quietly = TRUE))
       install.packages("BiocManager")
   BiocManager::install("edgeR")

Basic Usage
-----------

Run a quasi-likelihood differential expression analysis from a count matrix.

.. code-block:: r

   library(edgeR)

   counts <- read.csv("counts.csv", row.names = 1)
   group <- factor(c("control", "control", "treated", "treated"))

   y <- DGEList(counts = counts, group = group)
   y <- filterByExpr(y) |> (\(keep) y[keep, , keep.lib.sizes = FALSE])()
   y <- calcNormFactors(y)
   design <- model.matrix(~ group)
   y <- estimateDisp(y, design)

   fit <- glmQLFit(y, design)
   qlf <- glmQLFTest(fit, coef = 2)
   topTags(qlf, n = 20)

Key Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Function / parameter
     - Description
   * - ``DGEList()``
     - Create a DGEList object from a count matrix, with sample grouping and
       optional library size information.
   * - ``filterByExpr()``
     - Determine which genes have sufficiently large counts to be retained for
       statistical analysis.
   * - ``calcNormFactors()``
     - Calculate TMM normalisation factors to account for compositional
       differences between libraries.
   * - ``estimateDisp()``
     - Estimate common, trended, and tagwise dispersions using the empirical
       Bayes method and a design matrix.
   * - ``model.matrix()``
     - Define the experimental design for the GLM (e.g. ``~ group`` or
       ``~ batch + group``).
   * - ``glmQLFit()``
     - Fit a quasi-likelihood negative binomial GLM to the data.
   * - ``glmQLFTest()``
     - Perform a quasi-likelihood F-test on specified model coefficients or
       contrasts.
   * - ``topTags()``
     - Extract a table of the top differentially expressed genes, ranked by
       p-value.
   * - ``exactTest()``
     - Perform an exact test for differences between two groups (alternative
       to the GLM approach).

Expected Output
---------------

The ``topTags()`` function returns a data frame with one row per gene and the
following columns:

* ``logFC`` -- log2 fold change between conditions.
* ``logCPM`` -- average log2 counts per million across all samples.
* ``F`` -- quasi-likelihood F-statistic (or ``LR`` for likelihood ratio tests,
  or ``PValue`` for exact tests).
* ``PValue`` -- raw p-value.
* ``FDR`` -- false discovery rate (Benjamini-Hochberg adjusted p-value).

The full results table can be exported:

.. code-block:: r

   results <- topTags(qlf, n = Inf)
   write.csv(results$table, file = "edger_results.csv")

See Also
--------

* :doc:`deseq2` -- alternative Bioconductor package for differential
  expression using a negative binomial model with shrinkage estimators
* :doc:`/tools/quantification/featurecounts` -- generate the count matrix from
  aligned BAM files
* :doc:`/tools/quantification/salmon` -- alignment-free transcript
  quantification compatible with edgeR via tximport
* :doc:`/tools/quantification/htseq` -- read counting tool whose output can
  be used directly with edgeR
