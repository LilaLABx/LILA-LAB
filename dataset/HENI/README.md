# HENI — Hausa Dataset

**Pipeline:** [HENI](../../pipelines/HENI/) | **Status:** 🔜 Planned scaffold | **Target:** 100k+ articles (10+ years)

## Directory Structure

```
HENI/
├── raw/            # Raw Hausa news articles (place scraped data here)
│   ├── .gitkeep
├── processed/      # Cleaned, deduplicated, annotated data
│   ├── annotations/ # Human/LLM-assigned labels
│   └── indices/     # Narrative index output
└── README.md       # ← You are here
```

## How to Contribute

1. **Identify sources** — Online Hausa news portals (e.g., BBC Hausa, VOA Hausa, Rahma, Aminiya)
2. **Scrape articles** — Collect 10+ years of news coverage
3. **Place raw data** → `raw/`
4. **Process & annotate** → follow the [shared pipeline docs](../../pipelines/README.md)
5. **Submit** — PR your dataset or open an issue to coordinate

See [Linguistic Contribution Guide](../../docs/LINGUISTIC_CONTRIBUTION_GUIDE.md) for details.

## License

- **Data:** CC BY 4.0 — Attribute the source
- **Code:** MIT License
