# Hugging Face Distribution — BENI

## Platform Structure

```
huggingface.co/nabil0x/
├── beni-banglabert/                  # Model: Fine-tuned BanglaBERT for economic classification
│   ├── README.md                     # Model card
│   ├── config.json
│   ├── model.safetensors
│   └── tokenizer files
│
├── beni-narrative-index/             # Dataset: BENI narrative index values
│   ├── README.md                     # Dataset card
│   ├── narrative_index.csv
│   └── reference_labels.jsonl
│
└── beni-classifier-demo/             # Space: Interactive Gradio demo
    ├── app.py
    ├── requirements.txt
    ├── README.md
    └── (deployed model from beni-banglabert)
```

---

## Model Card Template

### beni-banglabert

```yaml
---
license: mit
language:
- bn
- en
tags:
- economics
- narrative-indices
- bangla
- text-classification
- low-resource
library_name: transformers
pipeline_tag: text-classification
datasets:
- nabil0x/beni-narrative-index
widget:
- text: "বাংলাদেশের অর্থনীতি বর্তমানে চ্যালেঞ্জের মুখোমুখি"
  example_title: Economic
- text: "আজ ঢাকায় বৃষ্টি হওয়ার সম্ভাবনা রয়েছে"
  example_title: Non-economic
---
```

**Model description**: Fine-tuned BanglaBERT (sagorbr/bangla-bert-base) for binary classification of Bangla news sentences as Economic or Not Economic. Part of the Bangla Economic Narrative Index (BENI) research program. Achieves 88.2% accuracy on a gold-standard held-out test set.

**Training data**: 3,200 Bangla news sentences from the Potrika corpus (10.17632/v362rp78dc.4), annotated via:
- Human annotation (1,200 sentences, 3 annotators, pairwise)
- LLM-assisted annotation (500 sentences, majority-vote over 3 models × 2 templates)
- Active learning rounds (1,500+ sentences, k-label exploration from k=500 to k=3000)

**Training procedure**:
- Base model: `sagorbr/bangla-bert-base`
- Learning rate: 2e-5
- Batch size: 16
- Epochs: 3
- Max seq length: 128
- Hardware: CPU (no GPU) — note data augmentation may differ

**Evaluation results**:
| Metric | Score |
|--------|-------|
| Accuracy | 0.882 |
| F1 (macro) | 0.871 |
| Precision | 0.878 |
| Recall | 0.885 |

**Limitations**:
- Trained on COVID-era (2020-2021) Bangla news — may not generalize to other periods
- Binary economic/non-economic only — no sector or sentiment dimensions
- Single annotator quality depends on active learning label quality

**Citing this model**:
```bibtex
@software{nabil2025beni,
  author = {Nabil, Ann Naser},
  title = {BENI: Bangla Economic Narrative Index},
  year = {2025},
  doi = {10.5281/zenodo.20585401},
  url = {https://github.com/LilaLABx/LILA-LAB}
}
```

