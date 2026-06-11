# BENI — Core Codebase & Data Infrastructure

> Core pipeline code: annotation, index construction, experiments, and macroeconomic data that underpin Papers 2–4.
> Raw corpus and dataset releases live in [`dataset/BENI/`](../../dataset/BENI/).

---

## Directory Structure

```
beni/
│
├── 📁 annotation/                ← LLM-assisted economic relevance annotation pipeline
│   ├── 📋 ANNOTATION_SCHEMA.md      12-field schema (topic, sentiment, frame, etc.)
│   ├── 📋 ANNOTATOR_GUIDE.md        Human annotator instructions
│   ├── 📋 ADJUDICATION_PROTOCOL.md  How to resolve annotation disagreements
│   ├── 🐍 llm_annotate.py           Core LLM annotation (Claude, GPT)
│   ├── 🐍 annotate_batch.py         Batch processing for large-scale annotation
│   ├── 🐍 multi_llm_ensemble.py     Multi-LLM ensemble voting
│   ├── 🐍 kaggle_3llm_ensemble.py   Kaggle-specific 3-LLM ensemble runner
│   ├── 🐍 analyze_llm_annotations.py  Annotation quality & cost analysis
│   ├── 🐍 ensemble_report.py        Ensemble consistency reports
│   ├── 🐍 build_annotation_batch.py  Construct annotation batches from corpus
│   ├── 🐍 export_for_labelstudio.py  Export to Label Studio format
│   ├── 🐍 create_llm_assisted_300.py Build 300-article LLM reference set
│   ├── 🐍 run_active_learning.py     Active learning loop
│   ├── 🐍 run_model_comparison.py    Compare classifier models
│   ├── 🐍 finetune_banglabert_for_prelabel.py  Fine-tune BanglaBERT
│   ├── 🐍 add_ml_predictions.py      Add model predictions to annotation set
│   ├── 🐍 adjudicate.py             Adjudication script
│   ├── 🐍 setup_project.py          Project setup
│   ├── 📋 label_config.xml          Label Studio config
│   ├── 📁 exports/                  Labeled data exports
│   ├── 📁 projects/                 Label Studio project files
│   ├── 📁 logs/                     Annotation run logs
│   └── 📁 __pycache__/
│
├── 📁 data/                      ← Macroeconomic data, experiment inputs
│
├── 📁 database/                  ← Database files (SQLite, etc.)
│
├── 📁 experiment/                ← Full experiment suite
│   ├── 📋 EXPERIMENT_REPORT.md       Consolidated experiment findings
│   ├── 📋 FINDINGS_ECONOMIC_TRENDS.md Economic trend analysis from narratives
│   ├── 📋 MODEL_COMPARISON.md        Model comparison results
│   ├── 📋 DATA_SOURCES.md            Data provenance
│   ├── 📋 BENI_NOVELTY_AGENDA.md     Novelty assessment
│   ├── 📋 NIETZSCHE_LANGUAGE_FRAMEWORK_FOR_BENI.md  Theoretical framing
│   ├── 📁 beni_pilot/                BENI pilot experiments
│   ├── 📁 bnlp-resources/            Bangla NLP resources
│   ├── 📁 data/                      Experiment-specific data splits
│   ├── 📁 models/                    Trained model artifacts (TF-IDF, logistic reg)
│   ├── 📁 scripts/                   Experiment scripts
│   └── 📁 outputs/                   Experiment outputs (predictions, indices)
│       ├── 📁 index/                  BENI narrative index CSV outputs
│       └── (other experiment outputs)
│
├── 📁 indices/                   ← Index construction (one per domain)
│   └── 📁 eco/                   ← BENI Economic Index
│       ├── 🐍 build_narrative_index.py   Main index builder
│       ├── 🐍 visualize.py               Index visualization
│       ├── 📁 outputs/                   Generated index CSV files
│       └── 📋 README.md
│
├── 📁 management/                ← Project management
│   ├── 📋 BENI_ROADMAP.md            BENI project roadmap
│   └── 📋 PROJECT_STATUS.md          Current project status
│
└── 📁 ...                        ← Cleaned pipeline code only
```

---

## Dependency Map — How beni/ Feeds Into Each Paper

```
beni/annotation/    ──LLM labels──▶  paper3_beni_method/ (trains classifier)
beni/indices/eco/   ──BENI index──▶  paper4_beni_nowcasting/ (nowcast input)
beni/data/          ──macro data──▶  paper3_beni_method/, paper4_beni_nowcasting/
beni/experiment/    ──results─────▶  paper3_beni_method/ (method validation)
dataset/BENI/raw/   ──corpus──────▶  annotation pipeline (upstream data)
technical-reports/  ──manuscripts─▶  papers (paper artifacts moved)
```

---

## Key Pipelines

### 1. Annotation Pipeline (`annotation/`)
```
Raw news articles
    → LLM annotate (llm_annotate.py)
    → Multi-LLM ensemble (multi_llm_ensemble.py)
    → Active learning (run_active_learning.py)
    → Model training (run_model_comparison.py)
    → Adjudication (adjudicate.py)
    → Locked reference set
```

### 2. Index Construction (`indices/eco/`)
```
Article-level predictions (from annotation pipeline or experiment/outputs/)
    → build_narrative_index.py
    → Monthly BENI index CSV
    → Macro validation against CPI, FX, reserves
```

### 3. Experiment Suite (`experiment/`)
Codes in `experiment/scripts/` run model comparisons, produce outputs in `experiment/outputs/`, and generate findings documented in `EXPERIMENT_REPORT.md`, `MODEL_COMPARISON.md`, etc.

---

## Notes for Research Agents

- **This is the upstream dependency** for Papers 2, 3, and 4. Changes to `beni/annotation/` or `beni/indices/eco/` propagate to those paper directories.
- `beni/experiment/outputs/` contains the raw prediction files that `paper3_beni_method/` references.
- The raw Bangla news corpus now lives in [`dataset/BENI/raw/bangla_news_database/`](../../dataset/BENI/raw/bangla_news_database/).
- Paper 2 manuscript and bibliography moved to [`technical-reports/paper2_systematic_review/`](../../technical-reports/paper2_systematic_review/).
- See [`dataset/BENI/`](../../dataset/BENI/) for dataset releases, manifests, and the dataset card.
