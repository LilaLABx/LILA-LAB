# Multi-Account Kaggle Experiment Guide

## Strategy

**Problem:** Training all 6 BanglaBERT models sequentially on one Kaggle account takes ~15 hours (Model 4a in `kaggle_pipeline.py`).

**Solution:** Distribute across 6 Kaggle accounts — each trains one model in parallel. Total wall time: **~3 hours** instead of 15.

| Account | Model | Params | Est. Time | Batch | Accum |
|---------|-------|--------|-----------|-------|-------|
| Account 1 | `csebuetnlp/banglabert_small` | 13M | ~30 min | 32 | 1 |
| Account 2 | `csebuetnlp/banglabert` | 110M | ~2-3 hrs | 8 | 4 |
| Account 3 | `sagorsarker/bangla-bert-base` | 110M | ~2-3 hrs | 8 | 4 |
| Account 4 | `neuropark/sahajBERT` | 18M | ~45 min | 32 | 1 |
| Account 5 | `xlm-roberta-base` | 270M | ~3-4 hrs | 4 | 8 |
| Account 6 | `bert-base-multilingual-cased` | 180M | ~2-3 hrs | 8 | 4 |

Each account will produce:
- `beni_model_{short_name}_*.zip` — fine-tuned model weights
- `beni_reports_{short_name}_*.zip` — training metrics
- `beni_artifacts_*.zip` — narrative index CSV + full predictions parquet + correlations

---

## Setup (Same for All 6 Accounts)

### Step 1: Create the notebook

