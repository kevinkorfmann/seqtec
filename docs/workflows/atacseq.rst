ATAC-seq
========

Overview
--------

Assay for Transposase-Accessible Chromatin using sequencing (ATAC-seq) maps
genome-wide chromatin accessibility. Tn5 transposase inserts sequencing adapters
into open chromatin regions, and the resulting fragments are sequenced. The
analysis pipeline trims reads, aligns to the reference genome, removes
duplicates and mitochondrial reads, shifts alignments to account for the Tn5
insertion offset, calls peaks representing accessible regions, and produces
signal tracks for visualisation in a genome browser.

Pipeline Steps
--------------

1. Trim adapters and low-quality bases with fastp.
2. Align reads to the reference genome using Bowtie2.
3. Filter out mitochondrial reads, low-quality alignments, and duplicates.
4. Apply the Tn5 offset shift (+4 bp/--5 bp) to aligned reads.
5. Call peaks with MACS2 in narrow-peak mode.
6. Generate normalised signal tracks (bigWig) with deepTools.
7. Produce a fragment-size distribution plot as a QC metric.
8. Aggregate QC metrics into a MultiQC report.

Implementation
--------------

.. tabs::

   .. tab:: Snakemake

      .. code-block:: python

         # Snakefile -- ATAC-seq Peak Calling Pipeline
         configfile: "config.yaml"

         SAMPLES   = config["samples"]
         REF       = config["bowtie2_index"]
         BLACKLIST = config["blacklist"]
         GENOME    = config.get("genome_size", "hs")

         rule all:
             input:
                 expand("results/peaks/{sample}_peaks.narrowPeak",
                        sample=SAMPLES),
                 expand("results/bigwig/{sample}.normalized.bw",
                        sample=SAMPLES),
                 "results/multiqc/multiqc_report.html"

         rule fastp_trim:
             input:
                 r1="data/{sample}_R1.fastq.gz",
                 r2="data/{sample}_R2.fastq.gz"
             output:
                 r1="results/trimmed/{sample}_R1.trimmed.fastq.gz",
                 r2="results/trimmed/{sample}_R2.trimmed.fastq.gz",
                 json="results/trimmed/{sample}_fastp.json"
             threads: 4
             conda: "envs/qc.yaml"
             shell:
                 """
                 fastp -i {input.r1} -I {input.r2} \
                   -o {output.r1} -O {output.r2} \
                   -j {output.json} \
                   --detect_adapter_for_pe --thread {threads}
                 """

         rule bowtie2_align:
             input:
                 r1="results/trimmed/{sample}_R1.trimmed.fastq.gz",
                 r2="results/trimmed/{sample}_R2.trimmed.fastq.gz",
                 index=REF
             output:
                 bam="results/aligned/{sample}.sorted.bam"
             threads: 16
             conda: "envs/align.yaml"
             shell:
                 """
                 bowtie2 -x {input.index} \
                   -1 {input.r1} -2 {input.r2} \
                   --very-sensitive -X 2000 --no-mixed --no-discordant \
                   --threads {threads} \
                   | samtools sort -@ 4 -o {output.bam} -
                 samtools index {output.bam}
                 """

         rule filter_and_dedup:
             input:
                 "results/aligned/{sample}.sorted.bam"
             output:
                 bam="results/filtered/{sample}.filtered.bam",
                 metrics="results/filtered/{sample}.dup_metrics.txt"
             threads: 8
             conda: "envs/align.yaml"
             shell:
                 """
                 # Remove mitochondrial, low-quality, and unmapped reads
                 samtools view -@ {threads} -h -q 30 -f 2 -F 1804 \
                   {input} | grep -v chrM \
                   | samtools sort -@ 4 -o results/filtered/{wildcards.sample}.tmp.bam -
                 # Mark and remove duplicates
                 sambamba markdup -t {threads} --remove-duplicates \
                   results/filtered/{wildcards.sample}.tmp.bam {output.bam} \
                   2> {output.metrics}
                 samtools index {output.bam}
                 rm -f results/filtered/{wildcards.sample}.tmp.bam
                 """

         rule tn5_shift:
             input:
                 "results/filtered/{sample}.filtered.bam"
             output:
                 "results/shifted/{sample}.shifted.bam"
             threads: 4
             conda: "envs/align.yaml"
             shell:
                 """
                 alignmentSieve -b {input} -o {output} \
                   --ATACshift --numberOfProcessors {threads}
                 samtools sort -@ {threads} -o {output} {output}
                 samtools index {output}
                 """

         rule macs2_callpeak:
             input:
                 "results/shifted/{sample}.shifted.bam"
             output:
                 peaks="results/peaks/{sample}_peaks.narrowPeak",
                 xls="results/peaks/{sample}_peaks.xls"
             params:
                 genome=GENOME,
                 name="{sample}"
             conda: "envs/peaks.yaml"
             shell:
                 """
                 macs2 callpeak -t {input} \
                   -f BAMPE -g {params.genome} \
                   -n {params.name} --outdir results/peaks/ \
                   --nomodel --shift -100 --extsize 200 \
                   --keep-dup all -q 0.05
                 """

         rule bigwig:
             input:
                 "results/shifted/{sample}.shifted.bam"
             output:
                 "results/bigwig/{sample}.normalized.bw"
             threads: 8
             conda: "envs/peaks.yaml"
             shell:
                 """
                 bamCoverage -b {input} -o {output} \
                   --normalizeUsing RPGC \
                   --effectiveGenomeSize 2913022398 \
                   --binSize 10 --numberOfProcessors {threads} \
                   --blackListFileName {BLACKLIST}
                 """

         rule multiqc:
             input:
                 expand("results/trimmed/{sample}_fastp.json", sample=SAMPLES),
                 expand("results/filtered/{sample}.dup_metrics.txt",
                        sample=SAMPLES),
                 expand("results/peaks/{sample}_peaks.xls", sample=SAMPLES)
             output:
                 "results/multiqc/multiqc_report.html"
             conda: "envs/qc.yaml"
             shell:
                 "multiqc results/ -o results/multiqc/ --force"

   .. tab:: Nextflow

      .. code-block:: groovy

         #!/usr/bin/env nextflow
         nextflow.enable.dsl = 2

         params.reads       = "data/*_{R1,R2}.fastq.gz"
         params.bt2_index   = "ref/bt2_index"
         params.blacklist   = "ref/blacklist.bed"
         params.genome_size = "hs"
         params.outdir      = "results"

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

         process BOWTIE2_ALIGN {
             tag "${sample_id}"
             publishDir "${params.outdir}/aligned", mode: 'copy'
             cpus 16
             input:
                 tuple val(sample_id), path(reads)
                 path(index)
             output:
                 tuple val(sample_id), path("*.sorted.bam"), path("*.sorted.bam.bai"), emit: bam
             script:
             def (r1, r2) = reads
             """
             bowtie2 -x ${index}/${index.name} \
               -1 ${r1} -2 ${r2} \
               --very-sensitive -X 2000 --no-mixed --no-discordant \
               --threads ${task.cpus} \
               | samtools sort -@ 4 -o ${sample_id}.sorted.bam -
             samtools index ${sample_id}.sorted.bam
             """
         }

         process FILTER_DEDUP {
             tag "${sample_id}"
             publishDir "${params.outdir}/filtered", mode: 'copy'
             cpus 8
             input:  tuple val(sample_id), path(bam), path(bai)
             output: tuple val(sample_id), path("*.filtered.bam"), path("*.filtered.bam.bai"), emit: bam
             script:
             """
             samtools view -@ ${task.cpus} -h -q 30 -f 2 -F 1804 \
               ${bam} | grep -v chrM \
               | samtools sort -@ 4 -o tmp.bam -
             sambamba markdup -t ${task.cpus} --remove-duplicates \
               tmp.bam ${sample_id}.filtered.bam
             samtools index ${sample_id}.filtered.bam
             rm -f tmp.bam
             """
         }

         process TN5_SHIFT {
             tag "${sample_id}"
             publishDir "${params.outdir}/shifted", mode: 'copy'
             cpus 4
             input:  tuple val(sample_id), path(bam), path(bai)
             output: tuple val(sample_id), path("*.shifted.bam"), path("*.shifted.bam.bai"), emit: bam
             script:
             """
             alignmentSieve -b ${bam} -o ${sample_id}.shifted.bam \
               --ATACshift --numberOfProcessors ${task.cpus}
             samtools sort -@ ${task.cpus} -o ${sample_id}.shifted.sorted.bam \
               ${sample_id}.shifted.bam
             mv ${sample_id}.shifted.sorted.bam ${sample_id}.shifted.bam
             samtools index ${sample_id}.shifted.bam
             """
         }

         process MACS2_CALLPEAK {
             tag "${sample_id}"
             publishDir "${params.outdir}/peaks", mode: 'copy'
             input:  tuple val(sample_id), path(bam), path(bai)
             output: path("${sample_id}_peaks.narrowPeak"), emit: peaks
             script:
             """
             macs2 callpeak -t ${bam} \
               -f BAMPE -g ${params.genome_size} \
               -n ${sample_id} --outdir . \
               --nomodel --shift -100 --extsize 200 \
               --keep-dup all -q 0.05
             """
         }

         process BIGWIG {
             tag "${sample_id}"
             publishDir "${params.outdir}/bigwig", mode: 'copy'
             cpus 8
             input:
                 tuple val(sample_id), path(bam), path(bai)
                 path(blacklist)
             output: path("*.normalized.bw"), emit: bw
             script:
             """
             bamCoverage -b ${bam} -o ${sample_id}.normalized.bw \
               --normalizeUsing RPGC \
               --effectiveGenomeSize 2913022398 \
               --binSize 10 --numberOfProcessors ${task.cpus} \
               --blackListFileName ${blacklist}
             """
         }

         process MULTIQC {
             publishDir "${params.outdir}/multiqc", mode: 'copy'
             input:  path('*')
             output: path("multiqc_report.html")
             script:
             """
             multiqc . -o . --force
             """
         }

         workflow {
             reads_ch     = Channel.fromFilePairs(params.reads, checkIfExists: true)
             bt2_index_ch = Channel.value(file(params.bt2_index))
             blacklist_ch = Channel.value(file(params.blacklist))

             FASTP(reads_ch)
             BOWTIE2_ALIGN(FASTP.out.trimmed, bt2_index_ch)
             FILTER_DEDUP(BOWTIE2_ALIGN.out.bam)
             TN5_SHIFT(FILTER_DEDUP.out.bam)
             MACS2_CALLPEAK(TN5_SHIFT.out.bam)
             BIGWIG(TN5_SHIFT.out.bam, blacklist_ch)

             ch_multiqc = FASTP.out.json.collect()
             MULTIQC(ch_multiqc)
         }

See Also
--------

* :doc:`snakemake` -- Snakemake workflow manager overview
* :doc:`nextflow` -- Nextflow DSL2 workflow manager overview
* :doc:`chipseq` -- ChIP-seq workflow (related chromatin profiling assay)
* :doc:`/tools/alignment/bowtie2` -- Bowtie2 aligner reference
* :doc:`/tools/epigenomics/index` -- Epigenomics tools
