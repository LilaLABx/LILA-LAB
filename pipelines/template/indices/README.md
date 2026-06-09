# Narrative Indices

## Purpose

Transform annotated article labels into monthly narrative indices — one per domain. Each index tracks how the narrative in your language's news evolves over time.

## Structure

```
indices/
├── README.md          # ← You are here
├── eco/               # Economic narrative index
│   ├── README.md      # Domain-specific instructions
│   ├── build_index.py # Index construction
│   └── validate.py    # Validation against real-world data
└── health/            # Health discourse index
    ├── README.md
    ├── build_index.py
    └── validate.py
```

## How an Index Is Built

```
Annotated articles (from annotation pipeline)
    → Aggregate article labels by month
    → Score: mean probability / proportion per category
    → Normalize: source-weight, volume-adjust
    → Monthly index series (CSV)
    → Validate against real-world indicators
```

## Instructions

1. **Create a subdirectory per domain** — name must match `schemas/{domain}.json`
2. **Implement `build_index.py`** — aggregate article-level predictions into monthly time series
3. **Implement `validate.py`** — compare index against trusted real-world indicators
4. **Document methodology** — what aggregation, normalization, and validation choices were made

## Deliverable

- Per-domain monthly index CSV files (e.g., `eco_monthly_index.csv`)
- Validation reports showing correlation with real-world indicators
- Visualization-ready time series
