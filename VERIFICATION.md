# Verification ledger: SeqTec Version 2

Last reconciled: 2026-09-01  
Baseline: GitHub `main` at `9dc81e1`  
Edition: `2.0.0-dev`

This ledger records a source-grounded review campaign. It does not claim
independent domain-expert peer review. A chapter becomes `VERIFIED` only after its
claims, calculations, examples, cross-references, website counterparts, strict
build, and rendered pages have passed the gates below. A global disclaimer or a
passing self-referential test is not evidence for an individual claim.

## Status meanings

| Status | Meaning |
|---|---|
| `NOT STARTED` | No systematic Version 2 review has been completed. |
| `IN PROGRESS` | Claims and examples are actively being checked; do not cite the chapter as verified. |
| `FOLLOW-UP` | A review found unresolved or time-sensitive items that still need closure. |
| `VERIFIED` | Source audit and all validation gates passed, with evidence recorded here. |

## Verification gates

1. Separate durable scientific principles from version-, price-, policy-, and
   vendor-dependent statements.
2. Prefer primary papers, standards bodies, official software documentation, and
   current manufacturer specification sheets. Secondary summaries are discovery
   aids, not final authority.
3. Recalculate quantitative examples independently, including units and whether
   a platform reports reads, read pairs, clusters, bases, or output per flow cell
   versus per instrument run.
4. Run or syntax-check published commands and workflows using pinned versions and
   small public fixtures where licensing and compute permit.
5. Record limitations honestly. Clinical thresholds, kit volumes, legal rules,
   cloud prices, and performance benchmarks require context and an as-of date.
6. Pass `pytest`, the strict Sphinx build, the LaTeX build, link checks, and visual
   review of affected PDF pages.

## Chapter campaign

| # | Chapter | Status | Evidence / open work |
|---:|---|---|---|
| 1 | Introduction: The Sequencing Revolution | `IN PROGRESS` | Historical dates, cost claims, and platform landscape require primary-source audit. |
| 2 | Molecular Biology Essentials | `IN PROGRESS` | Definitions, numerical molecular claims, and central-dogma qualifications require audit. |
| 3 | Principles of Modern Sequencing | `IN PROGRESS` | Platform units and performance specifications contain dated or contradictory values. |
| 4 | Short-Read Sequencing Platforms | `IN PROGRESS` | Current vendor specifications and market-language claims require normalization. |
| 5 | Long-Read Sequencing Platforms | `IN PROGRESS` | Revio/Vega and ONT chemistry specifications require current official-source reconciliation. |
| 6 | Library Preparation | `IN PROGRESS` | Kit-specific instructions must be tied to exact protocol revisions. |
| 7 | Whole-Genome and Exome Sequencing | `IN PROGRESS` | Coverage guidance, capture-kit specifications, and workflow examples require audit. |
| 8 | Variant Discovery and Interpretation | `IN PROGRESS` | Caller scope, filtering advice, and clinical interpretation language require audit. |
| 9 | Metagenomics and Microbiome Sequencing | `IN PROGRESS` | Database/tool versions, compositional-data caveats, and MAG criteria require audit. |
| 10 | RNA Sequencing | `IN PROGRESS` | Statistical formulas, tool comparisons, and workflow code require audit. |
| 11 | Single-Cell RNA Sequencing | `IN PROGRESS` | Chemistry-specific cell-loading and sequencing guidance require revision-aware sourcing. |
| 12 | Spatial Transcriptomics | `IN PROGRESS` | Rapidly changing platform specifications and claimed nf-core support require audit. |
| 13 | DNA Methylation | `IN PROGRESS` | Assay chemistry, modification distinguishability, and workflows require audit. |
| 14 | Chromatin Accessibility | `IN PROGRESS` | Protocol/QC thresholds and computational examples require audit. |
| 15 | Histone Modifications | `IN PROGRESS` | Assay comparisons, controls, and peak-calling recommendations require audit. |
| 16 | The 3D Genome | `IN PROGRESS` | Duplicate label and oversized-table defect fixed; depth-to-resolution heuristics still require source audit. |
| 17 | Single-Cell and Spatial Multiomics | `IN PROGRESS` | Method capabilities and model equations require paper/source-code audit. |
| 18 | Specialized Sequencing Applications | `IN PROGRESS` | Clinical claims and emerging assay descriptions require audit. |
| 19 | Emerging Technologies and Future Directions | `IN PROGRESS` | Speculative/vendor claims must be clearly labelled and dated. |
| 20 | Bioinformatics Fundamentals | `IN PROGRESS` | File-format definitions, command syntax, and algorithm explanations require audit. |
| 21 | Complete Analysis Workflows | `IN PROGRESS` | Published Snakemake/Nextflow examples need executable fixtures and version pins. |
| 22 | Experimental Design and Best Practices | `IN PROGRESS` | Corrected a 10x NovaSeq pooling error; remaining universal thresholds and power formulas require audit. |
| 23 | Data Standards, Sharing, and Reproducibility | `IN PROGRESS` | NIH 2026 plan format, policy scope, privacy-law amounts, and cloud prices require updates. |
| 24 | Accessible Sequencing | `IN PROGRESS` | Prices, availability, legal scope, and biosafety guidance are jurisdiction- and date-sensitive. |
| 25 | Practical Protocols | `IN PROGRESS` | No wet-lab protocol will be verified without an exact official protocol revision and safety boundary. |
| 26 | DIY Analysis | `IN PROGRESS` | Accessions, downloads, commands, expected outputs, benchmarks, and cloud claims require execution. |

