# LILA Lab Datasets

**Target:** 10 emerging-economy low-resource languages with baseline news corpora by H1 2027.

Each pipeline has a dedicated dataset directory with `raw/` and `processed/` subdirectories. Public releases must follow [`../docs/DATA_RELEASE_CHECKLIST.md`](../docs/DATA_RELEASE_CHECKLIST.md).

---

## Collection Progress

| # | Language | Pipeline | Region | Target Corpus | Status | Dataset Directory |
|---|----------|----------|--------|--------------|--------|-------------------|
| 1 | Bangla (বাংলা) | **BENI** | South Asia | ✅ 664k articles | ✅ Active | [`BENI/`](./BENI/) |
| 2 | Assamese (অসমীয়া) | **AENI** | South Asia | 🎯 100k+ (10+ yrs) | 🔜 Seeking | [`AENI/`](./AENI/) |
| 3 | Nepali (नेपाली) | **NENI** | South Asia | 🎯 100k+ (10+ yrs) | 🔜 Seeking | [`NENI/`](./NENI/) |
| 4 | Sylheti (চিটাঙ্গ) | **SENI** | South Asia | 🎯 Max viable | 🔜 Feasibility | [`SENI/`](./SENI/) |
| 5 | Chittagonian (চাঁটগাঁইয়া) | **CENI** | South Asia | 🎯 Max viable | 🔜 Feasibility | [`CENI/`](./CENI/) |
| 6 | Hausa | **HENI** | Africa | 🎯 100k+ (10+ yrs) | 🔜 Planned | [`HENI/`](./HENI/) |
| 7 | Kiswahili (Swahili) | **KIENI** | Africa | 🎯 100k+ (10+ yrs) | 🔜 Planned | [`KIENI/`](./KIENI/) |
| 8 | Vietnamese (Tiếng Việt) | **VIENI** | SE Asia | 🎯 100k+ (10+ yrs) | 🔜 Planned | [`VIENI/`](./VIENI/) |
| 9 | Tagalog (Filipino) | **TIENI** | SE Asia | 🎯 100k+ (10+ yrs) | 🔜 Planned | [`TIENI/`](./TIENI/) |
| 10 | Indonesian (Bahasa Indonesia) | **IDENI** | SE Asia | 🎯 100k+ (10+ yrs) | 🔜 Planned | [`IDENI/`](./IDENI/) |

**Progress:** 1 / 10 datasets collected. [Contribute a corpus →](../docs/LINGUISTIC_CONTRIBUTION_GUIDE.md)

---

## Dataset Directory Structure

```
dataset/
├── BENI/              # Bangla — ✅ Complete dataset (beni-v1, raw, processed, manifests)
├── AENI/              # Assamese — 🔜 Ready for contributions
├── NENI/              # Nepali — 🔜 Ready for contributions
├── SENI/              # Sylheti — 🔜 Feasibility stage
├── CENI/              # Chittagonian — 🔜 Feasibility stage
├── HENI/              # Hausa — 🔜 Ready for contributions
├── KIENI/             # Kiswahili — 🔜 Ready for contributions
├── VIENI/             # Vietnamese — 🔜 Ready for contributions
├── TIENI/             # Tagalog — 🔜 Ready for contributions
├── IDENI/             # Indonesian — 🔜 Ready for contributions
└── README.md          # ← You are here
```

Each pipeline dataset folder follows a common layout:

```
[pipeline]/
├── raw/               # Raw upstream data (scraped articles, corpora)
├── processed/         # Cleaned, deduplicated, annotated data
│   ├── annotations/   # Human/LLM-assigned labels
│   └── indices/       # Narrative index output
└── README.md          # Language-specific details + contribution guide
```

The **BENI** folder is the reference implementation — it includes a full dataset release (`beni-v1/`), distribution manifests (OSF, Zenodo, Hugging Face, Mendeley), and a dataset card.

---

## How to Contribute

1. Pick a language from the table above
2. Go to its dataset directory and read the `README.md`
3. Collect raw news articles and place them in `raw/`
4. Process, annotate, and build indices following the [pipeline docs](../pipelines/README.md)
5. Open a PR with your dataset

See the [Linguistic Contribution Guide](../docs/LINGUISTIC_CONTRIBUTION_GUIDE.md) for full instructions.

Released datasets need a dataset card, license statement, provenance notes, limitations/bias notes, contributor credit, and distribution manifest when a DOI or external platform record exists.

---

## License

- **Code:** MIT License — Use, modify, distribute freely
- **Data:** CC BY 4.0 — Attribute the source
- **Papers:** © Authors — Cite properly
