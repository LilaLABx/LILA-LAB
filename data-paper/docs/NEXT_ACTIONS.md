# Next Actions

## Priority 1: Make the Dataset Canonical

Create:

- `data/processed/beni_v1_articles.csv`
- `data/processed/beni_v1_reference_labels.jsonl`
- `data/processed/beni_v1_monthly_index.csv`

## Priority 2: Review Labels

Open:

- `data/annotations/beni_v0_1_review_queue.csv`

Decide each case:

- keep LLM label,
- revise after human review,
- mark ambiguous and exclude from clean validation.

## Priority 3: Regenerate Tables

All paper tables should be generated from files inside `BENI_v1_data_paper`.

Minimum tables:

- data coverage by source/category/year,
- annotation label counts,
- model comparison,
- monthly index summary,
- macro validation results.

## Priority 4: Align Manuscript

Update the second paper so that every number in the abstract, data section, methods, and results comes from the final BENI v1.0 release.

