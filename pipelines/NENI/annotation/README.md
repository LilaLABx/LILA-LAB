# Annotation Pipeline

## Purpose

Convert raw native-language news articles into labeled training data using LLM ensembles. This is the core measurement layer — annotation quality determines everything downstream.

## How It Works

```
Raw news articles (from data/)
    → llm_annotate.py      (multi-LLM annotation with Claude, GPT-4o, local models)
    → adjudicate.py         (resolve disagreements between annotators/models)
    → Locked reference set  (gold-standard labels for training & evaluation)
```

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `schemas/` | Per-domain annotation schemas (JSON) defining categories and labels |

## Instructions

1. **Define your annotation schema(s)** in `schemas/` — one JSON file per domain
2. **Implement `llm_annotate.py`** — adapt the multi-LLM ensemble for your language
   - Configure API keys, model selection, prompt templates
   - Handle your language's script and tokenization
3. **Implement `adjudicate.py`** — resolve disagreements between models/annotators
   - Majority voting, confidence thresholding, or human review
4. **Run annotation** — process your corpus in batches
5. **Quality check** — measure inter-annotator agreement, confidence distributions

## Deliverable

- **Annotated dataset**: A set of articles with gold-standard labels
- **Quality report**: Agreement metrics (≥ 0.80 target), confidence distributions, cost analysis
- **Reusable schema**: Domain schemas that others can adopt or adapt
