> **Navigation:** [Documentation Portal](../../index.md) > [Research](../) > [Methodologies](./) > Level 1
>
> ---

# Level 1: Lexicon-Based Narrative Detection

> **Hierarchy:** First automated approach — counts pre-defined words and phrases.
> **BENI Status:** ✅ Implemented — three Bangla lexicons in `narrative.py`
> **Core Idea:** Define a dictionary of terms associated with a narrative; count occurrences per document.

---

## Table of Contents

1. [Overview](#overview)
2. [Techniques](#techniques)
3. [Worked Example](#worked-example)
4. [Strengths & Weaknesses](#strengths--weaknesses)
5. [When to Use Level 1](#when-to-use-level-1)
6. [BENI Implementation Detail](#beni-implementation-detail)
7. [Best Practices](#best-practices)
8. [Advanced: Weighted and Scored Lexicons](#advanced-weighted-and-scored-lexicons)
9. [Improvement Path to Level 4](#improvement-path-to-level-4)
10. [References](#references)

---

## Overview

Lexicon-based narrative detection is the simplest automated approach. It counts occurrences of pre-defined words and phrases associated with specific narratives, then uses those counts as a proxy for narrative prevalence.

### Key Principle

**Words are markers of meaning.** If a document uses words like "inflation," "prices," and "cost of living," it is likely participating in an inflation narrative. The more such terms, the stronger the narrative presence.

### Limitations

The fundamental limitation: **lexicons find topics, not narratives.** A keyword match for "inflation" tells you the word appeared, not whether the article tells a causal story. This limitation motivates all higher levels.

---

## Techniques

### Simple Keyword Matching

```python
narrative_keywords = ["inflation", "prices", "cost of living"]
count = sum(1 for word in text.split() if word in narrative_keywords)
```

### Dictionary-Based Scoring

```python
narrative_lexicon = {
    "inflation": {"weight": 1.0, "polarity": "negative"},
    "price_hike": {"weight": 1.5, "polarity": "negative"},
    "stable_prices": {"weight": 0.5, "polarity": "positive"},
}
score = sum(entry["weight"] for word in text if word in narrative_lexicon)
```

### Regular Expression Patterns

```python
import re
pattern = re.compile(r"(inflation|rising prices|cost of living|price hike)", re.IGNORECASE)
matches = pattern.findall(text)
```

### Normalization Approaches

| Method | Formula | Use Case |
|--------|---------|----------|
| Raw count | `count` | Absolute presence |
| Per-document frequency | `count / total_words` | Document length normalization |
| Per-corpus TF | `count / total_docs_with_term` | Corpus-level prevalence |
| TF-IDF weighting | `count * log(N / df)` | Discriminative term importance |

---

## Worked Example

### Lexicon: Inflation Narrative

```python
inflation_lexicon = [
    "inflation", "prices", "cost of living",
    "food prices", "fuel costs", "price hike",
    "rising prices", "inflationary pressure"
]
```

### Document 1

> "Inflation continues to rise as food prices surge. The cost of living crisis is deepening."

**Matches:** inflation, food prices, cost of living, rising (prices implied)

**Score:** 4 matches — Strong inflation narrative presence

### Document 2

> "The central bank raised interest rates to 6%."

**Matches:** (none)

**Score:** 0 — No inflation narrative detected

### Document 3

> "Economists debate whether inflationary pressure is transitory. The price index rose 0.3%."

**Matches:** inflationary pressure, price (index)

**Score:** 2 matches — Moderate inflation narrative

---

## Strengths & Weaknesses

### Strengths

| Strength | Description |
|----------|-------------|
| **Simple to implement** | No training data, no models — just a word list |
| **Interpretable** | You know exactly which terms drove the score |
| **Fast** | Linear time in document length; millions of documents per second |
| **Reproducible** | Same input always produces same output |
| **Language-agnostic** | Works for any language with a word list |
| **Good for well-defined topics** | "Inflation" has a stable vocabulary across contexts |

### Weaknesses

| Weakness | Description | Mitigation |
|----------|-------------|------------|
| **Finds topics, not narratives** | Cannot distinguish "inflation is rising" from "inflation is controlled" | Add polarity weights |
| **No semantic understanding** | "Price" in "price of freedom" ≠ economic price | Use contextual disambiguation (L10) |
| **Vocabulary drift** | New terms ("greedflation") not in lexicon | Periodic lexicon updates |
| **Language variation** | Dialect, spelling variants, transliteration | Include all known variants |
| **False positives** | Keywords in non-narrative contexts | Use stop-word lists, negation handling |

---

## When to Use Level 1

| Scenario | Recommended | Alternative |
|----------|-------------|-------------|
| Quick exploratory analysis | ✅ **Level 1** | — |
| Real-time narrative tracking | ✅ **Level 1** (fastest option) | L10 for deeper analysis |
| Well-defined, stable vocabulary | ✅ **Level 1** | — |
| Cross-lingual baseline | ✅ **Level 1** (translated keywords) | L10 zero-shot |
| Complex, evolving narratives | ❌ Vocabulary is always outdated | L3/L4 topic modeling |
| Causal narrative extraction | ❌ Requires L7+ | — |

---

## BENI Implementation Detail

### Code References

| File | Purpose | Key Details |
|------|---------|-------------|
| `pipelines/BENI/experiment/beni_pilot/narrative.py` | Core lexicon module | 3 lexicons, scoring functions |
| `pipelines/BENI/experiment/beni_pilot/predict.py` | BENI Predictor | Combines TF-IDF + lexicon scoring |
| `pipelines/shared/analysis/bengali_economic_keywords.py` | Extended keyword lists | BBD index keywords |
| `pipelines/BENI/exploration/run_bbd_index.py` | BBD-style index | Keyword counting per month |
| `pipelines/BENI/exploration/config.yaml` | Keyword paths | References keyword files |
| `pipelines/BENI/annotation/finetune_banglabert_for_prelabel.py` | Keyword pre-labels | BanglaBERT on keyword labels |

### Narrative Force Lexicon

```python
NARRATIVE_FORCE_LEXICON = {
    "crisis": [
        "সংকট", "চাপ", "ঝুঁকি", "অস্থিরতা",
        "ধস", "ঘাটতি", "বিপর্যয়", "বিপর্যয়"
    ],
    "burden": [
        "দুর্ভোগ", "কষ্ট", "ব্যয়", "ব্যয়",
        "জীবনযাত্রা", "ভোগান্তি", "চড়া", "চড়া"
    ],
    "blame": [
        "ব্যর্থতা", "দুর্নীতি", "সিন্ডিকেট",
        "অব্যবস্থাপনা", "দায়ী", "দায়ী", "অভিযোগ"
    ],
    "reform": [
        "সংস্কার", "নীতিমালা", "শৃঙ্খলা",
        "উদ্যোগ", "পদক্ষেপ", "পরিকল্পনা"
    ],
    "stability": [
        "স্থিতিশীল", "স্বস্তি", "উন্নতি",
        "নিয়ন্ত্রণ", "নিয়ন্ত্রণ", "সামাল"
    ],
    "uncertainty": [
        "অনিশ্চয়তা", "অনিশ্চয়তা", "আশঙ্কা",
        "শঙ্কা", "সন্দেহ", "প্রশ্ন"
    ],
    "resilience": [
        "ঘুরে দাঁড়ানো", "ঘুরে দাঁড়ানো", "সহনশীল",
        "প্রবৃদ্ধি", "সম্ভাবনা", "পুনরুদ্ধার"
    ],
}
```

### Valuation Target Lexicon

```python
VALUATION_TARGET_LEXICON = {
    "government": ["সরকার", "মন্ত্রণালয়", "মন্ত্রণালয়", "মন্ত্রী", "প্রশাসন"],
    "central_bank": ["বাংলাদেশ ব্যাংক", "কেন্দ্রীয় ব্যাংক", "কেন্দ্রীয় ব্যাংক"],
    "banks": ["ব্যাংক", "ঋণ", "আমানত", "তারল্য"],
    "businesses": ["ব্যবসায়ী", "ব্যবসায়ী", "শিল্প", "উদ্যোক্তা", "কারখানা"],
    "market_actors": ["বাজার", "সিন্ডিকেট", "ব্যবসায়ী", "মজুতদার"],
    "global_economy": ["বিশ্ববাজার", "আইএমএফ", "ডলার", "তেল", "আমদানি", "রপ্তানি"],
    "households": ["ভোক্তা", "পরিবার", "জনগণ", "মানুষ", "ক্রেতা"],
}
```

### Economic Topic Lexicon

```python
ECONOMIC_TOPIC_LEXICON = {
    "inflation": ["মূল্যস্ফীতি", "দাম", "মূল্য", "খাদ্য মূল্য", "ভোক্তা মূল্য"],
    "exchange_rate": ["ডলার", "টাকা", "বিনিময় হার", "বিনিময় হার"],
    "reserves": ["রিজার্ভ", "বৈদেশিক মুদ্রা"],
    "banking": ["ব্যাংক", "ঋণ", "আমানত", "সুদ", "তারল্য"],
    "fiscal_policy": ["বাজেট", "কর", "রাজস্ব", "ভর্তুকি", "ঘাটতি"],
    "trade": ["রপ্তানি", "আমদানি", "বাণিজ্য", "এলসি"],
    "employment": ["কর্মসংস্থান", "বেকারত্ব", "মজুরি", "চাকরি"],
    "growth_investment": ["জিডিপি", "প্রবৃদ্ধি", "বিনিয়োগ", "বিনিয়োগ", "উৎপাদন"],
}
```

### Scoring Functions

The `narrative.py` module provides three functions:

```python
def score_lexicon(text, lexicon):
    """Score text against a lexicon. Returns sorted LexiconScore list."""
    normalized = normalize_text(text)
    scores = []
    for label, terms in lexicon.items():
        matches = [term for term in terms if term in normalized]
        scores.append(LexiconScore(label, len(matches), matches))
    return sorted(scores, key=lambda x: (-x.score, x.label))

def top_label(text, lexicon, fallback="none"):
    """Get the highest-scoring label for a lexicon."""
    scores = score_lexicon(text, lexicon)
    if not scores or scores[0].score == 0:
        return LexiconScore(fallback, 0, [])
    return scores[0]

def narrative_profile(text):
    """Full narrative profile: topic, force, target + all scores."""
    topic = top_label(text, ECONOMIC_TOPIC_LEXICON, "other")
    force = top_label(text, NARRATIVE_FORCE_LEXICON, "neutral")
    target = top_label(text, VALUATION_TARGET_LEXICON, "unnamed_system")
    return {
        "economic_topic": topic.__dict__,
        "narrative_force": force.__dict__,
        "valuation_target": target.__dict__,
        "all_topic_scores": [...],
        "all_force_scores": [...],
        "all_target_scores": [...],
    }
```

### BBD-Style Keyword Index

The BBD (Baker-Blum-Delves) style index uses broader keyword lists from `bengali_economic_keywords.py`:

```python
ECONOMY_KEYWORDS = [
    # 27 Bangla economic terms
    "অর্থনীতি", "বাজেট", "মূল্যস্ফীতি", ...
]
POLICY_KEYWORDS = [
    "নীতি", "সুদের হার", "আইএমএফ", ...
]
NARRATIVE_KEYWORDS = {
    "crisis": [...],
    "growth": [...],
    "instability": [...],
}
```

The BBD index normalizes per source and produces a monthly index standardized to mean=100.

---

## Best Practices

### Lexicon Design

1. **Start with seed terms** from domain experts or existing literature
2. **Expand via word embeddings** — find semantically similar terms (see Level 4)
3. **Include all orthographic variants** — Bangla has multiple spellings for many words
4. **Test precision and recall** on a small annotated sample before scaling
5. **Update periodically** — economic narratives coin new terms ("greedflation", "shrinkflation")

### Handling Negation

Simple negation handling drastically improves precision:

```python
NEGATION_PATTERNS = r"(not|no|never|without|despite|no)\s+(inflation|prices|...)"

def has_negation(text, keyword):
    """Check if a keyword match is negated."""
    pattern = rf"(not|no|never|without|despite)\s+{keyword}"
    return bool(re.search(pattern, text, re.IGNORECASE))
```

### Normalization for Bangla

BENI's `normalize_text()` in `utils.py`:

```python
BANGLA_PUNCT_RE = re.compile(r"[\u0964\u0965।,;:!?\"'“”‘’()\[\]{}<>/\\|_=+*`~#@$%^&]")
SPACE_RE = re.compile(r"\s+")

def normalize_text(text):
    text = str(text).replace("\ufeff", " ")  # BOM
    text = BANGLA_PUNCT_RE.sub(" ", text)
    text = SPACE_RE.sub(" ", text)
    return text.strip()
```

---

## Advanced: Weighted and Scored Lexicons

### Term Frequency-Weighted Scoring

```python
class WeightedLexicon:
    def __init__(self, categories):
        self.categories = categories  # {label: [(term, weight), ...]}

    def score(self, text):
        normalised = normalize_text(text)
        scores = {}
        for label, terms in self.categories.items():
            score = sum(weight * normalised.count(term) for term, weight in terms)
            scores[label] = score
        return scores
```

### PMI-Expanded Lexicons

Use Pointwise Mutual Information to discover new terms:

```python
PMI(w1, w2) = log(P(w1, w2) / (P(w1) * P(w2)))
```

Terms with high PMI to seed words are candidate additions.

### Sentiment-Weighted Lexicons

```python
narrative_lexicon = {
    "inflation": {"weight": 1.0, "sentiment": -0.3},
    "price_hike": {"weight": 1.5, "sentiment": -0.5},
    "economic_growth": {"weight": 1.0, "sentiment": +0.4},
}
weighted_narrative_score = sum(count * weight for term in text if term in lexicon)
sentiment_score = sum(count * sentiment for term in text if term in lexicon)
```

---

## Improvement Path to Level 4

The main limitation of Level 1 is vocabulary coverage. The path to Level 4 (Embedding-Based Discovery) uses the lexicon as *seed terms* for semantic expansion:

```
L1 Lexicon (seed terms, ~50-100 words)
    ↓
L4 Embedding Model (SBERT/E5/BGE)
    ↓
Semantic Similarity Search
    ↓
Expanded Term Set (500-1,000 semantically related terms)
    ↓
Validate against L0 gold standard
    ↓
Iterate
```

This preserves the interpretability of Level 1 while leveraging the semantic coverage of Level 4.

---

## References

### Core Reading

- Baker, S. R., Bloom, N., & Davis, S. J. (2016). "Measuring Economic Policy Uncertainty." *Quarterly Journal of Economics*, 131(4): 1593–1636.
  — The canonical BBD approach using keyword-based indices.

- Tetlock, P. C. (2007). "Giving Content to Investor Sentiment: The Role of Media in the Stock Market." *Journal of Finance*, 62(3): 1139–1168.
  — Early media sentiment index using keyword-based methods.

- Loughran, T. & McDonald, B. (2011). "When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks." *Journal of Finance*, 66(1): 35–65.
  — Finance-specific lexicon methodology.

### BENI-Specific

- Nabil, A. N. (2026). "BENI Narrative Lexicon." `pipelines/BENI/experiment/beni_pilot/narrative.py`
- Nabil, A. N. (2026). "BENI BBD Index." `pipelines/BENI/exploration/run_bbd_index.py`
- Nabil, A. N. (2026). "Bengali Economic Keywords." `pipelines/shared/analysis/bengali_economic_keywords.py`

### See Also

- Level 4: [Embedding-Based Narrative Discovery](L04_embedding_based_discovery.md) — Semantic expansion
- Level 2: [Statistical Text Mining](L02_statistical_text_mining.md) — TF-IDF weighting

---

**Up:** [Methodologies Index](INDEX.md) | **Main:** [Narrative Extraction Methodologies](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
