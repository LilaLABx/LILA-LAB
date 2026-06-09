# BENI v1.0 File Schema

This document defines the target schema for the final canonical BENI release.

## Target Article-Level File

Recommended filename:

- `data/processed/beni_v1_articles.csv`

Required fields:

| Field | Type | Description |
|---|---|---|
| `article_id` | string | Stable BENI article identifier. |
| `upstream_source` | string | Upstream dataset name, usually `potrika`. |
| `source_file` | string | Raw file from which the article was loaded. |
| `newspaper` | string | Newspaper/source name parsed from file or metadata. |
| `publication_date` | date | Article publication date in ISO format. |
| `year_month` | string | Monthly period, `YYYY-MM`. |
| `category` | string | Original category label. |
| `headline` | string | Article headline/title. |
| `text` | string | Original article text where redistribution is allowed. |
| `text_clean` | string | Normalized text used for modeling. |
| `language` | string | `bn`, `en`, or mixed if detected. |
| `split` | string | `train`, `validation`, `test`, or `index_only`. |
| `economic_label_source` | string | `category`, `keyword`, `llm_reference`, `human_review`, or `model_prediction`. |
| `economic_relevance` | int | Binary label when available: 1 economic, 0 not economic. |
| `economic_probability` | float | Model probability for economic relevance. |
| `economic_prediction` | int | Binary model prediction. |
| `model_version` | string | Model used to create the prediction. |
| `duplicate_group_id` | string | Optional duplicate cluster identifier. |
| `release_version` | string | `BENI_v1.0`. |

## Target Annotation File

Recommended filename:

- `data/processed/beni_v1_reference_labels.jsonl`

Required fields:

| Field | Type | Description |
|---|---|---|
| `article_id` | string | Must match article-level file. |
| `economic_relevance` | string | `Economic` or `Not Economic`. |
| `confidence` | int | 1, 2, or 3. |
| `difficulty` | string | `Clear-cut`, `Borderline`, or blank if not applicable. |
| `requires_review` | bool | True for low-confidence or disagreement cases. |
| `review_status` | string | `pending`, `reviewed`, or `not_required`. |
| `final_label_source` | string | `llm_reference`, `human_review`, or `adjudicated`. |

Optional future fields:

- `economic_topic`
- `sentiment`
- `narrative_force`
- `valuation_target`

## Target Monthly Index File

Recommended filename:

- `data/processed/beni_v1_monthly_index.csv`

Required fields:

| Field | Type | Description |
|---|---|---|
| `year_month` | string | Month, `YYYY-MM`. |
| `n_articles` | int | Number of valid articles in month. |
| `n_economic` | int | Number classified as economic. |
| `economic_share` | float | `n_economic / n_articles`. |
| `mean_economic_probability` | float | Mean model probability. |
| `index_version` | string | `BENI_v1.0`. |
| `model_version` | string | Model used for the index. |

Optional sub-index fields:

- `inflation_share`
- `exchange_rate_share`
- `banking_share`
- `fiscal_policy_share`
- `trade_share`
- `employment_share`

