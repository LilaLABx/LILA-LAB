# BENI v1.0 Data Paper Workspace

> **Title**: BENI v1.0: A Potrika-derived Bangla economic narrative corpus, annotation set, and monthly index for Bangladesh macroeconomic monitoring.
>
> **Status**: 📋 Not submission-ready yet, but structured for refinement
>
> **Former path**: `BENI_v1_data_paper/` (renamed for clarity)

This workspace separates the BENI v1 **data release** from the exploratory code and prototype outputs in `beni/`. The paper should claim only what can be reproduced from this folder.

---

## Directory Layout

```
dataset/
│
├── 📁 data/
│   ├── 📁 raw/potrika/         ← Potrika raw Bangla news CSV files
│   ├── 📁 raw/macro/           ← Macroeconomic indicators (CPI, FX, reserves)
│   ├── 📁 annotations/         ← Locked LLM-assisted labels, review queue
│   ├── 📁 index/               ← Prototype monthly BENI index & predictions
│   ├── 📁 processed/           ← Canonical processed datasets
│   └── 📁 models/              ← TF-IDF model artifact
│
├── 📁 paper/
│   ├── 📁 beni_data_paper/     ← Data paper manuscript (LaTeX)
│   └── 📎 paper3_beni_pipeline/ ← symlink → ../../technical-reports/paper3_beni_method/...
│
├── 📁 scripts/                 ← Build & validation scripts
├── 📁 docs/                    ← Schema docs, release manifests, data card
├── 📁 osf_upload_package/      ← OSF-ready release bundle
│
├── 📋 OSF_PREPRINT_UPLOAD.md   ← OSF preprint upload instructions
├── 📋 osf_main.pdf             ← OSF preprint PDF
├── 📋 CITATION.cff             ← Data citation metadata
├── 📋 CODE_LICENSE.md          ← Code license
├── 📋 DATA_LICENSE.md          ← Data license
│
├── 📦 BENI_v1_data_release.zip      ← Canonical data release bundle
├── 📦 BENI_v1_data_paper_osf_upload_package.zip
└── 📦 BENI_v1_data_paper_viable_upload.zip
```

---

## Derivative Map

| Content | Source | Notes |
|---------|--------|-------|
| `data/raw/potrika/` | Upstream Potrika corpus | Original source data |
| `data/raw/macro/` | IMF CPI, BIS FX | Downloaded independently |
| `data/annotations/` | `beni/annotation/` pipeline | Locked and reviewed labels |
| `data/index/` | `beni/experiment/outputs/index/` | Prototype index files |
| `data/models/` | `beni/experiment/models/` | Trained classifier |
| `paper/beni_data_paper/` | Independent | Standalone data paper manuscript |
| `paper/paper3_beni_pipeline` (symlink) | `technical-reports/paper3_beni_method/manuscript/paper3_beni_pipeline/` | Canonical Paper 3 manuscript |
| `osf_upload_package/` | Derived from `data/` + `docs/` | OSF-ready distribution |

---

## Relationship to Other Folders

| Folder | Relationship |
|--------|-------------|
| `beni/` | **Upstream** — `dataset/` contains canonical snapshots of `beni/` outputs |
| `technical-reports/paper3_beni_method/` | **Peer** — Paper 3's `data/processed/` symlinks here |
| `releases/` | **Downstream** — Distribution manifests reference this folder's content |
| `technical-reports/paper3_beni_pipeline/` (symlink) | **Reference** — Links to the Paper 3 manuscript that uses this data |

---

## Paper Framing

This is a **data-and-measurement paper**, not a plain data paper.

> We introduce BENI v1.0, a reproducible derived dataset and measurement pipeline that transforms an existing Bangla news corpus into an economic narrative index.

**Do not** claim that BENI creates the Potrika corpus. Potrika is the upstream source. BENI contributes the curated economic measurement layer: labels, processing choices, model predictions, index construction, validation files, and documentation.

---

## Required Before Submission

- [ ] Resolve the 115-row review queue in `data/annotations/beni_v0_1_review_queue.csv`
- [ ] Generate one canonical article-level dataset with stable IDs
- [ ] Ensure dates and source fields parse correctly
- [ ] Rebuild the monthly index from the final article-level file
- [ ] Rerun macro validation
- [ ] Update the manuscript to match the final release exactly

