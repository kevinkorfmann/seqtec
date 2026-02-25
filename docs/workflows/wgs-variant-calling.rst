WGS Variant Calling
===================

Overview
--------

Whole-genome sequencing (WGS) variant calling identifies single-nucleotide
variants (SNVs), insertions, and deletions (indels) from short-read sequencing
data. The workflow follows the GATK Best Practices for germline variant
discovery: reads are trimmed, aligned to a reference genome with BWA-MEM2,
deduplicated, and passed through GATK HaplotypeCaller in GVCF mode. Per-sample
GVCFs are combined and jointly genotyped, followed by variant quality score
recalibration (VQSR) and functional annotation with Ensembl VEP.

Pipeline Steps
--------------

1. Trim adapters and low-quality bases with fastp.
2. Align reads to the reference genome using BWA-MEM2.
3. Sort and index alignments with samtools.
4. Mark PCR duplicates with sambamba.
5. Call variants per sample in GVCF mode using GATK HaplotypeCaller.
6. Combine per-sample GVCFs with GATK CombineGVCFs.
7. Jointly genotype all samples with GATK GenotypeGVCFs.
8. Apply variant quality score recalibration (VQSR) for SNPs.
9. Annotate variants with Ensembl VEP.
10. Aggregate QC metrics into a MultiQC report.

Implementation
--------------

