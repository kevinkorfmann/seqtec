Nanopore Variant Calling
========================

Overview
--------

Oxford Nanopore long reads can be used for germline variant calling when aligned
to a reference genome and processed with a deep-learning-based variant caller.
This pipeline maps reads with minimap2, calls SNPs and indels with Clair3 (a
pileup-and-full-alignment neural-network caller optimized for Nanopore data),
and filters variants with bcftools. Clair3 leverages platform-specific models
trained on Nanopore error profiles, achieving high accuracy on both SNPs and
small indels from long-read data.

Pipeline Steps
--------------

1. **minimap2 align** -- Map Nanopore reads to the reference genome using
   minimap2 in ``map-ont`` mode with MD tags for accurate variant calling.
   Output is piped through samtools sort to produce a coordinate-sorted BAM.
2. **samtools index** -- Index the sorted BAM file for random access by
   downstream tools.
3. **Clair3** -- Call germline variants (SNPs and indels) using the Clair3
   deep-learning model appropriate for the Nanopore chemistry. The
   ``--include_all_ctgs`` flag processes all contigs in the reference.
4. **bcftools filter** -- Apply quality and depth filters to remove low-
   confidence variant calls (QUAL >= 20, DP >= 10).
5. **bcftools stats** -- Generate summary statistics for the filtered variant
   set including counts of SNPs, indels, and ts/tv ratio.

Implementation
--------------

