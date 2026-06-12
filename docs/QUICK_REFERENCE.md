# LILA Lab — Quick Reference Card

> **One-page cheat sheet.** For detailed docs, see [`docs/index.md`](index.md).

---

## Directory Structure

```
./
├── pipelines/    → XENI language pipelines (BENI, AENI, ..., template/)
├── dataset/      → Raw corpora + processed releases per language
├── registry/     → Central metadata (languages, schemas, publications)
├── technical-reports/ → Paper series + extension templates
├── docs/         → Website + guides + methodology research
├── communications/ → Brand, content, community strategy
├── infrastructure/ → Discord bot, website, scripts
├── api/          → REST API (planned)
├── cli/          → CLI tools (planned)
├── dist/         → Distribution manifests (Zenodo, HuggingFace, OSF)
├── tests/        → Shared test infrastructure
└── .github/      → CI workflows, issue templates
```

---

## Common Commands

| Command | When | What it does |
|---------|------|-------------|
| `pip install -e ".[core]"` | First setup | Install core dependencies |
| `pip install -e ".[all]"` | Full setup | Install everything |
| `python -m cli validate` | Before commit | Validate pipeline structure & schemas |
| `python infrastructure/scripts/validate_schemas.py` | Schema change | Validate annotation schemas |
| `ruff check pipelines/shared/` | Lint check | Python linting (ruff) |
| `pytest --tb=short -q` | Test run | Run all tests |
| `make audit` | Full audit | Run all validation steps |

---

## Key Terms

| Term | Meaning |
|------|---------|
| **XENI** | Framework: **[Language initial]** + **E**xploration & **N**ative-language **I**ntelligence |
| **BENI** | Bangla pipeline (B + ENI) — first and reference implementation |
| **Narrative Index** | Monthly time series of narrative prevalence in news, validated against macro indicators |
| **BENI Economic Index** | 79-month Bangla economic narrative index (proven, 91.7% accuracy) |
| **AENI/NENI/SENI/...** | Other pipelines: Assamese, Nepali, Sylheti, Chittagonian, Hausa, Kiswahili, Vietnamese, Tagalog, Indonesian |
| **LLM Annotation** | Multi-LLM ensemble annotation (Claude, GPT-4o, Gemini) with adjudication |
| **CENI** | Chittagonian pipeline (not to be confused with "Central" — it's Chittagonian) |

---

## Where to Find Things

| You Need | Go Here |
|----------|---------|
| Pipeline code & structure | [`pipelines/`](../pipelines/README.md) |
| Datasets & collection progress | [`dataset/`](../dataset/README.md) |
| Published papers | [`technical-reports/`](../technical-reports/README.md) |
| Methodology (12 levels) | [`docs/research/`](../docs/research/NARRATIVE_EXTRACTION_METHODOLOGIES.md) |
| Methodology level index | [`docs/research/methodologies/INDEX.md`](../docs/research/methodologies/INDEX.md) |
| Reproducibility run manifest | [`docs/research/RUN_MANIFEST_TEMPLATE.md`](../docs/research/RUN_MANIFEST_TEMPLATE.md) |
| Data release checklist | [`docs/DATA_RELEASE_CHECKLIST.md`](../docs/DATA_RELEASE_CHECKLIST.md) |
| Architectural decisions | [`docs/adr/`](../docs/adr/README.md) |
| Repository governance | [`docs/REPOSITORY_OPERATING_MODEL.md`](../docs/REPOSITORY_OPERATING_MODEL.md) |
| Collaboration & authorship | [`docs/COLLABORATION.md`](../docs/COLLABORATION.md) |
| Linguistic contribution guide | [`docs/LINGUISTIC_CONTRIBUTION_GUIDE.md`](../docs/LINGUISTIC_CONTRIBUTION_GUIDE.md) |
| Glossary | [`docs/GLOSSARY.md`](../docs/GLOSSARY.md) |
| FAQ | [`docs/FAQ.md`](../docs/FAQ.md) |
| Roadmap | [`docs/ROADMAP.md`](../docs/ROADMAP.md) |
| Website (GitHub Pages) | [`docs/WEBSITE.md`](../docs/WEBSITE.md) |

---

## Reproducibility (BENI Baseline)

```bash
cd pipelines/BENI/experiment/beni_pilot
python3 train.py --task economic --model-type tfidf --data-source potrika-timeseries
python3 build_index.py
python3 correlate.py
```

---

## Quick Links

- **Discord:** discord.gg/TrrdKbky
- **Email:** lila.lab0x@gmail.com
- **Website:** lilalab.pro.bd
- **Citation:** See [`technical-reports/README.md`](../technical-reports/README.md#citation)

---

*Last updated: 2026-06-12*
