# BENI Unified Corpus Merge Plan

## Objective

Create one harmonised BENI corpus by combining:

1. **Potrika dated raw files** for 2014-2020.
2. **BNAD post-2020 JSONL files** for 2021-2024.

Working dataset name:

> BENI Unified Corpus v1.0

Recommended paper language:

> We construct a harmonised Bangla economic news panel by combining Potrika's dated 2014-2020 newspaper files with post-2020 BNAD articles, retaining source provenance to test robustness against corpus-source changes.

## Merge Decision

Use this merge rule:

| Period | Source | Use |
|---|---|---|
| 2014-2020 | Potrika dated raw newspaper/category files | Main baseline |
| 2021-2024 | BNAD JSONL files | Main extension |
| 2014-2020 | BNAD JSONL files | Robustness only, not default merge |
| Undated Potrika balanced files | Potrika `*_40k.csv` files | Model training only, not time-series index |

Reason:

- Potrika and BNAD overlap heavily before 2021, but their source composition and scraping structure differ.
- Using Potrika before 2021 and BNAD after 2020 avoids unnecessary duplication and creates the cleanest long panel.
- BNAD pre-2021 can be used later for source-break robustness checks.

## Candidate Coverage

From the schema audit:

- Potrika dated rows: 472,464 from 2014-2020.
- BNAD post-2020 rows: 1,009,119 from 2021-2024.
- Combined pre-deduplication candidate panel: 1,481,583 dated articles.

Expected usable sample will be smaller after:

- category filtering,
- empty-text removal,
- duplicate removal,
- source-break checks.

## Canonical Unified Schema

Create:

- `data/processed/beni_unified_articles.csv`

Required fields:

| Field | Description |
|---|---|
| `article_id` | Stable ID, e.g. `potrika_000000001` or `bnad_000000001`. |
| `dataset_source` | `potrika` or `bnad`. |
| `source_file` | Original filename. |
| `newspaper` | Newspaper/source name. |
| `publication_date` | ISO date. |
| `year_month` | `YYYY-MM`. |
| `category_original` | Original source category. |
| `category_harmonised` | BENI category mapping. |
| `headline` | Title/headline. |
| `text` | Article body. |
| `text_clean` | Normalized body text. |
| `tags` | Optional tags, mainly from BNAD. |
| `meta` | Optional meta field, mainly from BNAD. |
| `language` | Default `bn`, with optional mixed-language flag later. |
| `text_hash` | Hash of normalized text. |
| `headline_date_hash` | Hash for headline/date deduplication. |
| `is_duplicate` | Boolean duplicate flag. |
| `duplicate_group_id` | Duplicate cluster ID. |
| `economic_seed_label` | Label from source category or keyword rule. |
| `economic_probability` | Model probability after scoring. |
| `economic_prediction` | Binary model prediction after scoring. |
| `model_version` | Model used for prediction. |
| `release_version` | `BENI_unified_v1.0`. |

## Category Harmonisation

Initial target categories:

- `economy`
- `national`
- `politics`
- `international`
- `sports`
- `education`
- `entertainment`
- `technology_science`
- `health`
- `other_or_unknown`

Economic relevance should not rely only on `category_harmonised == economy`.

Use a two-stage label:

1. Source-category seed:
   - economy/business/finance categories are positive.
   - clearly sports/entertainment/lifestyle categories are negative.
   - national/politics/international are ambiguous.
2. Economic relevance model:
   - score all articles using BENI classifier.
   - use model probability for index construction.

## Deduplication Plan

Run deduplication in this order:

1. Remove empty or extremely short text.
2. Exact duplicate on `text_hash`.
3. Same-day near duplicate using `headline_date_hash`.
4. Cross-source duplicate check for high-volume syndicated stories.

Keep duplicate metadata instead of deleting blindly:

- mark `is_duplicate`,
- assign `duplicate_group_id`,
- keep one canonical article per group for index construction,
- preserve source count for source-bias analysis if needed.

## Index Construction Plan

Build three monthly indices:

1. `BENI_potrika_only_2014_2020`
2. `BENI_bnad_only_2021_2024`
3. `BENI_unified_2014_2024`

For the unified index, report a source-break diagnostic at 2020/2021:

- article volume jump,
- source composition change,
- category composition change,
- mean economic probability shift,
- economic share shift.

Do not make strong claims from the unified trend unless the source-break test is acceptable.

## Robustness Checks

Required:

- Compare Potrika 2014-2020 and BNAD 2014-2020 overlapping years as a bridge sample.
- Compare economy-category-only index versus model-probability index.
- Compare raw article-weighted index versus source-balanced index.
- Check whether the 2021 jump is caused by dataset change rather than economic narratives.

## Paper Strategy

For Paper 2:

- Use Potrika-only BENI as the clean baseline.
- Present BNAD merge as an extension that enables later nowcasting.
- Include unified corpus construction if the source-break diagnostics are acceptable.

For Paper 3/nowcasting:

- Use the unified 2014-2024 index only after robustness checks.
- If source-break is too large, use 2021-2024 BNAD-only models for post-2020 nowcasting and Potrika-only models as historical baseline.

## Implementation Steps

1. Add parsers:
   - `parse_potrika.py`
   - `parse_bnad.py`
2. Build canonical source-specific article files:
   - `data/processed/potrika_articles_canonical.csv`
   - `data/processed/bnad_articles_canonical.csv`
3. Filter:
   - Potrika: keep dated raw newspaper/category files, 2014-2020.
   - BNAD: keep parseable dates after 2020 for main extension.
4. Merge into:
   - `data/processed/beni_unified_articles.csv`
5. Deduplicate and write:
   - `data/processed/beni_unified_articles_deduped.csv`
6. Score economic relevance.
7. Build monthly indices.
8. Run source-break and macro-validation diagnostics.

