> **Navigation:** [Documentation Portal](../../index.md) > [Research](../) > [Methodologies](./) > Level 4
>
> ---

# Level 4: Embedding-Based Narrative Discovery

> **Hierarchy:** Modern semantic clustering using dense vector representations.
> **BENI Status:** ⬜ Not Yet Implemented (BanglaBERT used for classification, not discovery)
> **Core Idea:** Represent documents as dense vectors in semantic space; cluster them to discover narratives.

---

## Table of Contents

1. [Overview](#overview)
2. [Embedding Models](#embedding-models)
3. [The Discovery Pipeline](#the-discovery-pipeline)
4. [Worked Example](#worked-example)
5. [Strengths & Weaknesses](#strengths--weaknesses)
6. [When to Use Level 4](#when-to-use-level-4)
7. [BENI Context & Recommendations](#beni-context--recommendations)
8. [Implementation Guide for BENI](#implementation-guide-for-beni)
9. [From Discovery to Narrative Index](#from-discovery-to-narrative-index)
10. [References](#references)

---

## Overview

Embedding-based narrative discovery represents documents as dense vectors in a high-dimensional semantic space, then uses clustering to group semantically similar documents. Unlike bag-of-words methods (L1, L2), embeddings capture meaning — "food prices rise," "grocery costs increase," and "higher market prices" map to nearby vectors despite zero lexical overlap.

### Key Principle

**Semantics, not keywords.** Embedding models are trained to place semantically similar texts near each other in vector space. This means narrative clusters can form around meaning rather than shared vocabulary.

### The Core Pipeline

```
Documents
    ↓
Embedding Model (SBERT/E5/BGE) → dense vectors
    ↓
Dimensionality Reduction (UMAP)
    ↓
Clustering (HDBSCAN)
    ↓
Narrative Clusters
    ↓
Human Labeling + Validation
```

---

## Embedding Models

### Comparison for BENI Use Case

| Model | Parameters | Languages | Bangla Quality | Dim | Best For |
|-------|-----------|-----------|----------------|-----|----------|
| **multilingual-E5-small** | 118M | 100+ | ⭐⭐⭐ | 384 | Fast, general purpose |
| **multilingual-E5-base** | 278M | 100+ | ⭐⭐⭐⭐ | 768 | Best quality/speed |
| **multilingual-E5-large** | 560M | 100+ | ⭐⭐⭐⭐⭐ | 1024 | Maximum quality |
| **BGE-m3** | 567M | 100+ | ⭐⭐⭐⭐⭐ | 1024 | Dense + sparse hybrid |
| **SBERT (distiluse-base)** | 134M | 50+ | ⭐⭐⭐ | 512 | Lightweight |
| **LaBSE** | 471M | 109 | ⭐⭐⭐⭐ | 768 | Cross-lingual retrieval |

### Why E5 for BENI

`intfloat/multilingual-e5-large` is recommended because:

1. **Best-in-class multilingual performance** on Bengali
2. **Supports retrieval-augmented workflows** (query: "passage: ...")
3. **Native 100+ language support** — works for all XENI target languages
4. **Strong benchmark scores** on multilingual semantic similarity

```python
# Usage
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-large")

# E5 requires prefixing
documents = [f"passage: {doc}" for doc in raw_documents]
embeddings = model.encode(documents, normalize_embeddings=True)
```

---

## The Discovery Pipeline

### Step 1: Document Embedding

```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-small")
embeddings = model.encode(
    documents,
    show_progress_bar=True,
    batch_size=64,
    normalize_embeddings=True,
    convert_to_numpy=True,
)
```

### Step 2: Dimensionality Reduction

UMAP preserves local structure while reducing to a clusterable dimensionality:

```python
import umap.umap_ as umap

reducer = umap.UMAP(
    n_neighbors=15,        # Balance local/global structure
    n_components=5,         # 5-10 dimensions is clusterable
    min_dist=0.0,           # Allow tight clusters
    metric="cosine",        # Cosine distance for normalized embeddings
    random_state=42,
)
projection = reducer.fit_transform(embeddings)
```

### Step 3: Clustering

HDBSCAN finds clusters of varying density without pre-specifying k:

```python
import hdbscan

clusterer = hdbscan.HDBSCAN(
    min_cluster_size=15,    # Minimum documents per narrative
    min_samples=5,          # Conservative clustering
    metric="euclidean",
    prediction_data=True,   # New document assignment
)
cluster_labels = clusterer.fit_predict(projection)

# -1 = outlier (no narrative cluster assigned)
```

### Step 4: Topic Representation

Extract representative terms for each cluster:

```python
from bertopic import BERTopic  # reuses c-TF-IDF

# Or manually:
from sklearn.feature_extraction.text import TfidfVectorizer

# Per-cluster TF-IDF
cluster_docs = {label: [] for label in set(cluster_labels)}
for doc, label in zip(documents, cluster_labels):
    if label != -1:
        cluster_docs[label].append(doc)

for label, docs in cluster_docs.items():
    vectorizer = TfidfVectorizer(max_features=20)
    tfidf = vectorizer.fit_transform(docs)
    # Top terms = narrative cluster keywords
```

---

## Worked Example

### Bangla News Narrative Discovery

**Input:** 10,000 Bangla news articles (varied topics)

**Pipeline output:** 14 narrative clusters + outliers

| Cluster | Size | Top Terms (Translated) | Narrative Label |
|---------|------|----------------------|-----------------|
| **0** | 1,240 | inflation, price, food, market, rise | Inflation narrative |
| **1** | 980 | export, garment, RMG, trade, factory | Garment trade narrative |
| **2** | 720 | remittance, worker, abroad, dollar | Remittance narrative |
| **3** | 650 | election, vote, government, party | Political narrative |
| **4** | 540 | bank, loan, interest, credit | Banking narrative |
| **5** | 480 | flood, climate, crop, farmer | Climate/agri narrative |
| **6** | 420 | reserve, forex, dollar, import | Reserves narrative |
| **7** | 380 | energy, gas, power, load-shedding | Energy crisis |
| **8** | 350 | budget, tax, revenue, spending | Fiscal narrative |
| **9** | 310 | stock, share, DSE, investment | Market narrative |
| **10–13** | 200-300 | Various mixed topics | Requires expert review |

### Interpreting Clusters

Each cluster must be validated as a *narrative* (not just a topic):

```json
{
    "cluster_0": {
        "topic_words": ["মূল্যস্ফীতি", "দাম", "খাদ্য"],
        "narrative": true,                // Has causal structure?
        "causal_claims": ["supply → prices", "demand → inflation"],
        "actors": ["consumers", "government", "central bank"],
        "stance": "negative",
        "validated": false
    }
}
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Description |
|----------|-------------|
| **Semantic understanding** | Captures meaning, not just keywords |
| **Multilingual by design** | E5/BGE support all XENI languages |
| **Zero-shot** | No training data needed for discovery |
| **Handles synonyms** | Same concept, different words → same cluster |
| **Outlier detection** | HDBSCAN naturally identifies documents that don't fit established narratives |
| **Hierarchical** | Nested clusters reveal granularity |

### Weaknesses

| Weakness | Description | Mitigation |
|----------|-------------|------------|
| **Black box** | Embeddings are not directly interpretable | c-TF-IDF for cluster keywords |
| **Cluster validation** | No guarantee clusters are "narratives" | Human validation protocol |
| **Sensitive to parameters** | min_cluster_size affects granularity | Sweep parameters, compare stability |
| **Computational cost** | Large models, large corpora | Use efficient models (E5-small) |
| **Temporal stability** | Embeddings shift as language evolves | Regular model updates |

---

## When to Use Level 4

| Scenario | Recommended | Alternative |
|----------|-------------|-------------|
| Exploratory discovery in new corpus | ✅ **Level 4** | — |
| Multilingual narrative discovery | ✅ **Level 4** (E5-native) | — |
| Fine-grained cluster analysis | ✅ **Level 4** | — |
| Pre-defined narrative categories | ❌ Better to use L10 | — |
| Interpretability critical | ❌ Lexicon (L1) more transparent | — |
| Small corpus (<1K docs) | ❌ Clustering unreliable | Lexicon (L1) or manual (L0) |

---

## BENI Context & Recommendations

**Current status: ⬜ Not Yet Implemented**

The closest BENI has to Level 4 is the BanglaBERT classifier — which uses transformer embeddings for *binary classification* (economic vs. not), not for *narrative discovery*.

### What BENI Needs

1. **Document embedding layer** — Pre-compute E5 embeddings for all 120K articles
2. **Narrative clustering pipeline** — UMAP + HDBSCAN for discovery
3. **Seed with existing lexicons** — Use `narrative.py` lexicons as cluster priors
4. **Temporal cluster tracking** — How do clusters change across 79 months?
5. **Cluster → index bridge** — Convert cluster membership to narrative prevalence time series

### Implementation Priority

**Phase 1 — Embedding infrastructure:**
```python
# Pre-compute once, use everywhere
embeddings = e5_model.encode(all_beni_articles)
np.save("beni_e5_embeddings.npy", embeddings)
```

**Phase 2 — Narrative discovery:**
```python
projection = UMAP().fit_transform(embeddings)
clusters = HDBSCAN().fit_predict(projection)
```

**Phase 3 — Temporal tracking:**
```python
# Per-month clustering or cluster assignment
monthly_clusters = assign_to_clusters(embeddings, timestamps)
monthly_narrative_prevalence = compute_prevalence(monthly_clusters)
```

---

## Implementation Guide for BENI

### Prerequisites

```bash
pip install sentence-transformers umap-learn hdbscan bertopic
```

### Full Pipeline

```python
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
import hdbscan
from bertopic import BERTopic

class NarrativeDiscovery:
    def __init__(self, model_name="intfloat/multilingual-e5-small"):
        self.model = SentenceTransformer(model_name)
        self.reducer = umap.UMAP(n_neighbors=15, n_components=5, metric="cosine")
        self.clusterer = None

    def embed(self, documents, batch_size=64):
        texts = [f"passage: {doc}" for doc in documents]
        return self.model.encode(texts, batch_size=batch_size, normalize_embeddings=True)

    def discover(self, embeddings, min_cluster_size=15):
        projection = self.reducer.fit_transform(embeddings)
        self.clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            min_samples=5,
            metric="euclidean",
            prediction_data=True,
        )
        return self.clusterer.fit_predict(projection)

    def assign_new(self, new_embeddings):
        """Assign new documents to existing narrative clusters."""
        if self.clusterer is None:
            raise ValueError("Must call discover() first")
        return hdbscan.approximate_predict(self.clusterer, new_embeddings)[0]

# Usage
discoverer = NarrativeDiscovery()
embeddings = discoverer.embed(beni_articles)
narrative_labels = discoverer.discover(embeddings, min_cluster_size=30)
```

### Integration with LLM Labels

```python
# After clustering, use LLM to validate and label each cluster
for cluster_id in set(narrative_labels):
    if cluster_id == -1:
        continue

    cluster_docs = [beni_articles[i] for i, l in enumerate(narrative_labels) if l == cluster_id]

    # Sample a few representative documents
    sample = cluster_docs[:5]

    # LLM prompt
    llm_label = llm_extract_narrative_label(sample)

    # Store
    cluster_labels[cluster_id] = llm_label
```

---

## From Discovery to Narrative Index

The key innovation: convert narrative clusters into time series indices.

### Per-Narrative Monthly Prevalence

```python
# For each narrative cluster, compute its share of all articles per month
narrative_index = df.groupby(["year_month", "narrative_cluster"]).size()
narrative_index = narrative_index / df.groupby("year_month").size()

# Result: time series for each narrative
# 2014-06: inflation=0.18, trade=0.12, politics=0.25, ...
# 2014-07: inflation=0.19, trade=0.11, politics=0.24, ...
```

### New BENI Sub-Indices

| Index | Source Cluster |
|-------|---------------|
| BENI Inflation Narrative Index | Cluster with inflation-related terms |
| BENI Trade Narrative Index | Cluster with export/import/garment terms |
| BENI Reserves Narrative Index | Cluster with forex/reserve terms |
| BENI Political Economy Index | Cluster with election/policy terms |

---

## References

### Core Reading

- Reimers, N. & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks." *EMNLP 2019*.
- Wang, L. et al. (2024). "Multilingual E5 Text Embeddings: A Technical Report." arXiv: `2402.05672`.
- McInnes, L. & Healy, J. (2018). "UMAP: Uniform Manifold Approximation and Projection." *JOSS*.
- McInnes, L. et al. (2017). "hdbscan: Hierarchical density based clustering." *JOSS*.
- Grootendorst, M. (2022). "BERTopic: Neural topic modeling with a class-based TF-IDF procedure." arXiv: `2203.05794`.

### BENI-Specific

- Nabil, A. N. (2026). "Narrative Force Lexicon." `pipelines/BENI/experiment/beni_pilot/narrative.py`
  — Use existing lexicons as cluster seed terms.

### See Also

- Level 3: [Topic Modeling](L03_topic_modeling.md) — BERTopic bridges L3 and L4
- Level 10: [LLM-Based Extraction](L10_llm_based_extraction.md) — LLM label validation
- Level 8: [Narrative Graphs](L08_narrative_networks_graphs.md) — Graph from clusters

---

**Up:** [Methodologies Index](INDEX.md) | **Main:** [Narrative Extraction Methodologies](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