1. Go to [kaggle.com](https://kaggle.com) → **Create** → **New Notebook**
2. In the right sidebar → **Add Data** → search for `annnasernabil/beni-data` → click **+** to add
3. **Settings** → **Accelerator** → **GPU T4 x1**
4. **Settings** → **Internet** → **On** (required to download HuggingFace models and git clone)

### Step 2: Cell 1 — Install dependencies

```python
!pip install -q transformers sentencepiece accelerate
```

### Step 3: Cell 2 — Detect data directory

```python
from pathlib import Path

DATA_CANDIDATES = [
    Path("/kaggle/input/datasets/annnasernabil/beni-data/beni-data"),
    Path("/kaggle/input/beni-data/beni-data"),
    Path("/kaggle/input/beni-data"),
]

DATA_DIR = None
for cand in DATA_CANDIDATES:
    if (cand / "potrika").exists():
        DATA_DIR = cand
        break

if DATA_DIR is None:
    raise FileNotFoundError(
        "Cannot find beni-data dataset. "
        "Make sure you added it to the notebook (Add Data → annnasernabil/beni-data)."
    )

print(f"Data directory: {DATA_DIR}")
print(f"  potrika/  exists: {(DATA_DIR / 'potrika').exists()}")
print(f"  macro/    exists: {(DATA_DIR / 'macro').exists()}")
print(f"  models/   exists: {(DATA_DIR / 'models').exists()}")
```

### Step 4: Cell 3 — Clone code

```python
!git clone --depth 1 https://github.com/LilaLABx/LILA-LAB.git /kaggle/working/repo 2>&1 | tail -3
%cd /kaggle/working/repo/pipelines/BENI/experiment/beni_pilot
!pwd
```

---

## Per-Account Commands (Copy the section for YOUR model only)

---

### Account 1 — `banglabert_small` (13M params, ~30 min)

```python
BANGLA_MODEL = "csebuetnlp/banglabert_small"

# --- TRAIN ---
!python3 train.py \
    --task economic \
    --model-type banglabert \
    --data-source potrika-timeseries \
    --data-dir "{DATA_DIR}" \
    --banglabert-model-name {BANGLA_MODEL} \
    --banglabert-batch-size 32 \
    --banglabert-epochs 10 \
    --zip

# ⬇️ DOWNLOAD: beni_model_banglabert_small_*.zip + beni_reports_banglabert_small_*.zip
#    Go to Data → Output → find these zips → download

# --- BUILD INDEX ---
!python3 build_index.py \
    --data-dir "{DATA_DIR}" \
    --model-type banglabert \
    --banglabert-model-name {BANGLA_MODEL} \
    --zip

# ⬇️ DOWNLOAD: beni_artifacts_*.zip  (contains narrative_index_banglabert_small.csv + full_predictions_banglabert_small.parquet + reports)

# --- CORRELATE ---
!python3 correlate.py \
    --data-dir "{DATA_DIR}" \
    --zip

# ⬇️ DOWNLOAD: beni_artifacts_*.zip (updated — now includes index/correlations.csv)
```

---

### Account 2 — `banglabert` (110M params, ~2-3 hrs)

```python
BANGLA_MODEL = "csebuetnlp/banglabert"

!python3 train.py \
    --task economic \
    --model-type banglabert \
    --data-source potrika-timeseries \
    --data-dir "{DATA_DIR}" \
    --banglabert-model-name {BANGLA_MODEL} \
    --banglabert-batch-size 8 \
    --banglabert-accum-steps 4 \
    --banglabert-epochs 10 \
    --zip

# ⬇️ DOWNLOAD: beni_model_banglabert_*.zip + beni_reports_banglabert_*.zip

!python3 build_index.py \
    --data-dir "{DATA_DIR}" \
    --model-type banglabert \
    --banglabert-model-name {BANGLA_MODEL} \
    --zip

# ⬇️ DOWNLOAD: beni_artifacts_*.zip

!python3 correlate.py \
    --data-dir "{DATA_DIR}" \
    --zip

# ⬇️ DOWNLOAD: beni_artifacts_*.zip (updated)
```

---

### Account 3 — `bangla-bert-base` (110M params, ~2-3 hrs)

```python
BANGLA_MODEL = "sagorsarker/bangla-bert-base"

!python3 train.py \
    --task economic \
    --model-type banglabert \
    --data-source potrika-timeseries \
    --data-dir "{DATA_DIR}" \
    --banglabert-model-name {BANGLA_MODEL} \
    --banglabert-batch-size 8 \
    --banglabert-accum-steps 4 \
    --banglabert-epochs 10 \
    --zip

# ⬇️ DOWNLOAD: beni_model_bangla_bert_base_*.zip + beni_reports_bangla_bert_base_*.zip

!python3 build_index.py \
    --data-dir "{DATA_DIR}" \
    --model-type banglabert \
    --banglabert-model-name {BANGLA_MODEL} \
    --zip

# ⬇️ DOWNLOAD: beni_artifacts_*.zip

!python3 correlate.py \
    --data-dir "{DATA_DIR}" \
    --zip

# ⬇️ DOWNLOAD: beni_artifacts_*.zip (updated)
```

---

### Account 4 — `sahajBERT` (18M params, ~45 min)

```python
BANGLA_MODEL = "neuropark/sahajBERT"

!python3 train.py \
    --task economic \
    --model-type banglabert \
    --data-source potrika-timeseries \
    --data-dir "{DATA_DIR}" \
    --banglabert-model-name {BANGLA_MODEL} \
    --banglabert-batch-size 32 \
    --banglabert-epochs 10 \
    --zip

# ⬇️ DOWNLOAD: beni_model_sahajbert_*.zip + beni_reports_sahajbert_*.zip

!python3 build_index.py \
    --data-dir "{DATA_DIR}" \
    --model-type banglabert \
    --banglabert-model-name {BANGLA_MODEL} \
    --zip

# ⬇️ DOWNLOAD: beni_artifacts_*.zip

!python3 correlate.py \
    --data-dir "{DATA_DIR}" \
    --zip

# ⬇️ DOWNLOAD: beni_artifacts_*.zip (updated)
```

---

### Account 5 — `xlm-roberta-base` (270M params, ~3-4 hrs)

> ⚠️ This is the largest model. The T4 has 15 GB VRAM which is enough,
> but batch size is reduced to 4 with 8 accumulation steps to stay within limits.

```python
BANGLA_MODEL = "xlm-roberta-base"

!python3 train.py \
    --task economic \
    --model-type banglabert \
    --data-source potrika-timeseries \
    --data-dir "{DATA_DIR}" \
    --banglabert-model-name {BANGLA_MODEL} \
    --banglabert-batch-size 4 \
    --banglabert-accum-steps 8 \
    --banglabert-epochs 10 \
    --zip

# ⬇️ DOWNLOAD: beni_model_xlm_roberta_base_*.zip + beni_reports_xlm_roberta_base_*.zip

!python3 build_index.py \
    --data-dir "{DATA_DIR}" \
    --model-type banglabert \
    --banglabert-model-name {BANGLA_MODEL} \
    --zip

# ⬇️ DOWNLOAD: beni_artifacts_*.zip

!python3 correlate.py \
    --data-dir "{DATA_DIR}" \
    --zip

# ⬇️ DOWNLOAD: beni_artifacts_*.zip (updated)
```

---

### Account 6 — `mBERT` (180M params, ~2-3 hrs)

```python
BANGLA_MODEL = "bert-base-multilingual-cased"

!python3 train.py \
    --task economic \
    --model-type banglabert \
    --data-source potrika-timeseries \
    --data-dir "{DATA_DIR}" \
    --banglabert-model-name {BANGLA_MODEL} \
    --banglabert-batch-size 8 \
    --banglabert-accum-steps 4 \
    --banglabert-epochs 10 \
    --zip

# ⬇️ DOWNLOAD: beni_model_mbert_*.zip + beni_reports_mbert_*.zip

!python3 build_index.py \
    --data-dir "{DATA_DIR}" \
    --model-type banglabert \
    --banglabert-model-name {BANGLA_MODEL} \
    --zip

# ⬇️ DOWNLOAD: beni_artifacts_*.zip

!python3 correlate.py \
    --data-dir "{DATA_DIR}" \
    --zip

# ⬇️ DOWNLOAD: beni_artifacts_*.zip (updated)
```

---

## Download Checklist

After all cells finish, download these zips from **Data → Output**:

| Account | Model ZIP | Reports ZIP | Artifacts ZIP |
|---------|-----------|-------------|---------------|
| 1 | `beni_model_banglabert_small_*.zip` | `beni_reports_banglabert_small_*.zip` | `beni_artifacts_*.zip` |
| 2 | `beni_model_banglabert_*.zip` | `beni_reports_banglabert_*.zip` | `beni_artifacts_*.zip` |
| 3 | `beni_model_bangla_bert_base_*.zip` | `beni_reports_bangla_bert_base_*.zip` | `beni_artifacts_*.zip` |
| 4 | `beni_model_sahajbert_*.zip` | `beni_reports_sahajbert_*.zip` | `beni_artifacts_*.zip` |
| 5 | `beni_model_xlm_roberta_base_*.zip` | `beni_reports_xlm_roberta_base_*.zip` | `beni_artifacts_*.zip` |
| 6 | `beni_model_mbert_*.zip` | `beni_reports_mbert_*.zip` | `beni_artifacts_*.zip` |

---

## Combining Results (After All Accounts Finish)

Once you've downloaded all zips, organize them locally:

```bash
# Create a combined results directory
mkdir -p results/models results/reports results/index

# Extract each model's zip into the right place
cd results

# Example for banglabert (do this for each model):
unzip ~/Downloads/beni_model_banglabert_small_*.zip -d models/
unzip ~/Downloads/beni_reports_banglabert_small_*.zip -d reports/
unzip ~/Downloads/beni_artifacts_20260611_*.zip   # ← contains index/ for this model
```

Each model's artifacts zip contains **model-prefixed** files:
- `index/narrative_index_{short_name}.csv`
- `index/full_predictions_{short_name}.parquet`
- `index/correlations.csv` (shared — last model's run overwrites)

The correlation files are identical across models (same macro data). For the per-model comparison, use the `narrative_index_{short_name}.csv` files to compare index values across models.

---

## McNemar's Test (Optional)

To statistically compare any two models on the test set (e.g., BanglaBERT vs TF-IDF),
add this cell after training (see Cell 4.5 in `kaggle_pipeline.py`):

```python
import sys, joblib, torch, numpy as np
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score
from scipy.stats import chi2
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer

sys.path.insert(0, "/kaggle/working/repo/pipelines/BENI/experiment/beni_pilot")
from data import load_potrika_timeseries
from config import ExperimentConfig
from banglabert import BanglaBERTDataset, get_model_short_name

BANGLA_MODEL = "csebuetnlp/banglabert"  # ← change to compare a different model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load test set
cfg = ExperimentConfig(potrika_dir=DATA_DIR / "potrika")
splits = load_potrika_timeseries(cfg)
test = splits["test"]
texts = test["text_norm"].tolist()
labels = test["economic_relevance"].tolist()

# TF-IDF predictions
tfidf = joblib.load(DATA_DIR / "models" / "economic_potrika-timeseries_tfidf_logreg.joblib")
tfidf_preds = tfidf.predict(texts)

# BanglaBERT predictions
short_name = get_model_short_name(BANGLA_MODEL)
model_path = f"/kaggle/working/outputs/models/{short_name}_economic_potrika-timeseries"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.to(device)
model.eval()

dataset = BanglaBERTDataset(texts, [0] * len(texts), tokenizer, cfg)
loader = DataLoader(dataset, batch_size=8, shuffle=False)

bert_preds = []
for batch in loader:
    input_ids = batch["input_ids"].to(device)
    attention_mask = batch["attention_mask"].to(device)
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        preds = torch.argmax(outputs.logits, dim=-1)
        bert_preds.extend(preds.cpu().numpy())

# Contingency table
n00 = n01 = n10 = n11 = 0
for t, a, b in zip(labels, tfidf_preds, bert_preds):
    if a == t and b == t:    n00 += 1
    elif a == t and b != t:  n01 += 1
    elif a != t and b == t:  n10 += 1
    else:                    n11 += 1

stat = (abs(n01 - n10) - 1) ** 2 / (n01 + n10 + 1e-10)
p = chi2.sf(stat, 1)

print(f"Both correct:        {n00}")
print(f"TF-IDF only correct: {n01}")
print(f"BanglaBERT only:     {n10}")
print(f"Both wrong:          {n11}")
print(f"χ² = {stat:.2f}, p = {p:.4f}")
print(f"BanglaBERT net improvement: {n10 - n01} fewer errors")
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `CUDA out of memory` | Batch too large for model | Reduce `--banglabert-batch-size` and increase `--banglabert-accum-steps` proportionally |
| `Cannot find beni-data dataset` | Dataset not added to notebook | Click Add Data → search `annnasernabil/beni-data` |
| `No space left on device` | /kaggle/working disk full | Run Cell 9 safety zip, download everything, then restart session |
| Model downloads every time | Cache cleared between sessions | Expected — first run always downloads from HuggingFace |

---

## Quick Reference: Model Short Names

The code maps full HuggingFace names to short names for filenames:

| Full Name | Short Name |
|-----------|-----------|
| `csebuetnlp/banglabert_small` | `banglabert_small` |
| `csebuetnlp/banglabert` | `banglabert` |
| `sagorsarker/bangla-bert-base` | `bangla_bert_base` |
| `neuropark/sahajBERT` | `sahajbert` |
| `xlm-roberta-base` | `xlm_roberta_base` |
| `bert-base-multilingual-cased` | `mbert` |

Use the short name when matching downloaded zip files to models.
