# LILA Lab — CLI Tool

**Self-service pipeline bootstrap and project management.**

The LILA CLI (`lila`) gives contributors a self-service way to inspect pipeline status and validate repository metadata. Bootstrap and publishing commands remain planned.

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
| CLI scaffold | ✅ Implemented |
| `lila init` command | 📋 Planned |
| `lila validate` command | ✅ Implemented |
| `lila publish` command | 🔜 Future |
| `lila status` command | ✅ Implemented |

## Current Commands

```bash
python -m cli status
python -m cli validate
```

## Related

- `pipelines/template/` — The bootstrap source for `lila init`
- `registry/languages.json` — Source of truth for `lila status`
- `pipelines/shared/` — Shared utilities the CLI will import
