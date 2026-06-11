# Experiments

## Purpose

Train and evaluate classifiers on annotated data. The annotation pipeline produces gold-standard labels; this directory turns them into reproducible models.

## Structure

```
experiment/
├── README.md         # ← You are here
├── train.py          # Train classifiers (TF-IDF, BERT, etc.)
└── evaluate.py       # Evaluate and compare model performance
```

## Workflow

```
Locked reference set (from annotation/adjudicate.py)
    → train.py
    → Trained model artifacts
    → evaluate.py
    → Performance report + predictions → indices/
```

## Instructions

1. **Implement `train.py`** — Train classifiers on your language's annotated data
   - Start with TF-IDF + logistic regression (strong baseline, cheap)
   - Progress to multilingual BERT or your language's pretrained model
   - Document hyperparameters, train/val/test splits
2. **Implement `evaluate.py`** — Benchmark model performance
   - Report accuracy, precision, recall, F1 per category
   - Compare against BENI benchmarks (91.7% TF-IDF, 88.2% BanglaBERT)
   - Analyze failure modes and annotation disagreements
3. **Output predictions** — Save article-level predictions for index construction

## Deliverable

- Trained model artifacts (ready for inference)
- Evaluation report with per-category metrics
- Article-level predictions CSV (input to `indices/{domain}/build_index.py`)
