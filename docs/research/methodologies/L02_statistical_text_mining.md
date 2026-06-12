> **Navigation:** [Documentation Portal](../../index.md) > [Research](../) > [Methodologies](./) > Level 2
>
> ---

# Level 2: Statistical Text Mining

> **Hierarchy:** Narrative approximation through word distribution patterns.
> **BENI Status:** ✅ Implemented — TF-IDF + Logistic Regression at 91.7% accuracy
> **Core Idea:** Use statistical properties of word distributions (frequency, co-occurrence, discrimination) to identify narrative-relevant text patterns.

---

## Table of Contents

1. [Overview](#overview)
2. [Techniques](#techniques)
3. [Worked Example](#worked-example)
4. [Strengths & Weaknesses](#strengths--weaknesses)
5. [When to Use Level 2](#when-to-use-level-2)
6. [BENI Implementation Detail](#beni-implementation-detail)
7. [TF-IDF Deep Dive](#tf-idf-deep-dive)
8. [Co-occurrence Networks](#co-occurrence-networks)
9. [Best Practices](#best-practices)
10. [References](#references)

---

## Overview

Statistical text mining uses the distributional properties of words — how often they appear, which words they appear with, and how discriminative they are across documents — to identify narrative-relevant patterns. Unlike Level 1 (pre-defined lexicons), Level 2 learns these patterns from the data itself.

### Key Principle

**Words that behave similarly in distribution are similarly in meaning** (distributional hypothesis). Narratives generate characteristic word distributions — "inflation" articles will systematically use different vocabulary than "sports" articles.

---

## Techniques

### TF-IDF (Term Frequency-Inverse Document Frequency)

The most widely used statistical weighting scheme:

```
TF-IDF(t, d) = TF(t, d) × IDF(t)

Where:
TF(t, d) = frequency of term t in document d
IDF(t) = log(N / df(t))
N = total number of documents
df(t) = number of documents containing term t
```

**Key insight:** Terms that appear frequently in few documents get high TF-IDF weights — they are *discriminative* for those documents.

### N-grams

Multi-word sequences capturing phrasal patterns:

| Type | Example | Narrative Value |
|------|---------|-----------------|
| Unigram | "inflation" | Single word |
| Bigram | "price hike" | Modifier + noun |
| Trigram | "cost of living" | Fixed phrase |
| Skip-gram | "inflation * rising" | Flexible patterns |

### PMI (Pointwise Mutual Information)

Measures how often words co-occur relative to chance:

```
PMI(w1, w2) = log(P(w1, w2) / (P(w1) × P(w2)))

PMI > 0: words co-occur more than expected by chance
PMI = 0: independent
PMI < 0: words co-occur less than expected
```

### Co-occurrence Networks

Graph where nodes are words and edges represent co-occurrence strength:

```
     inflation ──┬── prices
                 ├── supply chain
                 ├── central bank
                 └── food
```

### Chi-Square Feature Selection

Tests whether a term's distribution differs significantly across categories:

```python
from sklearn.feature_selection import chi2

chi2_scores, p_values = chi2(X, y)
# Higher scores = more discriminative terms
```

---

## Worked Example

### TF-IDF Feature Extraction

**Document:** "Inflation is rising because supply chain disruptions have increased food prices."

**TF-IDF Vector (top 5 features after fitting):**

| Term | TF | IDF | TF-IDF |
|------|----|-----|--------|
| supply chain | 1 | 8.5 | 8.5 |
| inflation | 1 | 7.2 | 7.2 |
| food prices | 1 | 6.8 | 6.8 |
| disruptions | 1 | 5.9 | 5.9 |
| rising | 1 | 4.1 | 4.1 |

### Classification

TF-IDF vector → Logistic Regression → Narrative probability:

```python
# Pseudocode
tfidf_vector = vectorizer.transform([document])
probability = classifier.predict_proba(tfidf_vector)[0, 1]
# probability = 0.94 (94% confident this is an economic narrative)
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Description |
|----------|-------------|
| **Data-driven** | Learns discriminative patterns — no manual lexicon needed |
| **Interpretable** | Top-weighted terms reveal *why* a document was classified as narrative X |
| **Fast to train** | Minutes for millions of documents |
| **Fast to predict** | Milliseconds per document at scale |
| **Strong baseline** | Often matches or approaches deep learning performance |
| **Well-understood** | Decades of methodology research |

### Weaknesses

| Weakness | Description | Mitigation |
|----------|-------------|------------|
| **Bag-of-words** | Ignores word order and syntax | Use n-grams (BENI uses 1-2 grams) |
| **No semantics** | "Price is high" ≠ "High price" semantically same | Use embeddings (L4) |
| **Sparse** | Each document has few non-zero features | Dimensionality reduction |
| **Vocabulary mismatch** | Same narrative, different words | Embedding expansion |
| **No causal understanding** | Cannot distinguish correlation from causation | Level 7+ |

---

## When to Use Level 2

| Scenario | Recommended | Alternative |
|----------|-------------|-------------|
| Classification baseline | ✅ **Level 2** (always start here) | — |
| Large-scale text classification | ✅ **Level 2** | L4 for marginal gains |
| Interpretable narrative index | ✅ **Level 2** (top terms per month) | — |
| Complex semantic tasks | ❌ Bag-of-words too limiting | L4 or L10 |
| Small datasets (<1K docs) | ❌ TF-IDF too sparse | L1 lexicon or L10 LLM |

---

## BENI Implementation Detail

### Code References

| File | Purpose | Key Details |
|------|---------|-------------|
| `pipelines/shared/models.py` | TF-IDF + LR pipeline factory | `TfidfVectorizer(80k, min_df=2, ngram=(1,2))` |
| `pipelines/BENI/experiment/beni_pilot/models.py` | BENI-specific model wrapper | Config integration |
| `pipelines/BENI/experiment/beni_pilot/train.py` | Training orchestrator | Supports TF-IDF + BanglaBERT |
| `pipelines/BENI/experiment/beni_pilot/data.py` | Data loaders | BNLP, Potrika, Potrika timeseries |
| `pipelines/BENI/experiment/beni_pilot/build_index.py` | Index construction | Monthly TF-IDF aggregation |
| `pipelines/BENI/experiment/beni_pilot/eval.py` | Evaluation | Classification metrics |
| `pipelines/BENI/exploration/evaluate_tfidf_index.py` | Macro validation | CPI/FX/reserve correlations |

### Model Configuration

```python
# From shared/models.py
def build_tfidf_logreg(max_features=80000, min_df=2, ngram_range=(1, 2)):
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=max_features,
            min_df=min_df,
            ngram_range=ngram_range,
            sublinear_tf=True,        # Use 1 + log(TF) instead of raw TF
            norm="l2",                 # Euclidean normalization
        )),
        ("clf", OneVsRestClassifier(
            LogisticRegression(
                class_weight="balanced",
                solver="liblinear",
                max_iter=1000,
                C=1.0,
            )
        )),
    ])
```

### Data Split Strategy

Time-based split (critical for time series validity):

| Split | Period | Size | Purpose |
|-------|--------|------|---------|
| Train | ≤ 2018-12 | ~70,000 | Model training |
| Validation | 2019-01 to 2019-12 | ~21,000 | Hyperparameter tuning |
| Test | ≥ 2020-01 | ~30,000 | Final evaluation |

### Results

| Task | Dataset | Accuracy | Macro F1 |
|------|---------|----------|----------|
| Topic classification | BNLP test | 89.4% | 0.860 |
| Economic relevance | BNLP test | 95.0% | 0.750 |
| **Economic relevance** | **Potrika timeseries** | **91.7%** | **0.894** |

### Index Construction

The narrative index is built by:

```
1. Train TF-IDF classifier on labeled articles
2. Predict economic_prob for all 120K articles
3. Group by year_month:
   economic_share = mean(binary predictions per month)
   mean_prob = mean(economic_prob per month)
   n_economic = sum(binary predictions per month)
4. Normalize: z-score or LLM calibration
```

### BENI Index Results

| Metric | Value |
|--------|-------|
| Monthly observations | 79 (Jun 2014 – Dec 2020) |
| Mean economic share | 38.9% |
| CPI level correlation | r = −0.75 (p < 0.001) |
| FX level correlation | r = −0.72 (p < 0.001) |
| Reserves level correlation | r = −0.77 (p < 0.05) |
| First-differenced CPI | r = −0.04 (not significant) |

---

## TF-IDF Deep Dive

### Why 80,000 Features?

For a Bangla news corpus, 80,000 features captures:
- All content words appearing in ≥2 documents
- Common bigrams ("supply chain", "interest rate")
- Domain-specific vocabulary (economic terms, policy names)
- Bangla-specific multi-word expressions

### Why Sublinear TF?

`sublinear_tf=True` uses `1 + log(TF)` instead of raw TF. This prevents very frequent terms (e.g., "বাংলাদেশ" = Bangladesh) from dominating:

```python
# Without sublinear TF: dominates because it appears in 60%+ of articles
# With sublinear TF: contribution grows logarithmically

# Example
tfidf_standard = count * idf        # Raw: 50 * 0.5 = 25
tfidf_sublinear = (1 + log(count)) * idf  # Sublinear: (1 + 3.9) * 0.5 = 2.45
```

### Understanding Top Features

The most discriminative features for "Economic" vs "Not Economic" in the BENI classifier:

**Top features for Economic class (highest coefficients):**
```
মূল্যস্ফীতি (inflation)
ডলার (dollar/exchange rate)
বাজেট (budget)
রিজার্ভ (reserves)
রপ্তানি (exports)
```

**Top features for Not Economic class:**
```
ক্রিকেট (cricket)
খেলা (sports)
বিনোদন (entertainment)
চলচ্চিত্র (cinema)
￼বিবাহ (wedding)
```

---

## Co-occurrence Networks

### Constructing a Narrative Co-occurrence Network

```python
from collections import defaultdict
import networkx as nx

def build_cooccurrence_network(documents, window=5, threshold=10):
    """Build a co-occurrence network from a list of documents."""
    G = nx.Graph()
    cooccurrences = defaultdict(int)

    for doc in documents:
        tokens = doc.split()
        for i, token in enumerate(tokens):
            for j in range(i+1, min(i+window, len(tokens))):
                pair = tuple(sorted([token, tokens[j]]))
                cooccurrences[pair] += 1

    for (w1, w2), count in cooccurrences.items():
        if count >= threshold:
            G.add_edge(w1, w2, weight=count)

    return G
```

### Interpretation

Clusters in the co-occurrence network reveal narrative themes:

```
Cluster 1 (Inflation narrative):
    inflation ↔ prices, supply chain, central bank, food

Cluster 2 (Trade narrative):
    exports ↔ garments, remittances, trade deficit, foreign exchange

Cluster 3 (Fiscal narrative):
    budget ↔ deficit, spending, tax, revenue, IMF
```

---

## Best Practices

### Feature Engineering

1. **Start with unigrams + bigrams** (BENI uses `ngram_range=(1,2)`)
2. **Remove very rare terms** (`min_df=2` removes singletons that cause overfitting)
3. **Remove very frequent terms** (`max_df=0.95` removes corpus-wide terms)
4. **Use sublinear TF scaling** for robust term weighting
5. **Normalize vectors** (L2 norm handles document length variation)

### Validation for Time Series

**CRITICAL: Never randomly split time series data.** Use time-based splits:

```python
# WRONG: Random split leaks future information
train, test = train_test_split(data, test_size=0.2, random_state=42)

# CORRECT: Time-based split preserves temporal order
train = data[data["date"] <= "2018-12-31"]
val = data[(data["date"] >= "2019-01-01") & (data["date"] <= "2019-12-31")]
test = data[data["date"] >= "2020-01-01"]
```

### Interpreting Weak Detrended Correlations

The BENI TF-IDF index shows strong level correlations with CPI (r = -0.75) but weak first-differenced correlations (r = -0.04). This could mean:

1. **Structural signal only:** TF-IDF captures long-run narrative shifts but not short-term noise
2. **Slow-moving narrative share:** Economic news share changes slowly; month-to-month variance is low
3. **Model limitation:** TF-IDF lacks the semantic precision to detect short-term narrative changes

**Diagnosis:** Compare against BanglaBERT (L4) — if BanglaBERT improves detrended correlations, the issue is model precision. If not, it's a structural feature of narrative indices.

---

## References

### Core Reading

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval.* Cambridge University Press.
  — Chapters 6 (TF-IDF) and 13 (Text Classification).

- Joachims, T. (1998). "Text Categorization with Support Vector Machines." *ECML*.
  — Foundational paper on statistical text classification.

- Blei, D. M. (2012). "Probabilistic Topic Models." *Communications of the ACM*, 55(4): 77–84.
  — Bridges Level 2 and Level 3.

### BENI-Specific

- Nabil, A. N. (2026). "TF-IDF Baseline Model." `pipelines/shared/models.py`
- Nabil, A. N. (2026). "BENI Pilot Index Results." `pipelines/BENI/experiment/beni_pilot/experiment_report.md`
- Nabil, A. N. (2026). "BENI Index Construction." `pipelines/BENI/experiment/beni_pilot/build_index.py`

### See Also

- Level 3: [Topic Modeling](L03_topic_modeling.md) — Latent structure beyond TF-IDF
- Level 4: [Embedding-Based Discovery](L04_embedding_based_discovery.md) — Semantic vectors
- Level 1: [Lexicon-Based Detection](L01_lexicon_based_detection.md) — Complementary approach

---

**Up:** [Methodologies Index](INDEX.md) | **Main:** [Narrative Extraction Methodologies](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