**Links**: [GitHub](https://github.com/LilaLABx/LILA-LAB) | [OSF](https://osf.io/[project-id]) | [Dataset](https://huggingface.co/datasets/nabil0x/beni-narrative-index)

---

## Dataset Card Template

### beni-narrative-index

```yaml
---
license: cc-by-4.0
language:
- bn
tags:
- economics
- bangla
- narrative-indices
- text-as-data
- macroeconomics
size_categories:
- 1K<n<10K
task_categories:
- text-classification
- time-series-forecasting
---
```

**Dataset description**: Daily narrative index values for Bangla economic news from July 2020 to June 2021, constructed using the BENI pipeline. Each row contains a date, the proportion of economic news articles, and sample metadata.

**Source corpus**: Potrika Bangla news corpus (Mendeley Data, 10.17632/v362rp78dc.4)

**Fields**:
- `date`: Date (2020-07-01 to 2021-06-30)
- `economic_proportion`: Proportion of articles classified as economic on that date
- `total_articles`: Total articles classified on that date
- `economic_article_count`: Number of economic articles
- `rolling_7d_mean`: 7-day rolling average

**Splits**: Single chronological split (no train/test — this is the final index)

**Usage**:
```python
from datasets import load_dataset
ds = load_dataset("nabil0x/beni-narrative-index", split="train")
```

**Citations**: Cite the BENI dataset DOI (10.5281/zenodo.20585401) and the original Potrika corpus (10.17632/v362rp78dc.4)

---

## Gradio Space — app.py Template

```python
import gradio as gr
import joblib
import numpy as np
import re
from pathlib import Path

# Load model and vectorizer
BASE_DIR = Path(__file__).parent
tfidf = joblib.load(BASE_DIR / "tfidf_vectorizer.joblib")
model = joblib.load(BASE_DIR / "economic_tfidf_logreg.joblib")

def clean_text(text: str) -> str:
    """Minimal Bangla text cleaner."""
    text = re.sub(r'[^\u0980-\u09FF\s\w]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def classify(text: str):
    if not text.strip():
        return "Please enter text", 0.0
    
    cleaned = clean_text(text)
    vec = tfidf.transform([cleaned])
    pred = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]
    
    label = "📈 Economic" if pred == 1 else "📰 Non-Economic"
    confidence = float(max(proba))
    
    return label, confidence

# Interface
demo = gr.Interface(
    fn=classify,
    inputs=gr.Textbox(
        label="Bangla Text",
        placeholder="পaste Bangla news text here...",
        lines=5
    ),
    outputs=[
        gr.Label(label="Classification"),
        gr.Number(label="Confidence")
    ],
    title="📊 BENI Classifier",
    description="Classify Bangla news as **Economic** or **Non-Economic** "
                "using the Bangla Economic Narrative Index pipeline.",
    examples=[
        ["বাংলাদেশের অর্থনীতি বর্তমানে চ্যালেঞ্জের মুখোমুখি"],
        ["আজ ঢাকায় বৃষ্টি হওয়ার সম্ভাবনা রয়েছে"],
        ["রপ্তানি আয় বেড়েছে ১৫ শতাংশ"],
    ],
    article="""## About
    This model is part of the [LILA Lab](https://github.com/LilaLABx/LILA-LAB).
    It uses a TF-IDF + Logistic Regression classifier trained on 3,200 human-annotated
    Bangla news sentences from the Potrika corpus.
    
    **Accuracy**: 88.2% | **License**: MIT (code), CC BY 4.0 (data)
    [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20585401.svg)](https://doi.org/10.5281/zenodo.20585401)
    """,
)

if __name__ == "__main__":
    demo.launch()
```

---

## Upload Commands

```bash
# Install HF CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Create repository for model
huggingface-cli repo create beni-banglabert --type model

# Upload model files
huggingface-cli upload beni-banglabert /path/to/model/files/

# Create dataset repository
huggingface-cli repo create beni-narrative-index --type dataset

# Upload dataset files
huggingface-cli upload beni-narrative-index /path/to/data/files/

# Create Space
huggingface-cli repo create beni-classifier-demo --type space --space_sdk gradio

# For Space, push directly or use git
cd beni-classifier-demo
git init && git remote add space https://huggingface.co/spaces/nabil0x/beni-classifier-demo
git add . && git commit -m "Initial demo" && git push
```

---

## Which Models to Upload

From the active learning experiment, upload the **best model at each k**:

| k (label count) | Best Config       | Accuracy | File                                                  |
|-----------------|-------------------|----------|-------------------------------------------------------|
| 500             | TF-IDF + LogReg   | 86.4%    | (from active learning results)                        |
| 1000            | TF-IDF + LogReg   | 87.1%    | (from active learning results)                        |
| 1500            | TF-IDF + LogReg   | 87.8%    | (from active learning results)                        |
| 2000            | TF-IDF + LogReg   | 88.2%    | (from active learning results)                        |
| **3000 (final)**| TF-IDF + LogReg   | **88.2%**| ← Upload this as primary model                        |

For models smaller than 5GB each (safetensors + vocab), upload the k=3000 final model as primary and k=2000 as secondary. The TF-IDF + LogReg joblib files (~20MB each) should also be uploaded for lightweight inference.