## Findings already confirmed

- The Version 1 repository tracked generated Sphinx and LaTeX artifacts. Version
  2 ignores them and rebuilds them in CI to prevent stale website/book output.
- The baseline website could not build in the ambient system Python because its
  declared Sphinx extensions were absent; the Version 2 build uses an isolated
  environment and CI-installed requirements.
- The baseline LaTeX log reported multiple floats hundreds to thousands of
  points taller than a page. Version 2 makes long listings and protocol boxes
  page-breakable and converts long tables to multipage structures; the current
  build has no oversized-float, overfull-vbox, missing-reference, or
  undefined-reference warnings.
- Chapter 16 defined `subsec:3dgenome:compartments` twice; Version 2 gives the
  analysis section a unique label.
- Chapter 22 treated roughly 30 million PE150 read pairs as sufficient for 30x
  coverage of a 3 Gb genome. The dimensional calculation is about 300 million
  pairs before overhead, reducing the theoretical 10B-flow-cell capacity from
  roughly 330 genomes to roughly 33. The correction uses Illumina's current
  NovaSeq X specification range rather than the flow-cell nickname as a guarantee.

## Primary current sources opened for the cross-cutting audit

- Illumina, *NovaSeq X Series Specification Sheet*, M-US-00197 v9.0:
  <https://supportassets.illumina.com/content/dam/illumina/gcs/assembled-assets/marketing-literature/novaseq-x-series-spec-sheet-m-us-00197/novaseq-x-series-specification-sheet-m-us-00197.pdf>
- PacBio, current sequencing-system specifications:
  <https://www.pacb.com/sequencing-systems/>
- 10x Genomics, Chromium Next GEM Single Cell 5' user guide CG000592:
  <https://cdn.10xgenomics.com/image/upload/v1670307213/support-documents/CG000592_ChromiumNextGEMSingleCell5_v2_BEAM_CellSurfaceProtein_UserGuide_Rev_A.pdf>
- NIH, 2026 Data Management and Sharing Plan guidance:
  <https://www.grants.nih.gov/policy-and-compliance/policy-topics/sharing-policies/dms/writing-dms-plan>
- GATK, official HaplotypeCaller overview:
  <https://gatk.broadinstitute.org/hc/en-us/articles/360035531412-HaplotypeCaller-in-a-nutshell>
- GA4GH, current standards and products:
  <https://www.ga4gh.org/our-products/>

## Release blockers

- No chapter is yet entitled to `VERIFIED` status.
- The new bibliography contains 33 DOI records whose first-author metadata is
  checked against Crossref, and every chapter has an initial primary-source
  anchor. This is scaffolding, not a completed claim-level citation audit.
- The website does not yet mirror the full book and its published commands have
  no executable fixture suite.
- Remaining overfull horizontal boxes and dense tables require page-by-page
  correction. The current 647-page draft is reviewable but not release-ready.
- Source integrity (26 chapters, 1,029 labels), DOI verification, pytest, strict
  Sphinx HTML, LaTeX, glossary, and bibliography builds pass. External link
  checking, executable workflow fixtures, and final full-book visual validation
  remain open.
