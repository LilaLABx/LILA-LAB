# OSF Upload Manifest — LILA Lab

## Project Structure

```
Bangla Economic Narrative Indices (BENI)
├── OSF Project ID: [TBD on creation]
├── License: CC BY 4.0
├── Description: "Measuring economic narratives in Bangla news media.
│   A 6-paper research program on low-resource economic measurement."
│
├── [Component] Paper 1: Statistical Economics of Narrative
│   ├── paper1_statistical_economics_submitted.pdf
│   └── paper1_statistical_economics.tex
│
├── [Component] Paper 2: A Systematic Review of Economic Narrative Indices
│   ├── paper2_systematic_review_FORMATTED_2026-06-06.pdf
│   ├── paper2_systematic_review.tex
│   └── paper2_systematic_review_figures.zip
│       ├── figure_1_prisma_flow.png
│       ├── figure_2_timeline_trends.png
│       ├── figure_3_geographic_map.png
│       ├── figure_4_methods_matrix.png
│       └── figure_5_correlation_heatmap.png
│
├── [Component] Paper 3: BENI — Bangla Economic Narrative Index
│   ├── paper3_beni_pipeline_preprint.pdf
│   ├── paper3_beni_pipeline.tex
│   └── paper3_supplementary.pdf
│       └── (active learning curves, model comparisons, annotation stats)
│
├── [Component] Paper 4: Nowcasting with BENI
│   ├── paper4_beni_nowcasting_preprint.pdf
│   ├── paper4_beni_nowcasting.tex
│   └── paper4_supplementary.pdf
│       └── (VAR diagnostics, robustness checks, DM test details)
│
├── [Component] Paper 5: Text as Data — Survey of 110-Year ENI Evolution
│   ├── paper5_text_as_data_survey_preprint.pdf
│   ├── paper5_text_as_data_survey.tex
│   └── paper5_supplementary.pdf
│       └── (screening PRISMA checklist, included studies table)
│
├── [Component] Paper 6: LLM-Assisted Narrative Extraction
│   ├── paper6_llm_narrative_extraction_preprint.pdf
│   ├── paper6_llm_narrative_extraction.tex
│   └── paper6_supplementary.pdf
│       └── (prompt templates, inter-annotator agreement, extraction schemas)
│
├── [Component] BENI v1.0 — Data Paper
│   ├── beni_v1_data_paper_preprint.pdf
│   ├── beni_v1_data_paper.tex
│   ├── supplementary_materials.pdf
│   └── data_supplement/
│       ├── DATASET_CARD.md
│       ├── FILE_SCHEMA.md
│       ├── narrative_index_full.csv
│       └── beni_v1_reference_labels_frozen.jsonl
│
├── [Top-Level Files]
│   ├── README.md
│   ├── CITATION.cff
│   ├── LICENSE (CC BY 4.0)
│   └── FUNDING.md
│
├── [Resource: Figures]
│   Contains ALL publication figures from all 6 papers
│   ├── figure_1_6paper_dag.png
│   ├── figure_2_citation_funnel.png
│   └── [paper-specific figures in separate subdirectories]
│
├── [Resource: Protocols]
│   ├── annotation_schema.md
│   ├── annotation_guidelines.md
│   ├── adjudication_protocol.md
│   └── active_learning_sampling_strategy.md
│
└── Links
    ├── GitHub: https://github.com/LilaLABx/LILA-LAB
    ├── Zenodo: https://doi.org/10.5281/zenodo.20585401
    ├── Hugging Face: https://huggingface.co/nabil0x
    └── Mendeley Data: https://data.mendeley.com/datasets/v362rp78dc/4
```

---

## Upload Instructions

### Step 1: Create OSF Account
1. Go to https://osf.io/login/
2. Register or log in
3. Verify email

### Step 2: Create Project
1. Click "Create" → "Create project"
2. Title: `Bangla Economic Narrative Indices (BENI)`
3. Description: (paste from above)
4. License: Creative Commons Attribution 4.0 International (CC BY 4.0)
5. Make public

### Step 3: Add Components
For each component:
1. Click "Add Component"
2. Name as listed above
3. Category: "Project Component"
4. Description: Brief 1-2 line summary of each paper

### Step 4: Upload Files
- Files up to 5GB each on OSF
- Use OSF Storage (free, unlimited within reason)
- Upload PDFs + source TeX files
- Zip supplementary folders for clean upload

### Step 5: Add Links
1. Edit project page
2. Add links to GitHub, Zenodo, Hugging Face, Mendeley in the "Links" section

### Step 6: Mint OSF DOI
1. Go to Project Settings
2. Click "Create DOI" under "Identifiers"
3. Test the DOI resolves correctly

---

## File Source Mapping

| OSF File | Source Path (this repo) |
|----------|------------------------|
| Paper 3 preprint PDF | `technical-reports/paper3_beni_pipeline/manuscript/paper3_preprint.pdf` |
| Paper 3 figures | `technical-reports/paper3_beni_pipeline/figures/*.png` |
| Paper 4 preprint PDF | `technical-reports/paper4_beni_nowcasting/manuscript/paper4_preprint.pdf` |
| Paper 4 figures | `technical-reports/paper4_beni_nowcasting/figures/*.png` |
| Paper 5 preprint PDF | `technical-reports/paper5_text_as_data_survey/manuscript/paper5_preprint.pdf` |
| Paper 5 figures | `technical-reports/paper5_text_as_data_survey/figures/*.png` |
| Paper 6 preprint PDF | `technical-reports/paper6_llm_narrative_extraction/manuscript/paper6_preprint.pdf` |
| Annotation schema | `beni/annotation/annotation_schema.md` |
| Annotation guidelines | `beni/annotation/annotation_guidelines.pdf` |
| Adjudication protocol | `beni/annotation/adjudication_protocol.md` |
| Dataset card | `releases/DATASET_CARD.md` |
| FILE_SCHEMA.md | `beni/index/FILE_SCHEMA.md` (verify path) |
| CITATION.cff | `CITATION.cff` (repo root) |

---

## Metadata Tags (for OSF discoverability)
```
Bangla, NLP, economic narrative, text as data, nowcasting, Bangladesh,
active learning, LLM annotation, systematic review, BENI, natural language
processing, computational social science, low-resource language
```
