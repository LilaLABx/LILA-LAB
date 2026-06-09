# Dataset Card — BENI v1.0: Bangla Economic Narrative Index

## Dataset Description

**BENI** is a daily narrative index measuring the proportion of economic news in Bangla-language online news media from July 1, 2020 to June 30, 2021. It is constructed from the Potrika corpus (≈7.5M articles, 2013–2023) filtered to 2020–2021 (≈1.5M articles), classified using a TF-IDF + Logistic Regression model trained on 3,200 human-annotated sentences with active learning.

- **Homepage**: [OSF Project](https://osf.io/[project-id])
- **Repository**: [GitHub](https://github.com/nabil0x/economic-narrative-indices)
- **DOI**: `10.5281/zenodo.20585401`
- **License**: CC BY 4.0 (data), MIT (code)
- **Contact**: Ann Naser Nabil (ann.n.nabil@gmail.com)

## Dataset Composition

### Primary Files

| File | Format | Rows | Description |
|------|--------|------|-------------|
| `narrative_index_full.csv` | CSV | 365 | Daily index values (2020-07-01 to 2021-06-30) |
| `beni_v1_reference_labels_frozen.jsonl` | JSONL | 3,200 | Human-annotated gold-standard labels |
| `beni_v1_baseline_results.csv` | CSV | ~50 | Model performance metrics by k-label count |
| `beni_v1_llm_assisted_labels.jsonl` | JSONL | 300 | LLM-generated labels (3 models × 2 templates) |
| `beni_v1_active_learning_curves.csv` | CSV | ~200 | F1 across active learning rounds |
| `beni_v1_systematic_review_database.csv` | CSV | ~500 | Paper 2 screening database |

### Index File Schema (`narrative_index_full.csv`)

| Column | Type | Description |
|--------|------|-------------|
| `date` | date (ISO 8601) | Calendar date |
| `economic_article_count` | int | Number of articles classified as economic |
| `non_economic_article_count` | int | Number of articles classified as non-economic |
| `total_classified` | int | Total articles classified on that date |
| `economic_proportion` | float | Proportion classified as economic (0–1) |
| `rolling_7d_mean` | float | 7-day centered rolling average |
| `rolling_30d_mean` | float | 30-day centered rolling average |
| `economic_shares_index` | float | Normalized index (mean = 100) |

## Collection Methodology

### Source
- **Corpus**: Potrika Bangla News Corpus (10.17632/v362rp78dc.4)
- **Date range**: July 2020 – June 2021 (filtered from 2013–2023)
- **Filters**: Articles with 50+ words, non-empty headline, valid date

### Annotation
- **Human annotation**: 3 Bangladeshi annotators (native Bangla), pairwise annotation of 1,200 sentences
- **LLM annotation**: 300 articles annotated by 3 LLMs (Sonnet, Haiku, GPT-4o) with 2 prompt templates → majority-vote
- **Active learning**: K-label exploration from k=500 to k=3000, uncertainty sampling

### Classification Model
- **Architecture**: TF-IDF (unigrams + bigrams) → Logistic Regression (L2, C=1.0)
- **Training set**: 3,200 labeled sentences
- **Test set**: 800 held-out sentences
- **Accuracy**: 88.2% | **F1 (macro)**: 0.871
- **Software**: Python + scikit-learn

## Usage

### Loading the index
```python
import pandas as pd
df = pd.read_csv("narrative_index_full.csv", parse_dates=["date"])
df.head()
```

### Loading reference labels
```python
import json
labels = [json.loads(line) for line in open("beni_v1_reference_labels_frozen.jsonl")]
```

### Loading with Hugging Face Datasets (after upload)
```python
from datasets import load_dataset
ds = load_dataset("nabil0x/beni-narrative-index", split="train")
```

## Limitations & Biases

1. **Temporal coverage**: COVID-era data only (2020–2021). Patterns may differ in non-crisis periods.
2. **Source bias**: Only online news portals; excludes print, TV, radio, social media.
3. **Classification granularity**: Binary (economic/non-economic) only — no sectoral or sentiment breakdown.
4. **Language**: Standard Bangla; excludes English code-switching common in Bangladeshi media.
5. **Annotation quality**: Active learning labels are single-annotator after k=200.
6. **Model size**: TF-IDF + LogReg captures bag-of-words signals but misses context (no transformer embeddings in final model).

## Citation

```bibtex
@data{nabil2025beni,
  author = {Nabil, Ann Naser},
  title = {BENI v1.0: Bangla Economic Narrative Index — Dataset and Pipeline},
  publisher = {Zenodo},
  year = {2025},
  doi = {10.5281/zenodo.20585401},
  url = {https://github.com/nabil0x/economic-narrative-indices}
}
```

## Related Datasets

| Dataset | DOI | Relation |
|---------|-----|----------|
| Potrika Bangla News Corpus | 10.17632/v362rp78dc.4 | Source corpus |
| BENI v2.0 (planned) | — | Extended index with LLM extraction (Paper 6) |

## Keywords
`Bangla`, `economic narrative`, `NLP`, `text classification`, `text as data`, `nowcasting`, `Bangladesh`, `BENI`, `active learning`, `low-resource`
