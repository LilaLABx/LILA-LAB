# LILA Lab Datasets

## Data Overview

This directory contains all datasets used and produced by LILA Lab pipelines, along with distribution manifests for multi-platform release.

### 10-Language Collection Progress

Our target is **10 emerging-economy low-resource languages** with baseline news corpora by H1 2027. [View the full plan →](../technical-reports/extensions/INDEX.md)

| # | Language | Pipeline | Region | Target Corpus | Status | Lead |
|---|----------|----------|--------|--------------|--------|--------|------|
| 1 | Bangla (বাংলা) | BENI | South Asia | ✅ 664k articles | ✅ Active | LILA Lab |
| 2 | Assamese (অসমীয়া) | AENI | South Asia | 🎯 100k+ (10+ yrs) | 🔜 Seeking | — |
| 3 | Nepali (नेपाली) | NENI | South Asia | 🎯 100k+ (10+ yrs) | 🔜 Seeking | — |
| 4 | Sylheti (চিটাঙ্গ) | SENI | South Asia | 🎯 Max viable (limited sources) | 🔜 Feasibility | — |
| 5 | Chittagonian (চাঁটগাঁইয়া) | CENI | South Asia | 🎯 Max viable (limited sources) | 🔜 Feasibility | — |
| 6 | Hausa | HENI | Africa | 🎯 100k+ (10+ yrs) | 🔜 Seeking | — |
| 7 | Kiswahili (Swahili) | KIENI | Africa | 🎯 100k+ (10+ yrs) | 🔜 Seeking | — |
| 8 | Vietnamese (Tiếng Việt) | VIENI | SE Asia | 🎯 100k+ (10+ yrs) | 🔜 Seeking | — |
| 9 | Tagalog (Filipino) | TIENI | SE Asia | 🎯 100k+ (10+ yrs) | 🔜 Seeking | — |
| 10 | Indonesian (Bahasa Indonesia) | IDENI | SE Asia | 🎯 100k+ (10+ yrs) | 🔜 Seeking | — |

**Progress:** 1 / 10 datasets collected. [Contribute a corpus →](../docs/LINGUISTIC_CONTRIBUTION_GUIDE.md)

### Available Datasets

| Dataset | Language | Size | License | Status |
|---------|----------|------|---------|--------|
| **BENI v1** | Bangla | — | CC BY 4.0 | ✅ Released |
| Potrika Corpus | Bangla | 3.3 GB | CC BY 4.0 | ✅ Available |
| BNLP Resources | Bangla | 56 MB | CC BY-NC-SA 4.0 | ✅ Available |

### Directory Structure

```
data/
├── beni-v1/              # BENI v1 dataset release
│   ├── README.md         # Dataset documentation
│   ├── CITATION.cff      # Citation metadata
│   └── ...               # Dataset files
│
├── raw/                  # Raw upstream data
│   ├── potrika/          # Potrika Bangla News Corpus
│   └── bnlp/             # BNLP resources
│
├── processed/            # Processed datasets
│   ├── annotations/      # Human annotations
│   └── indices/          # Narrative indices
│
├── OSF_UPLOAD_MANIFEST.md
├── ZENODO_UPLOAD_MANIFEST.md
├── HUGGINGFACE.md
├── MENDELEY_UPLOAD.md
└── DATASET_CARD.md
```

### BENI v1 Dataset

The BENI v1 dataset contains:

- 664,000+ Bangla news articles
- 3,200 human-annotated labels (gold standard)
- Monthly narrative indices (2014–2020)
- Macroeconomic indicators (CPI, FX, reserves)

**Citation:**
```
Nabil, A. N. (2026). LILA-BENI v1.0: A Harmonised Bangla News Dataset 
for Economic Narrative Measurement. Zenodo. 
https://doi.org/10.5281/zenodo.20585401
```

### Contributing Data

We accept contributions of:

1. **Text corpora** — News articles, social media, any text in your language
2. **Annotations** — Economic/Not Economic labels with cultural context
3. **Dialectal variants** — Chittagonian, Sylheti, Rangpuri, etc.

See `../docs/LINGUISTIC_CONTRIBUTION_GUIDE.md` for submission guidelines.

### Distribution Platforms

| Platform | Role | URL |
|----------|------|-----|
| **OSF** | Discovery + preprint hub | osf.io/ |
| **Zenodo** | Permanent DOI | doi.org/10.5281/zenodo.20585401 |
| **Hugging Face** | NLP community | huggingface.co/nabil0x |
| **Mendeley Data** | Raw corpus | data.mendeley.com/datasets/v362rp78dc |

### Distribution Manifests

| File | Platform | Purpose |
|------|----------|---------|
| `OSF_UPLOAD_MANIFEST.md` | OSF | Project hub, preprints, protocols |
| `ZENODO_UPLOAD_MANIFEST.md` | Zenodo | Dataset DOI + code release archive |
| `HUGGINGFACE.md` | Hugging Face | Models, datasets, Gradio demo |
| `MENDELEY_UPLOAD.md` | Mendeley Data | Raw Potrika corpus distribution |
| `DATASET_CARD.md` | All platforms | Standardised dataset metadata card |

### Citation Funnel

```
pipelines/[x]eni/ ──→ data/ ──→ OSF / Zenodo / Hugging Face / Mendeley
                              │
                              ▼
                        Citation Funnel
                      (../communications/DISTRIBUTION_STRATEGY.md)
```

The manifests reference content from:
- `pipelines/beni/` — trained models, code
- `data/beni-v1/` — canonical data files, annotation sets, BENI index
- `technical-reports/` — preprints, manuscripts
