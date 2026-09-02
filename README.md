# SeqTec Version 2

SeqTec is the source repository for *The Complete Guide to Next-Generation
Sequencing* and its companion bioinformatics website. Version 2 is undergoing a
source-grounded, chapter-by-chapter review inspired by the verification process
used for [WatchGen](https://github.com/kevinkorfmann/watchgen).

The book covers sequencing chemistry, current platforms, library preparation,
genomics, transcriptomics, epigenomics, multiomics, experimental design, data
standards, practical protocols, and executable analysis workflows. The companion
Sphinx site provides tool-focused commands and workflow examples.

## Verification standard

A chapter is not called verified merely because it reads plausibly or compiles.
Review requires checking scientific claims against primary literature, standards
against their issuing organizations, and time-sensitive specifications against
current official documentation. Calculations receive independent dimensional or
analytic checks. Published commands must be syntax-checked or executed on a small
public fixture where feasible. The book and website must then build without
warnings, and the rendered PDF must be inspected.

Progress, evidence, corrections, and unresolved limitations are recorded in
[`VERIFICATION.md`](VERIFICATION.md). Until that ledger marks a
chapter `VERIFIED`, treat it as a draft under review.

## Version 2 progress

**Overall completion: approximately 15% (as of 2026-09-01).** This is a
conservative editorial estimate, not the percentage of sentences sampled. No
chapter is counted as finished until it clears every gate in
[`VERIFICATION.md`](VERIFICATION.md); currently **0 of 26 chapters are fully
verified**.

Completed so far:

- Established the chapter ledger, evidence rules, source-integrity tests, and
  continuous book/website builds.
- Added an initial 33-item DOI-verified primary bibliography and a verification
  anchor to every chapter.
- Corrected confirmed cross-cutting errors in platform throughput, genome
  coverage arithmetic, pricing language, policy scope, terminology, and
  cross-references.
- Removed committed generated files and repaired the largest PDF defects:
  oversized floats, unbreakable listings and protocol boxes, broken references,
  glossary generation, and several unreadable tables.
- Confirmed that source integrity, DOI retrieval, tests, strict website build,
  and the 647-page book build pass locally.

Still required for Version 2:

- Complete the claim-by-claim primary-source audit for all 26 chapters and
  record evidence for every material correction.
- Pin and execute the published Snakemake, Nextflow, shell, Python, and R
  examples against small public fixtures where feasible.
- Reconcile the companion website with the book and run external-link checking.
- Finish current vendor, kit, policy, software-version, protocol, biosafety, and
  jurisdiction-specific checks.
- Correct remaining dense or overfull horizontal layouts, then visually inspect
  the complete book and website.
- Obtain specialist review for wet-lab, clinical, legal/privacy, and biosafety
  material before calling those sections authoritative.

## Build and test

```bash
make setup
make verify
make test
make docs
make book
```

The final PDF is written to `output/pdf/seqtec_v2.pdf`. The website is written to
`docs/_build/html/`.

## Important scope note

This is an educational reference. It is not a validated clinical pipeline,
manufacturer protocol, biosafety authorization, or legal opinion. Always use the
protocol revision matching the exact reagent kit and software release in your
laboratory, and validate regulated workflows locally.

## Author

Kevin Korfmann