.. tabs::

   .. tab:: Snakemake

      .. code-block:: python

         # Snakefile -- Nanopore Variant Calling Pipeline
         configfile: "config.yaml"

         SAMPLES   = config["samples"]
         REFERENCE = config["reference"]
         MODEL     = config["clair3_model"]

         rule all:
             input:
                 expand("results/variants/{sample}_snps.vcf.gz", sample=SAMPLES),
                 expand("results/variants/{sample}_stats.txt", sample=SAMPLES)

         rule minimap2_align:
             input:
                 reads="data/{sample}.fastq.gz",
                 ref=REFERENCE
             output:
                 bam="results/aligned/{sample}.sorted.bam",
                 bai="results/aligned/{sample}.sorted.bam.bai"
             threads: 8
             shell:
                 """
                 minimap2 -ax map-ont --MD \
                   -R '@RG\\tID:{wildcards.sample}\\tSM:{wildcards.sample}\\tPL:ONT' \
                   {input.ref} {input.reads} \
                   | samtools sort -@ {threads} -o {output.bam} -
                 samtools index {output.bam}
                 """

         rule clair3:
             input:
                 bam="results/aligned/{sample}.sorted.bam",
                 bai="results/aligned/{sample}.sorted.bam.bai",
                 ref=REFERENCE
             output:
                 vcf="results/clair3/{sample}/merge_output.vcf.gz"
             params:
                 model=MODEL,
                 outdir="results/clair3/{sample}"
             threads: 8
             shell:
                 """
                 run_clair3.sh \
                   --bam_fn={input.bam} \
                   --ref_fn={input.ref} \
                   --output={params.outdir} \
                   --threads={threads} \
                   --platform="ont" \
                   --model_path={params.model} \
                   --sample_name={wildcards.sample} \
                   --include_all_ctgs
                 """

         rule bcftools_filter:
             input:
                 "results/clair3/{sample}/merge_output.vcf.gz"
             output:
                 filtered="results/variants/{sample}_filtered.vcf.gz",
                 snps="results/variants/{sample}_snps.vcf.gz",
                 stats="results/variants/{sample}_stats.txt"
             shell:
                 """
                 bcftools filter -i 'QUAL>=20 && INFO/DP>=10' \
                   {input} -Oz -o {output.filtered}
                 bcftools view -v snps {output.filtered} -Oz -o {output.snps}
                 bcftools stats {output.filtered} > {output.stats}
                 """

   .. tab:: Nextflow

      .. code-block:: groovy

         #!/usr/bin/env nextflow
         nextflow.enable.dsl = 2

         params.samplesheet  = "samplesheet.csv"
         params.reference    = "ref/reference.fna"
         params.clair3_model = "\${CONDA_PREFIX}/bin/models/ont"
         params.outdir       = "results"

         process MINIMAP2_ALIGN {
             tag "${sample_id}"
             publishDir "${params.outdir}/aligned", mode: 'copy'
             cpus 8
             memory '16 GB'
             input:
                 tuple val(sample_id), path(reads)
                 path(reference)
             output:
                 tuple val(sample_id),
                       path("${sample_id}.sorted.bam"),
                       path("${sample_id}.sorted.bam.bai"), emit: bam
             script:
             """
             minimap2 -ax map-ont --MD \
               -R '@RG\\tID:${sample_id}\\tSM:${sample_id}\\tPL:ONT' \
               ${reference} ${reads} \
               | samtools sort -@ ${task.cpus} -o ${sample_id}.sorted.bam -
             samtools index ${sample_id}.sorted.bam
             """
         }

         process CLAIR3 {
             tag "${sample_id}"
             publishDir "${params.outdir}/clair3/${sample_id}", mode: 'copy'
             cpus 8
             memory '32 GB'
             input:
                 tuple val(sample_id), path(bam), path(bai)
                 path(reference)
             output:
                 tuple val(sample_id),
                       path("merge_output.vcf.gz"), emit: vcf
             script:
             """
             run_clair3.sh \
               --bam_fn=${bam} \
               --ref_fn=${reference} \
               --output=. \
               --threads=${task.cpus} \
               --platform="ont" \
               --model_path=${params.clair3_model} \
               --sample_name=${sample_id} \
               --include_all_ctgs
             """
         }

         process BCFTOOLS_FILTER {
             tag "${sample_id}"
             publishDir "${params.outdir}/variants", mode: 'copy'
             input:
                 tuple val(sample_id), path(vcf)
             output:
                 tuple val(sample_id),
                       path("${sample_id}_filtered.vcf.gz"), emit: filtered
                 tuple val(sample_id),
                       path("${sample_id}_snps.vcf.gz"), emit: snps
                 path("${sample_id}_stats.txt"), emit: stats
             script:
             """
             bcftools filter -i 'QUAL>=20 && INFO/DP>=10' \
               ${vcf} -Oz -o ${sample_id}_filtered.vcf.gz
             bcftools view -v snps ${sample_id}_filtered.vcf.gz \
               -Oz -o ${sample_id}_snps.vcf.gz
             bcftools stats ${sample_id}_filtered.vcf.gz \
               > ${sample_id}_stats.txt
             """
         }

         workflow {
             ch_input = Channel.fromPath(params.samplesheet)
                 .splitCsv(header: true)
                 .map { row -> tuple(row.sample_id, file(row.fastq)) }

             reference = Channel.value(file(params.reference))

             MINIMAP2_ALIGN(ch_input, reference)
             CLAIR3(MINIMAP2_ALIGN.out.bam, reference)
             BCFTOOLS_FILTER(CLAIR3.out.vcf)
         }

Expected Output
---------------

After a successful run the output directory will contain:

* ``results/aligned/<sample>.sorted.bam`` -- Coordinate-sorted BAM file with
  read group tags and MD tags for variant calling.
* ``results/clair3/<sample>/merge_output.vcf.gz`` -- Raw Clair3 variant calls
  including SNPs and indels with quality scores and genotype likelihoods.
* ``results/variants/<sample>_filtered.vcf.gz`` -- Quality-filtered variants
  (QUAL >= 20, DP >= 10).
* ``results/variants/<sample>_snps.vcf.gz`` -- SNP-only subset of filtered
  variants.
* ``results/variants/<sample>_stats.txt`` -- Summary statistics including total
  variants, SNP count, indel count, and transition/transversion ratio.

See Also
--------

* :doc:`bacterial-genome-assembly` -- Nanopore bacterial genome assembly
* :doc:`wgs-variant-calling` -- Illumina WGS variant calling pipeline