.. tabs::

   .. tab:: Snakemake

      .. code-block:: python

         # Snakefile -- WGS Germline Variant Calling (GATK Best Practices)
         configfile: "config.yaml"

         SAMPLES = config["samples"]
         REF     = config["reference"]
         KNOWN   = config["known_sites"]

         rule all:
             input:
                 "results/annotation/all_samples.annotated.vcf",
                 "results/multiqc/multiqc_report.html"

         rule fastp_trim:
             input:
                 r1="data/{sample}_R1.fastq.gz",
                 r2="data/{sample}_R2.fastq.gz"
             output:
                 r1="results/trimmed/{sample}_R1.trimmed.fastq.gz",
                 r2="results/trimmed/{sample}_R2.trimmed.fastq.gz",
                 json="results/trimmed/{sample}_fastp.json",
                 html="results/trimmed/{sample}_fastp.html"
             threads: 4
             conda: "envs/qc.yaml"
             shell:
                 """
                 fastp -i {input.r1} -I {input.r2} \
                   -o {output.r1} -O {output.r2} \
                   -j {output.json} -h {output.html} \
                   --detect_adapter_for_pe --thread {threads}
                 """

         rule bwa_mem2_align:
             input:
                 r1="results/trimmed/{sample}_R1.trimmed.fastq.gz",
                 r2="results/trimmed/{sample}_R2.trimmed.fastq.gz",
                 ref=REF
             output:
                 bam="results/aligned/{sample}.sorted.bam"
             threads: 16
             params:
                 rg=lambda wc: f"@RG\\tID:{wc.sample}\\tSM:{wc.sample}\\tPL:ILLUMINA"
             conda: "envs/align.yaml"
             shell:
                 """
                 bwa-mem2 mem -t {threads} -R '{params.rg}' {input.ref} \
                   {input.r1} {input.r2} \
                   | samtools sort -@ 4 -o {output.bam} -
                 samtools index {output.bam}
                 """

         rule mark_duplicates:
             input:
                 "results/aligned/{sample}.sorted.bam"
             output:
                 bam="results/dedup/{sample}.dedup.bam",
                 metrics="results/dedup/{sample}.dup_metrics.txt"
             threads: 8
             conda: "envs/align.yaml"
             shell:
                 """
                 sambamba markdup -t {threads} \
                   {input} {output.bam} 2> {output.metrics}
                 """

         rule haplotype_caller:
             input:
                 bam="results/dedup/{sample}.dedup.bam",
                 ref=REF
             output:
                 gvcf="results/gvcf/{sample}.g.vcf.gz"
             threads: 4
             conda: "envs/gatk.yaml"
             shell:
                 """
                 gatk HaplotypeCaller \
                   -R {input.ref} -I {input.bam} \
                   -O {output.gvcf} -ERC GVCF \
                   --native-pair-hmm-threads {threads}
                 """

         rule combine_gvcfs:
             input:
                 gvcfs=expand("results/gvcf/{sample}.g.vcf.gz",
                               sample=SAMPLES),
                 ref=REF
             output:
                 "results/genotyped/combined.g.vcf.gz"
             params:
                 gvcf_args=lambda wc, input: " ".join(
                     [f"-V {g}" for g in input.gvcfs])
             conda: "envs/gatk.yaml"
             shell:
                 """
                 gatk CombineGVCFs -R {input.ref} {params.gvcf_args} \
                   -O {output}
                 """

         rule genotype_gvcfs:
             input:
                 gvcf="results/genotyped/combined.g.vcf.gz",
                 ref=REF
             output:
                 "results/genotyped/all_samples.vcf.gz"
             conda: "envs/gatk.yaml"
             shell:
                 """
                 gatk GenotypeGVCFs -R {input.ref} -V {input.gvcf} \
                   -O {output}
                 """

         rule vqsr_snps:
             input:
                 vcf="results/genotyped/all_samples.vcf.gz",
                 ref=REF
             output:
                 recal="results/vqsr/snps.recal",
                 tranches="results/vqsr/snps.tranches",
                 vcf="results/vqsr/snps_recalibrated.vcf.gz"
             params:
                 hapmap=config["hapmap"],
                 omni=config["omni"],
                 g1k=config["g1k_snps"],
                 dbsnp=config["dbsnp"]
             conda: "envs/gatk.yaml"
             shell:
                 """
                 gatk VariantRecalibrator -R {input.ref} -V {input.vcf} \
                   --resource:hapmap,known=false,training=true,truth=true,prior=15.0 {params.hapmap} \
                   --resource:omni,known=false,training=true,truth=false,prior=12.0 {params.omni} \
                   --resource:1000G,known=false,training=true,truth=false,prior=10.0 {params.g1k} \
                   --resource:dbsnp,known=true,training=false,truth=false,prior=2.0 {params.dbsnp} \
                   -an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR \
                   -mode SNP -O {output.recal} --tranches-file {output.tranches}

                 gatk ApplyVQSR -R {input.ref} -V {input.vcf} \
                   --recal-file {output.recal} --tranches-file {output.tranches} \
                   --truth-sensitivity-filter-level 99.5 -mode SNP \
                   -O {output.vcf}
                 """

         rule vep_annotate:
             input:
                 "results/vqsr/snps_recalibrated.vcf.gz"
             output:
                 "results/annotation/all_samples.annotated.vcf"
             threads: 4
             conda: "envs/annotation.yaml"
             shell:
                 """
                 vep --input_file {input} --output_file {output} \
                   --format vcf --vcf --fork {threads} \
                   --cache --offline --assembly GRCh38 \
                   --sift b --polyphen b --symbol --numbers \
                   --canonical --biotype --af --af_1kg --af_gnomade
                 """

         rule multiqc:
             input:
                 expand("results/trimmed/{sample}_fastp.json", sample=SAMPLES),
                 expand("results/dedup/{sample}.dup_metrics.txt", sample=SAMPLES)
             output:
                 "results/multiqc/multiqc_report.html"
             conda: "envs/qc.yaml"
             shell:
                 "multiqc results/ -o results/multiqc/ --force"

   .. tab:: Nextflow

      .. code-block:: groovy

         #!/usr/bin/env nextflow
         nextflow.enable.dsl = 2

         params.reads     = "data/*_{R1,R2}.fastq.gz"
         params.ref       = "ref/GRCh38.fa"
         params.outdir    = "results"
         params.dbsnp     = "ref/dbsnp_156.vcf.gz"

         process FASTP {
             tag "${sample_id}"
             publishDir "${params.outdir}/trimmed", mode: 'copy'
             cpus 4
             input:  tuple val(sample_id), path(reads)
             output:
                 tuple val(sample_id), path("*_trimmed.fastq.gz"), emit: trimmed
                 path("*.json"), emit: json
             script:
             def (r1, r2) = reads
             """
             fastp -i ${r1} -I ${r2} \
               -o ${sample_id}_R1_trimmed.fastq.gz \
               -O ${sample_id}_R2_trimmed.fastq.gz \
               -j ${sample_id}_fastp.json \
               --detect_adapter_for_pe --thread ${task.cpus}
             """
         }

         process BWA_MEM2 {
             tag "${sample_id}"
             publishDir "${params.outdir}/aligned", mode: 'copy'
             cpus 16
             memory '32 GB'
             input:
                 tuple val(sample_id), path(reads)
                 path(ref)
             output:
                 tuple val(sample_id), path("*.sorted.bam"), path("*.sorted.bam.bai"), emit: bam
             script:
             def (r1, r2) = reads
             """
             bwa-mem2 mem -t ${task.cpus} \
               -R "@RG\\tID:${sample_id}\\tSM:${sample_id}\\tPL:ILLUMINA" \
               ${ref} ${r1} ${r2} \
               | samtools sort -@ 4 -o ${sample_id}.sorted.bam -
             samtools index ${sample_id}.sorted.bam
             """
         }

         process MARKDUP {
             tag "${sample_id}"
             publishDir "${params.outdir}/dedup", mode: 'copy'
             cpus 8
             input:  tuple val(sample_id), path(bam), path(bai)
             output: tuple val(sample_id), path("*.dedup.bam"), path("*.dedup.bam.bai"), emit: bam
             script:
             """
             sambamba markdup -t ${task.cpus} ${bam} ${sample_id}.dedup.bam
             samtools index ${sample_id}.dedup.bam
             """
         }

         process HAPLOTYPE_CALLER {
             tag "${sample_id}"
             publishDir "${params.outdir}/gvcf", mode: 'copy'
             cpus 4
             memory '16 GB'
             input:
                 tuple val(sample_id), path(bam), path(bai)
                 path(ref)
             output: tuple val(sample_id), path("*.g.vcf.gz"), path("*.g.vcf.gz.tbi"), emit: gvcf
             script:
             """
             gatk HaplotypeCaller -R ${ref} -I ${bam} \
               -O ${sample_id}.g.vcf.gz -ERC GVCF \
               --native-pair-hmm-threads ${task.cpus}
             """
         }

         process JOINT_GENOTYPE {
             publishDir "${params.outdir}/genotyped", mode: 'copy'
             memory '32 GB'
             input:
                 path(gvcfs)
                 path(tbis)
                 path(ref)
             output: path("all_samples.vcf.gz"), emit: vcf
             script:
             def gvcf_args = gvcfs.collect { "-V ${it}" }.join(' ')
             """
             gatk CombineGVCFs -R ${ref} ${gvcf_args} -O combined.g.vcf.gz
             gatk GenotypeGVCFs -R ${ref} -V combined.g.vcf.gz \
               -O all_samples.vcf.gz
             """
         }

         process VEP_ANNOTATE {
             publishDir "${params.outdir}/annotation", mode: 'copy'
             cpus 4
             input:  path(vcf)
             output: path("annotated.vcf")
             script:
             """
             vep --input_file ${vcf} --output_file annotated.vcf \
               --format vcf --vcf --fork ${task.cpus} \
               --cache --offline --assembly GRCh38 \
               --sift b --polyphen b --symbol --canonical --af_gnomade
             """
         }

         workflow {
             reads_ch = Channel.fromFilePairs(params.reads, checkIfExists: true)
             ref_ch   = Channel.value(file(params.ref))

             FASTP(reads_ch)
             BWA_MEM2(FASTP.out.trimmed, ref_ch)
             MARKDUP(BWA_MEM2.out.bam)
             HAPLOTYPE_CALLER(MARKDUP.out.bam, ref_ch)

             gvcfs = HAPLOTYPE_CALLER.out.gvcf.map { it[1] }.collect()
             tbis  = HAPLOTYPE_CALLER.out.gvcf.map { it[2] }.collect()

             JOINT_GENOTYPE(gvcfs, tbis, ref_ch)
             VEP_ANNOTATE(JOINT_GENOTYPE.out.vcf)
         }

See Also
--------

* :doc:`snakemake` -- Snakemake workflow manager overview
* :doc:`nextflow` -- Nextflow DSL2 workflow manager overview
* :doc:`/tools/variant-calling/gatk` -- GATK variant caller reference
* :doc:`/tools/alignment/bwa-mem2` -- BWA-MEM2 aligner reference
* :doc:`/tools/variant-annotation/vep` -- Ensembl VEP annotation reference
