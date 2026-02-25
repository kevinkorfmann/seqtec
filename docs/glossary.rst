Glossary
========

.. glossary::
   :sorted:

   ASV
      Amplicon Sequence Variant. Exact biological sequences resolved by DADA2,
      replacing the older OTU approach in 16S amplicon analysis.

   BAM
      Binary Alignment Map. Compressed binary form of the SAM format for
      storing aligned sequencing reads.

   BED
      Browser Extensible Data. Tab-delimited format for genomic intervals
      using 0-based, half-open coordinates.

   BUSCO
      Benchmarking Universal Single-Copy Orthologs. Tool for assessing
      genome assembly completeness using conserved gene sets.

   BWA
      Burrows-Wheeler Aligner. Short-read alignment tool; BWA-MEM2 is the
      faster SIMD-optimized successor.

   CIGAR
      Compact Idiosyncratic Gapped Alignment Report. String in SAM format
      describing how a read aligns to the reference (e.g., ``151M``,
      ``75M2I74M``).

   CpG
      Cytosine-phosphate-Guanine dinucleotide. Primary target of DNA
      methylation in mammalian genomes.

   CRAM
      Reference-based compressed alignment format. More compact than BAM
      but requires the reference genome for decoding.

   DE
      Differential Expression. Statistical identification of genes with
      significantly different expression levels between conditions.

   DMR
      Differentially Methylated Region. Genomic region with statistically
      significant methylation differences between conditions.

   DSL2
      Domain Specific Language version 2. Nextflow's modular workflow
      syntax enabling process reuse and sub-workflows.

   eDNA
      Environmental DNA. DNA extracted directly from environmental samples
      (water, soil) without isolating organisms.

   FASTQ
      Text-based format storing nucleotide sequences together with
      per-base Phred quality scores.

   FASTA
      Text-based format for nucleotide or protein sequences. Uses ``>``
      header lines followed by sequence data.

   FLAG
      Bitwise flag in SAM format encoding read properties (paired, mapped,
      duplicate, etc.). E.g., 99 = paired, proper pair, mate reverse, first
      in pair.

   GFF
      General Feature Format. Tab-delimited format for genomic annotations
      (genes, exons, CDS). GFF3 is the current version.

   GTF
      Gene Transfer Format (GFF version 2). Widely used for gene annotations,
      especially from GENCODE and Ensembl.

   GVCF
      Genomic VCF. GATK's extended VCF that records confidence at every
      position, enabling efficient joint genotyping.

   h5ad
      HDF5-based file format used by AnnData/Scanpy for single-cell data.
      Stores count matrices, cell metadata, and embeddings.

   HPC
      High-Performance Computing. Cluster computing environment managed
      by job schedulers like SLURM.

   HVG
      Highly Variable Genes. Genes with the most variable expression across
      cells, selected as informative features for dimensionality reduction.

   IGV
      Integrative Genomics Viewer. Desktop application for interactive
      visualization of genomic data (BAM, VCF, BED, BigWig).

   indel
      Insertion or deletion variant relative to the reference genome.

   MAPQ
      Mapping Quality. Phred-scaled probability that an alignment is wrong.
      MAPQ 30 means 1 in 1000 chance of incorrect mapping.

   MEX
      Market Exchange format. Sparse matrix format (matrix.mtx, barcodes.tsv,
      features.tsv) output by Cell Ranger and STARsolo.

   NGS
      Next-Generation Sequencing. High-throughput DNA/RNA sequencing
      technologies producing millions of reads per run.

   ONT
      Oxford Nanopore Technologies. Long-read sequencing platform that
      reads DNA by measuring ionic current changes through nanopores.

   OTU
      Operational Taxonomic Unit. Cluster of similar sequences (typically
      97% identity) used in older 16S analyses. Superseded by ASVs.

   PCA
      Principal Component Analysis. Dimensionality reduction method used
      to identify major axes of variation in gene expression data.

   Phred
      Quality score encoding where Q = -10 log10(P_error). Q30 means
      99.9% base call accuracy.

   RPKM
      Reads Per Kilobase per Million mapped reads. Normalization method
      for coverage tracks accounting for library size and region length.

   SAM
      Sequence Alignment/Map. Tab-delimited text format for storing
      aligned sequencing reads against a reference genome.

   SLURM
      Simple Linux Utility for Resource Management. Widely used HPC job
      scheduling system.

   SNV
      Single Nucleotide Variant. Single base-pair change relative to the
      reference genome.

   SRA
      Sequence Read Archive. NCBI's primary repository for raw sequencing
      data from high-throughput platforms.

   TSS
      Transcription Start Site. Genomic position where RNA polymerase
      begins transcription of a gene.

   UMAP
      Uniform Manifold Approximation and Projection. Non-linear
      dimensionality reduction used for visualizing single-cell data.

   UMI
      Unique Molecular Identifier. Random barcode attached during library
      preparation to tag individual molecules, enabling PCR duplicate
      removal in single-cell and other protocols.

   VCF
      Variant Call Format. Standard format for storing genetic variants
      (SNVs, indels, structural variants) with genotype information.

   VQSR
      Variant Quality Score Recalibration. GATK's machine-learning approach
      to variant filtering using known variant databases as training data.

   WGS
      Whole Genome Sequencing. Sequencing of an organism's entire genome
      at uniform coverage.

   WGBS
      Whole Genome Bisulfite Sequencing. Technique for measuring DNA
      methylation at single-base resolution across the entire genome.
