# [X]ENI Pipeline Template

> Use this template to bootstrap a new XENI pipeline for your language.

## Quick Start

```bash
# Copy the template
cp -r pipelines/template/ pipelines/[your-lang]/
cd pipelines/[your-lang]/

# Rename everything
# Replace [x]eni with your pipeline name (e.g., BENI, HENI, AENI)
# Replace [Language] with your language name
```

## Template Structure

```
[x]eni/
├── README.md                    # ← You are here
├── annotation/                  # LLM annotation pipeline (domain-agnostic)
│   ├── README.md                # Instructions + deliverables
│   ├── schemas/                 # Per-domain annotation schemas
│   │   ├── README.md            # How to create schemas
│   │   ├── economic.json        # Example: economic narrative schema
│   │   └── health.json          # Example: health discourse schema
│   ├── llm_annotate.py          # Multi-LLM annotation script
│   └── adjudicate.py            # Disagreement resolution
├── indices/                     # Index construction — one per domain
│   ├── README.md                # How indices work
│   ├── eco/                     # Economic narrative index
│   │   ├── README.md
│   │   ├── build_index.py
│   │   └── validate.py
│   └── health/                  # Health discourse index
│       ├── README.md
│       ├── build_index.py
│       └── validate.py
├── experiment/                  # Model training & evaluation
│   ├── README.md
│   ├── train.py
│   └── evaluate.py
├── database/                    # Data storage (SQLite, etc.)
│   └── README.md
└── data/                        # Raw & processed data
    └── README.md
```

## Next Steps After Copying

1. **Edit this README** — Replace `[x]eni` and `[Language]` with your details
2. **Define schemas** — Create domain schemas in `annotation/schemas/`
3. **Collect data** — Place raw news data in `data/`
4. **Run annotation** — Implement `llm_annotate.py` for your language
5. **Build indices** — Implement index construction for each domain
6. **Train models** — Run experiments in `experiment/`
7. **Publish** — Write up results and submit

## Deliverable

A complete, reproducible XENI pipeline for your language producing validated narrative indices across one or more domains.
