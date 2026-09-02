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
