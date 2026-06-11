# BENI v1.0 Processing Plan

This is the required processing path for turning the current workspace into a paper-ready dataset release.

## Step 1: Freeze Scope

Decision:

- Use Potrika as the upstream news corpus.
- Use 2014-2020 as the main time window.
- Use Economy as positive source category.
- Use National, Politics, and World News as negative/comparison categories.

Do not mix this release with the separate `Bangla_News_Database` JSONL collection unless a later BENI v2 release explicitly expands sources.

## Step 2: Build Canonical Article File

Create:

- `data/processed/beni_v1_articles.csv`

Requirements:

- stable `article_id`,
- parsed `publication_date`,
- parsed `newspaper`,
- original `category`,
- normalized text,
- documented train/validation/test split,
- model output fields.

## Step 3: Resolve Annotation Queue

Input:

- `data/annotations/beni_v0_1_review_queue.csv`

Output:

- `data/processed/beni_v1_reference_labels.jsonl`

Rules:

- Keep "LLM-assisted reference labels" unless human review is actually completed.
- If manual review is completed, mark reviewed cases as `human_review`.
- Do not use "gold standard" unless independent adjudication is documented.

## Step 4: Train or Lock Model

Minimum:

- TF-IDF + Logistic Regression as the main reproducible baseline.

Optional:

- BanglaBERT if training is rerun and evaluation is stable.

Final output:

- `data/models/beni_v1_tfidf_logreg.joblib`
- model card in `docs/MODEL_CARD.md`

## Step 5: Rebuild Index

Create:

- `data/processed/beni_v1_monthly_index.csv`

The paper should use only this regenerated file, not older prototype index outputs.

## Step 6: Validate

Create:

- `data/processed/beni_v1_macro_validation.csv`

Minimum tests:

- level correlations,
- first-difference correlations,
- clearly reported sample size,
- macro data source documentation.

## Step 7: Update Manuscript

The paper must match:

- final article counts,
- final date range,
- final model metrics,
- final annotation counts,
- final index sample size,
- final validation results.

## Submission Gate

The dataset is ready for paper submission only when:

- no unresolved review queue remains,
- one canonical article file exists,
- one canonical reference-label file exists,
- one canonical monthly index exists,
- paper tables are regenerated from those files,
- the README and dataset card match the final files.

