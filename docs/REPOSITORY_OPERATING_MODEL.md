# Repository Operating Model

This repository is the public operating system for LILA Lab: research code, dataset metadata, release records, contribution rules, and public documentation for low-resource-language linguistic exploration.

## Source of Truth Map

| Area | Owns | Must not contain | Source of truth |
| --- | --- | --- | --- |
| `pipelines/` | XENI pipeline code, schemas, configs, small examples | raw corpora, model weights, private credentials | `registry/languages.json`, `registry/xeni_pipeline_contract.json` |
| `dataset/` | dataset cards, release notes, raw/processed directory placeholders | unpublished private corpora, local scratch files | `dataset/README.md`, per-language `DATASET_CARD.md` |
| `technical-reports/` | papers, extension templates, replication templates, contributor records | generated build artifacts as canonical records | `technical-reports/README.md`, `technical-reports/contributions/OWNERS.csv` |
| `registry/` | machine-readable language and schema metadata | prose-only status claims | `registry/languages.json`, `registry/schemas.json` |
| `dist/` | external platform manifests, DOI records, publication metadata | dataset payloads | `dist/manifests/` |
| `docs/` | public docs, governance, release checklists, GitHub Pages content | local secrets or raw data | `docs/README.md` |
| `infrastructure/` | deployment helpers, scripts, website and bot source when public | live `.env` files or private deployments | `infrastructure/README.md` |
| `communications/` | brand, content, community coordination | pipeline status or release metadata | `communications/COMMUNICATIONS.md` |
| `api/` | future API specification and implementation | source-of-truth metadata duplicated from registry | `api/README.md` |
| `cli/` | self-service status and validation commands | research business logic or scraped data | `cli/README.md` |
| `tests/` | repository-level validation tests | production pipeline logic | `pyproject.toml`, `tests/conftest.py` |
| `.github/` | CI, issue templates, pull request templates | local credentials or release payloads | `.github/workflows/` |
| `.vscode/` | editor recommendations for contributors | required runtime configuration | `.vscode/` |
| `.playwright-mcp/` | local/browser automation support files when tracked | product source-of-truth claims | `.playwright-mcp/` |
| `.omo/` | agent plans, evidence, execution ledgers | product source code | `.omo/plans/` |

## Pipeline Maturity Levels

| Status | Meaning | Required proof |
| --- | --- | --- |
| `bootstrapped` | Template structure exists and passes contract validation | `python -m cli validate` |
| `feasibility` | Source landscape is being assessed | source survey or README notes |
| `planned` | Target language is approved but not yet collecting data | registry row and dataset placeholder |
| `active` | Code, dataset, validation, and public docs exist | dataset card, schema, run manifest, validation outputs |

Do not describe a pipeline as active unless `registry/languages.json` says it is active and the release/readiness artifacts exist.

## Data and Release Rules

- Raw and processed corpora stay out of Git unless they are small metadata examples.
- Public releases need a dataset card, license statement, DOI/platform manifest when available, provenance notes, limitations, and contributor credit.
- `dist/` tracks manifests and external identifiers, not large payloads.
- Ignored local files such as `.env`, `__pycache__`, PDFs, zips, model weights, and `personal/` are not lab source-of-truth artifacts.

## Quality Gates

- Local and CI checks must use the same enforced scope.
- BENI legacy code can remain advisory while shared/template/CLI validation hardens.
- Schema validation checks actual `annotation/schemas/*.json` files.
- Contributor-facing changes should include command evidence in `.omo/evidence/` when executed by an agent.

## Maintenance Rule

When adding a new top-level directory or new public status claim, update this operating model, `docs/README.md`, and the relevant registry or checklist in the same change.
