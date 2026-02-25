ChIP-seq
========

Overview
--------

Chromatin Immunoprecipitation followed by sequencing (ChIP-seq) identifies
genome-wide binding sites of transcription factors, histone modifications, and
other chromatin-associated proteins. After cross-linking, fragmentation, and
immunoprecipitation with a target-specific antibody, enriched DNA fragments are
sequenced. The analysis pipeline trims reads, aligns them to the reference
genome, removes duplicates, calls peaks relative to an input control using
MACS2, and generates normalised signal tracks for genome browser visualisation.

Pipeline Steps
--------------

1. Trim adapters and low-quality bases with fastp.
2. Align reads to the reference genome using Bowtie2.
3. Filter low-quality alignments and remove PCR duplicates.
4. Call peaks with MACS2 using matched input controls.
5. Filter peaks against a blacklist of problematic regions.
6. Generate normalised signal tracks (bigWig) with deepTools.
7. Compute quality metrics including FRiP (Fraction of Reads in Peaks).
8. Aggregate QC metrics into a MultiQC report.

Implementation
--------------

.. tabs::

   .. tab:: Snakemake

      .. code-block:: python

         # Snakefile -- ChIP-seq Peak Calling Pipeline
         configfile: "config.yaml"

         SAMPLES   = config["samples"]     # ChIP samples
         INPUTS    = config["inputs"]      # input controls per sample
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
                   --very-sensitive -X 1000 \
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
                 samtools view -@ {threads} -h -q 30 -f 2 -F 1804 \
                   {input} \
                   | samtools sort -@ 4 -o results/filtered/{wildcards.sample}.tmp.bam -
                 sambamba markdup -t {threads} --remove-duplicates \
                   results/filtered/{wildcards.sample}.tmp.bam {output.bam} \
                   2> {output.metrics}
                 samtools index {output.bam}
                 rm -f results/filtered/{wildcards.sample}.tmp.bam
                 """

         rule macs2_callpeak:
             input:
                 treatment="results/filtered/{sample}.filtered.bam",
                 control=lambda wc: f"results/filtered/{INPUTS[wc.sample]}.filtered.bam"
             output:
                 peaks="results/peaks/{sample}_peaks.narrowPeak",
                 xls="results/peaks/{sample}_peaks.xls"
             params:
                 genome=GENOME,
                 name="{sample}"
             conda: "envs/peaks.yaml"
             shell:
                 """
                 macs2 callpeak \
                   -t {input.treatment} -c {input.control} \
                   -f BAMPE -g {params.genome} \
                   -n {params.name} --outdir results/peaks/ \
                   -q 0.05
                 """

         rule filter_blacklist:
             input:
                 peaks="results/peaks/{sample}_peaks.narrowPeak",
                 blacklist=BLACKLIST
             output:
                 "results/peaks/{sample}_peaks.filtered.narrowPeak"
             conda: "envs/peaks.yaml"
             shell:
                 """
                 bedtools intersect -v \
                   -a {input.peaks} -b {input.blacklist} \
                   > {output}
                 """

         rule bigwig:
             input:
                 "results/filtered/{sample}.filtered.bam"
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
                   --extendReads 200
                 """

         rule frip_score:
             input:
                 bam="results/filtered/{sample}.filtered.bam",
                 peaks="results/peaks/{sample}_peaks.filtered.narrowPeak"
             output:
                 "results/qc/{sample}_frip.txt"
             conda: "envs/peaks.yaml"
             shell:
                 """
                 total=$(samtools view -c {input.bam})
                 in_peaks=$(bedtools intersect -a {input.bam} -b {input.peaks} \
                   -u -ubam | samtools view -c)
                 echo -e "{wildcards.sample}\t${{in_peaks}}\t${{total}}" > {output}
                 """

         rule multiqc:
             input:
                 expand("results/trimmed/{sample}_fastp.json",
                        sample=list(SAMPLES) + list(INPUTS.values())),
                 expand("results/filtered/{sample}.dup_metrics.txt",
                        sample=list(SAMPLES) + list(INPUTS.values())),
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
         params.input_csv   = "samplesheet.csv"  // sample_id,fastq_1,fastq_2,control_id

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
               --very-sensitive -X 1000 \
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
               ${bam} \
               | samtools sort -@ 4 -o tmp.bam -
             sambamba markdup -t ${task.cpus} --remove-duplicates \
               tmp.bam ${sample_id}.filtered.bam
             samtools index ${sample_id}.filtered.bam
             rm -f tmp.bam
             """
         }

         process MACS2_CALLPEAK {
             tag "${sample_id}"
             publishDir "${params.outdir}/peaks", mode: 'copy'
             input:
                 tuple val(sample_id), path(treatment_bam), path(treatment_bai)
                 tuple val(control_id), path(control_bam), path(control_bai)
             output:
                 tuple val(sample_id), path("${sample_id}_peaks.narrowPeak"), emit: peaks
             script:
             """
             macs2 callpeak \
               -t ${treatment_bam} -c ${control_bam} \
               -f BAMPE -g ${params.genome_size} \
               -n ${sample_id} --outdir . \
               -q 0.05
             """
         }

         process FILTER_BLACKLIST {
             tag "${sample_id}"
             publishDir "${params.outdir}/peaks", mode: 'copy'
             input:
                 tuple val(sample_id), path(peaks)
                 path(blacklist)
             output:
                 tuple val(sample_id), path("*_filtered.narrowPeak"), emit: peaks
             script:
             """
             bedtools intersect -v \
               -a ${peaks} -b ${blacklist} \
               > ${sample_id}_filtered.narrowPeak
             """
         }

         process BIGWIG {
             tag "${sample_id}"
             publishDir "${params.outdir}/bigwig", mode: 'copy'
             cpus 8
             input:  tuple val(sample_id), path(bam), path(bai)
             output: path("*.normalized.bw"), emit: bw
             script:
             """
             bamCoverage -b ${bam} -o ${sample_id}.normalized.bw \
               --normalizeUsing RPGC \
               --effectiveGenomeSize 2913022398 \
               --binSize 10 --numberOfProcessors ${task.cpus} \
               --extendReads 200
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

             // Parse samplesheet to get treatment-control pairs
             samplesheet = Channel.fromPath(params.input_csv)
                 .splitCsv(header: true)
                 .map { row -> [row.sample_id, row.control_id] }

             FASTP(reads_ch)
             BOWTIE2_ALIGN(FASTP.out.trimmed, bt2_index_ch)
             FILTER_DEDUP(BOWTIE2_ALIGN.out.bam)

             // Pair treatment with control BAMs
             treatment_ch = FILTER_DEDUP.out.bam
                 .join(samplesheet)
             control_bams = FILTER_DEDUP.out.bam
             paired_ch = treatment_ch
                 .map { sample_id, bam, bai, control_id -> [control_id, sample_id, bam, bai] }
                 .combine(control_bams, by: 0)
                 .map { control_id, sample_id, treat_bam, treat_bai, ctrl_bam, ctrl_bai ->
                     [[sample_id, treat_bam, treat_bai], [control_id, ctrl_bam, ctrl_bai]]
                 }

             MACS2_CALLPEAK(
                 paired_ch.map { it[0] },
                 paired_ch.map { it[1] }
             )
             FILTER_BLACKLIST(MACS2_CALLPEAK.out.peaks, blacklist_ch)
             BIGWIG(FILTER_DEDUP.out.bam)

             ch_multiqc = FASTP.out.json.collect()
             MULTIQC(ch_multiqc)
         }

See Also
--------

* :doc:`snakemake` -- Snakemake workflow manager overview
* :doc:`nextflow` -- Nextflow DSL2 workflow manager overview
* :doc:`atacseq` -- ATAC-seq workflow (related chromatin profiling assay)
* :doc:`/tools/alignment/bowtie2` -- Bowtie2 aligner reference
* :doc:`/tools/epigenomics/index` -- Epigenomics tools
