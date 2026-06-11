# CENI — Chittagonian (চাঁটগাঁইয়া) Dataset

**Pipeline:** [CENI](../../pipelines/ceni/) | **Status:** 🔜 Feasibility study | **Target:** Max viable corpus (limited sources)

## Directory Structure

```
CENI/
├── raw/            # Raw Chittagonian news articles (place scraped data here)
│   ├── .gitkeep
├── processed/      # Cleaned, deduplicated, annotated data
│   ├── annotations/ # Human/LLM-assigned labels
│   └── indices/     # Narrative index output
└── README.md       # ← You are here
```

## Background

Chittagonian is a minority language spoken by ~16M people, primarily in the Chittagong region of Bangladesh. Digital news presence is limited — feasibility work is needed to identify viable sources.

## How to Contribute

1. **Survey sources** — Identify any online Chittagonian-language news/media
2. **Collect samples** — Even small corpora help assess feasibility
3. **Place raw data** → `raw/`
4. **Report findings** — Open an issue documenting source landscape

See [Linguistic Contribution Guide](../../docs/LINGUISTIC_CONTRIBUTION_GUIDE.md) for details.

## License

- **Data:** CC BY 4.0 — Attribute the source
- **Code:** MIT License
