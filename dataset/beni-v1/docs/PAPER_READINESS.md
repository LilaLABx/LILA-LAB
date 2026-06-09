# Paper Readiness Declaration

## Current Decision

BENI v1.0 is being refined as a **data-and-measurement paper**.

It should not be submitted yet as a pure data paper because the release still needs a canonical processed dataset, resolved annotation queue, and regenerated final index.

## What Is Ready

- Upstream Potrika data are present locally.
- Macro data are present locally.
- LLM-assisted 300-article annotation files are present.
- A TF-IDF model artifact is present.
- Prototype index outputs are present.
- The existing draft manuscript can be adapted.

## What Is Not Ready

- The release does not yet have a canonical `BENI_v1.0` article-level file.
- The 115-row review queue still needs a decision.
- The prototype index should be regenerated from the final canonical file.
- The manuscript must be updated to match final files exactly.
- BanglaBERT should not be treated as a successful production model unless rerun and documented.

## Recommended Target Paper Claim

Use:

> This paper introduces BENI v1.0, a reproducible derived data release and measurement pipeline that transforms the Potrika Bangla news corpus into an economic narrative index for Bangladesh.

Avoid:

> This paper introduces a new raw Bangla news corpus.

## Readiness Rating

Current readiness:

- Dataset organization: high.
- Raw data availability: high.
- Annotation documentation: medium.
- Canonical release file: low.
- Paper-table reproducibility: medium-low.
- Submission readiness: not yet.

Next milestone:

> Produce `data/processed/beni_v1_articles.csv`, `data/processed/beni_v1_reference_labels.jsonl`, and `data/processed/beni_v1_monthly_index.csv`.

