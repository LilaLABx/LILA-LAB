# Zenodo Upload Manifest — BENI v1.0

## Record Metadata

| Field | Value |
|-------|-------|
| **Title** | BENI v1.0: Bangla Economic Narrative Index — Dataset and Pipeline |
| **Authors** | Nabil, Ann Naser (Jahangirnagar University) |
| **Description** | Full reproducible pipeline for constructing the Bangla Economic Narrative Index (BENI). Includes the daily narrative index values (July 2020–June 2021), gold-standard human-annotated reference labels, active learning experiment outputs, and all Python scripts required to reproduce from raw Potrika corpus. |
| **License** | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| **Version** | v1.0.0 |
| **DOI** | `10.5281/zenodo.20585401` (already reserved) |
| **Keywords** | Bangla, economic narrative, NLP, text classification, active learning, Bangladesh, nowcasting, BENI |
| **Related identifiers** | Potrika corpus: 10.17632/v362rp78dc.4 (Mendeley Data) — this dataset is a derivative |
| **Notes** | This repository is archived from GitHub: https://github.com/nabil0x/economic-narrative-indices |

---

## File Inventory

### Essential Package (~100 MB compressed)

| File | Description | Size (approx) | Source Path |
|------|-------------|---------------|-------------|
| `beni_v1_narrative_index.csv` | Daily proportion of economic articles, Jul 2020–Jun 2021 | 50 KB | `beni/index/narrative_index.csv` |
| `beni_v1_reference_labels_frozen.jsonl` | Gold-standard human labels (3 annotators, adjudicated) | 200 KB | `beni/experiment/beni_pilot/data/combined_classification/beni_v1_reference_labels_frozen.jsonl` |
| `beni_v1_baseline_results.csv` | Model performance across active learning rounds | 100 KB | `beni/experiment/beni_pilot/results/` |
| `beni_v1_domain_barometer.csv` | Domain barometer scores per article | 1 MB | `beni/experiment/beni_pilot/` or `domain_barometer/` |
| `tfidf_vectorizer.joblib` | TF-IDF vectorizer (fit on Potrika corpus) | 5 MB | `beni/models/tfidf_vectorizer.joblib` |
| `economic_tfidf_logreg.joblib` | Best-performing TF-IDF + Logistic Regression | 10 MB | `beni/models/economic_tfidf_logreg.joblib` |
| `topic_tfidf_logreg.joblib` | Topic classifier model | 10 MB | `beni/models/topic_tfidf_logreg.joblib` |
| `annotation_schema.md` | The annotation schema document | 50 KB | `beni/annotation/annotation_schema.md` |
| `annotation_guidelines.pdf` | Annotator instruction guide | 500 KB | `beni/annotation/annotation_guidelines.pdf` |
| `adjudication_protocol.md` | Disagreement resolution protocol | 30 KB | `beni/annotation/adjudication_protocol.md` |

### Code Package (~5 MB compressed)

| File | Description |
|------|-------------|
| `scripts/` | All Python pipeline scripts (63 scripts, see below) |
| `requirements.txt` | Python dependencies with pinned versions |

### Supplementary (~50 MB compressed)

| File | Description |
|------|-------------|
| `beni_v1_active_learning_curves.csv` | F1 score across k-label exploration |
| `beni_v1_annotation_exports/` | Raw annotation exports from Label Studio / data labeling |
| `beni_v1_llm_assisted_labels.jsonl` | LLM-generated labels (300 articles, 3 models × 2 templates) |
| `beni_v1_systematic_review_database.csv` | Paper 2 systematic review screening database |

### Documentation

| File | Description |
|------|-------------|
| `README.md` | Dataset overview and usage |
| `CITATION.cff` | Citation metadata |
| `LICENSE` | CC BY 4.0 text |
| `DATASET_CARD.md` | Formal dataset card (Hugging Face style) |
| `FILE_SCHEMA.md` | Schema for every file in the dataset |
| `DISTRIBUTION_STRATEGY.md` | Multi-platform distribution plan |

---

## Core Scripts Inventory

These 63 scripts constitute the full reproducible pipeline. Include all in the code package:

### Data Collection
- `beni/database/0_download_potrika.ipynb`
- `beni/database/1_build_news_database.ipynb`
- `beni/database/2_feature_extraction.ipynb`
- `beni/database/3_daily_article_cleanup.ipynb`
- `beni/database/4_filtering_for_economic_annotation.ipynb`
- `beni/database/5_generate_candidate_pool.ipynb`

### Annotation
- `beni/annotation/0_prepare_annotation_data.ipynb`
- `beni/annotation/1_label_studio_sync.py`
- `beni/annotation/2_annotation_quality_report.ipynb`
- `beni/annotation/3_llm_annotation_pipeline.py`
- `beni/annotation/4_adjudicate_labels.ipynb`

### Active Learning
- `beni/experiment/beni_pilot/0_explore_active_learning.R`
- `beni/experiment/beni_pilot/1_run_k_label_experiment.R`
- `beni/experiment/beni_pilot/2_compare_model_configs.R`
- `beni/experiment/beni_pilot/3_analyze_learning_curves.R`
- `beni/experiment/beni_pilot/4_plot_figures.R`

### Index Construction
- `beni/index/0_construct_narrative_index.R`
- `beni/index/1_validate_index_properties.R`
- `beni/index/2_plot_index_timeseries.R`

### Domain Barometer
- `domain_barometer/main_experiment.py`
- `domain_barometer/analysis.py`
- `domain_barometer/visualization.py`

### Systematic Review (Paper 2)
- `paper2/fetch_crossref.py`
- `paper2/screen_abstracts.py`
- `paper2/extract_study_data.R`
- `paper2/meta_analysis.R`
- `paper2/visualize_results.R`

---

## Versioning Strategy

| Version | Contents | When |
|---------|----------|------|
| **v1.0.0** | BENI pipeline + index + gold-standard labels + active learning | Now (current) |
| **v1.1.0** | LLM-assisted annotations (300 articles, multi-model) | After Paper 3 submission |
| **v2.0.0** | Expanded index with Potrika v2 corpus (if updated) | Future |
| **v2.1.0** | Nowcasting replication data (Paper 4) | After Paper 4 acceptance |

---

## Upload Instructions

### Via Web Upload (Simplest for v1)
1. Go to https://zenodo.org/deposit/new
2. Fill in metadata using the table above
3. Upload files (drag & drop, up to 50GB per dataset)
4. Click "Publish"

### Via GitHub Integration (Recommended for future versions)
1. Go to https://zenodo.org/account/settings/github/
2. Link GitHub account
3. Enable `nabil0x/economic-narrative-indices`
4. (Next) Create a GitHub release → Zenodo auto-archives

### Zenodo-GitHub Integration Setup
```bash
# After enabling in Zenodo:
# 1. Create a GitHub release
git tag v1.0.0 -m "BENI v1.0 - Initial release"
git push origin v1.0.0

# 2. Zenodo automatically:
#    - Archives the repo at this tag
#    - Creates a DOI for this release
#    - Updates the badge in README
```

---

## DOI Check

```
Pre-existing DOI: 10.5281/zenodo.20585401

Action required:
1. Visit https://doi.org/10.5281/zenodo.20585401 — does it resolve?
2. If yes → use it as the BENI v1.0 DOI
3. If no → create new deposit at https://zenodo.org/deposit/new → mint new DOI → update CITATION.cff
```
