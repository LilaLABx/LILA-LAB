# Distribution — Multi-Platform Release Manifests

> This folder contains the platform-specific upload manifests, dataset cards, and distribution templates for the BENI research program's multi-platform citation funnel.

---

## Contents

| File | Platform | Purpose |
|------|----------|---------|
| `OSF_UPLOAD_MANIFEST.md` | [OSF](https://osf.io/) | Open Science Framework — project hub, preprints, protocols |
| `ZENODO_UPLOAD_MANIFEST.md` | [Zenodo](https://zenodo.org/) | Dataset DOI + code release archive |
| `HUGGINGFACE.md` | [Hugging Face](https://huggingface.co/) | Models, datasets, Gradio demo |
| `MENDELEY_UPLOAD.md` | [Mendeley Data](https://data.mendeley.com/) | Raw Potrika corpus distribution |
| `DATASET_CARD.md` | All platforms | Standardised dataset metadata card |

---

## Dependency Graph

```
data-paper/data/ ──canonical datasets──┐
                                       ├──▶ distribution/*.md (manifests)
beni/ ──code + models──────┘                │
                                            ▼
                                  OSF / Zenodo / Hugging Face / Mendeley
                                            │
                                            ▼
                                      Citation Funnel
                                    (DISTRIBUTION_STRATEGY.md)
```

The manifests reference content from:
- `data-paper/` — canonical data files, annotation sets, BENI index
- `beni/` — trained models, code
- `papers/` — preprints, manuscripts

---

## The Distribution Strategy

The full strategy is documented in `/DISTRIBUTION_STRATEGY.md` at the project root. In brief:

| Platform | Role | Content |
|----------|------|---------|
| **OSF** | Discovery + preprint hub | Project page, preprints, protocols, supplementary materials |
| **Zenodo** | Permanent DOI for datasets | BENI v1 data release, code archives |
| **Hugging Face** | NLP community discovery | BanglaBERT models, BENI dataset, Gradio demo |
| **Mendeley Data** | Upstream corpus | Raw Potrika corpus (original source) |
| **GitHub** | Code of record | Full repository, issue tracking, version control |

---

## For Research Agents

- These manifests are **distribution instructions**, not automated scripts. Each platform has its own upload workflow.
- Before uploading, verify that the files referenced in each manifest exist at the expected paths.
- Update version numbers across all manifests simultaneously to keep them consistent.
- The `DISTRIBUTION_STRATEGY.md` at root level contains the strategic rationale and citation funnel design.
