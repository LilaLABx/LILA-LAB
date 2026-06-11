# LILA Lab — CLI Tool

**Self-service pipeline bootstrap and project management.**

The LILA CLI (`lila`) will let contributors bootstrap new pipelines, validate datasets, and publish indices — all from the command line. This directory is a **planning stub**.

## Target Commands

```bash
lila init --language yoruba --region africa
    → Creates pipelines/YORUBANI/ from template
    → Creates dataset/YORUBANI/ with raw/processed/external
    → Generates README with language-specific info

lila validate --pipeline YORUBANI
    → Validates pipeline structure against template
    → Checks annotation schemas, directory layout, configs

lila publish --pipeline YORUBANI --platform zenodo
    → Zips and uploads dataset to Zenodo
    → Generates DATASET_CARD.md
    → Updates registry/languages.json

lila status
    → Shows all pipelines with their current status
    → Reads from registry/languages.json

lila list
    → Lists all supported languages and their pipeline status
```

## Implementation Plan

| Component | Status |
|-----------|--------|
| CLI scaffold (click/typer) | 📋 Planned |
| `lila init` command | 📋 Planned |
| `lila validate` command | 📋 Planned |
| `lila publish` command | 🔜 Future |
| `lila status` command | 🔜 Future |

## Related

- `pipelines/template/` — The bootstrap source for `lila init`
- `registry/languages.json` — Source of truth for `lila status`
- `pipelines/shared/` — Shared utilities the CLI will import
