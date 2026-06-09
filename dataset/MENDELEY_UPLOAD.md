# Mendeley Data — Upload Manifest

## Current State

| Dataset | DOI | Status |
|---------|-----|--------|
| **Potrika Bangla News Corpus** | `10.17632/v362rp78dc.4` | ✅ Already published (CC BY 4.0) |
| **BENI narrative index** | *(new Mendeley deposit)* | ⬜ Not yet uploaded |

## Strategy

BENI data proper → **Zenodo** (DOI 10.5281/zenodo.20585401)

Mendeley is for **raw corpus data** that is too large for Zenodo (50GB cap):

- **Potrika corpus** → already on Mendeley. Cite it, don't duplicate.
- **Bangla_News_Database JSONLs** (9 files, 16 GB) → could be deposited as a supplement if Potrika authors agree
- **BENI v2 supplement** (future) → extended corpus for Papers 4/6

## Citation Entry

When citing Mendeley in BENI papers, use the existing Potrika DOI:

```bibtex
@misc{potrika2023,
  author = {Hasan, Md. Arid and others},
  title = {Potrika: Bangla News Corpus},
  publisher = {Mendeley Data},
  year = {2023},
  doi = {10.17632/v362rp78dc.4}
}
```

## If Creating a New Mendeley Deposit

| Field | Value |
|-------|-------|
| **Title** | BENI v1.0: Gold-Standard Economic Narrative Labels for Bangla News |
| **Authors** | Nabil, Ann Naser |
| **Description** | 3,200 human-annotated Bangla news sentences with economic/non-economic labels, used to train the Bangla Economic Narrative Index (BENI). |
| **Disciplines** | Economics, Library and Information Science, Computational Linguistics |
| **Keywords** | Bangla, economic narrative, NLP, annotation |
| **License** | CC BY 4.0 |
| **Related DOI** | 10.17632/v362rp78dc.4 (Potrika — this is a derivative) |
| **Files** | `beni_v1_reference_labels_frozen.jsonl` (200 KB) |
| **Version** | 1 |
