# Technical Reports — LILA Lab Paper Series

This directory documents the paper series produced by LILA Lab. Each paper directory contains the manuscript, figures, data references, and replication code where available.

---

## Paper Series

| Paper | Title | Status | Location |
|-------|-------|--------|----------|
| 1 | Systematic Review of Economic Narrative Indices | Complete (submitted) | `paper1_systematic_review/` |
| 2 | BENI v1 Dataset (Potrika corpus + LLM labels) | Complete (OSF preprint) | `dataset/BENI/beni-v1/` |
| 3 | Nowcasting Inflation with a TF-IDF Narrative Index | Active | `paper3_tfidf_nowcasting/` |
| 4 | Nowcasting Inflation with BENI | 📋 Planned (Aug 2026) | `paper4_nowcasting_inflation/` |
| 5 | Text as Data in Social Science | 📋 Planned (Oct 2026) | `paper5_text_as_data/` |
| 6 | LLMs as Measurement Devices | 💡 Proposed (Jan 2027) | `paper6_llm_measurement/` |

### Paper 1 — Systematic Review of Economic Narrative Indices
Systematic literature review of 66 papers (2007–2025) mapping dictionary-based, supervised ML, and LLM-based approaches to economic narrative index construction. Includes a BENI pilot (TF-IDF classifier at 91.7%, 79-month index, macro correlations). Identifies severe publication bias (88% positive), geographic bias (84% English, 56% US, 0% Bangla), and a pooled median RMSE improvement of 3.76%.

### Paper 2 — BENI v1 Dataset
Describes the release of the BENI v1 dataset: 933K Bangla news articles (Potrika corpus) with LLM-annotated economic narrative labels. Dataset available on Mendeley Data, Zenodo, and OSF. The actual paper manuscript lives at `dataset/BENI/beni-v1/osf_upload_package/paper/main.tex`.

### Paper 3 — Nowcasting Inflation with a TF-IDF Narrative Index
Evaluates whether a simple TF-IDF narrative index from Bangla news contains predictive content for CPI inflation. Key findings: cointegration with macro variables (1 CV at all lags), CPI Granger-causes narrative (p=0.01), out-of-sample VAR beats random walk by 20.9% (DM p=0.0004).

### Paper 4 — Nowcasting Inflation with BENI (Planned)
*Manuscript forthcoming.* Directory placeholder for the BENI nowcasting paper.

### Paper 5 — Text as Data in Social Science (Planned)
*Manuscript forthcoming.* Directory placeholder for the text-as-data methodology paper.

### Paper 6 — LLMs as Measurement Devices (Proposed)
*Proposal stage.* Directory placeholder for the LLM measurement paper.

---

## Directory Structure

```
technical-reports/
├── README.md                         # This file
├── extensions/                       # Language and domain extension proposals
│   ├── INDEX.md                      # Registry of active extensions
│   ├── EXTENSION_TEMPLATE.md         # Template for proposing a new extension
│   └── REPLICATION_TEMPLATE.md       # Template for replication reports
├── contributions/                    # Contribution tracking
│   └── OWNERS.csv                    # Who owns what
├── paper1_systematic_review/         # Paper 1 — Systematic review manuscript
├── paper2_beni_dataset/              # Paper 2 — Reference to BENI v1 dataset paper
└── paper3_tfidf_nowcasting/          # Paper 3 — TF-IDF nowcasting analysis
```

---

## Using These Reports

- **Researchers**: Each paper directory contains the manuscript, figures, data references, and replication code. For the full methodology framework these papers build on, see [`docs/research/NARRATIVE_EXTRACTION_METHODOLOGIES.md`](../docs/research/NARRATIVE_EXTRACTION_METHODOLOGIES.md) (12-level hierarchy).
- **Contributors**: See [extensions/INDEX.md](extensions/INDEX.md) for active extension opportunities, and [contributions/OWNERS.csv](contributions/OWNERS.csv) to record your participation.
- **Reviewers**: Replication reports can be submitted using the [REPLICATION_TEMPLATE.md](extensions/REPLICATION_TEMPLATE.md).

## Related Resources

- [Methodology Hierarchy](../docs/research/NARRATIVE_EXTRACTION_METHODOLOGIES.md) — narrative extraction methods from manual coding to agentic systems
- [Methodology Level Index](../docs/research/methodologies/INDEX.md) — detailed deep-dives into each of the 12 levels
- [BENI Pilot Run Manifest](../docs/research/BENI_PILOT_RUN_MANIFEST.md) — experimental results from the Bangla pilot
- [Documentation Portal](../docs/index.md) — all LILA Lab docs organized by role

---

## Citation

For the overall project:

```bibtex
@software{lila_lab,
  author = {Nabil, Ann Naser and others},
  title = {LILA Lab: Language Intelligence for Low-resource Applications},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/LilaLABx/LILA-LAB}
}
```

Individual paper citations are available in each paper's directory.
