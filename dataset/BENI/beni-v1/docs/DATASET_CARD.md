# Dataset Card: BENI v1.0

## Dataset Name

BENI v1.0: Bangla Economic Narrative Index Dataset

## Dataset Type

Derived data-and-measurement release.

BENI v1.0 is not a replacement for the original Potrika corpus. It is a curated research dataset and measurement layer built from Potrika news data, LLM-assisted annotations, model predictions, and macroeconomic validation series.

## Intended Use

BENI v1.0 is intended for:

- economic text classification in Bangla,
- local-language narrative measurement,
- construction of monthly economic narrative indices,
- validation of text-based economic indicators against macroeconomic series,
- low-resource NLP benchmarking in an applied economics setting.

## Not Intended For

BENI v1.0 should not be used as:

- a complete archive of Bangladeshi media,
- a causal estimate of news effects on the economy,
- a human gold-standard annotation benchmark unless human adjudication is completed,
- a real-time policy tool without additional validation.

## Upstream News Data

Source: Potrika Bangla News Corpus  
DOI: `10.17632/v362rp78dc.4`  
License: CC BY 4.0  
Period: 2014-2020  
Original coverage: 664,880 articles from six Bangla newspapers.

Local path:

- `data/raw/potrika/`

## Macro Data

Local path:

- `data/raw/macro/`

Current files:

- `cpi_imf_bgd_index_monthly.csv`
- `fx_bdt_usd_bis_eop_monthly.csv`
- `fx_bdt_usd_imf_eop_monthly.csv`
- `reserves_wb_annual.csv`

## Annotation Data

Local path:

- `data/annotations/`

Current files:

- `llm_assisted_300_annotations.jsonl`
- `llm_assisted_300_summary.json`
- `beni_v0_1_annotations_locked.jsonl`
- `beni_v0_1_review_queue.csv`
- `model_comparison.json`
- `active_learning_results.json`

Current annotation framing:

- LLM-assisted reference labels.
- Not independent human gold labels.
- Human or expert review is still required before using "adjudicated" language.

## Known Limitations

- The review queue is not fully resolved.
- The current index output is a prototype and must be regenerated from the final canonical article file.
- Existing model outputs include TF-IDF results; BanglaBERT should be treated as exploratory unless rerun and documented.
- Source and date parsing must be verified before paper submission.

## Recommended Citation Language

Use:

> We use the Potrika Bangla News Corpus as the upstream news source and release BENI v1.0 as a derived economic narrative measurement dataset, including article-level processing metadata, LLM-assisted reference labels, classifier outputs, and monthly index values.

Avoid:

> We created the Potrika corpus.

