> **Navigation:** [Documentation Portal](../../index.md) > [Research](../) > [Methodologies](./) > Level 3
>
> ---

# Level 3: Topic Modeling

> **Hierarchy:** First major step toward latent narrative discovery.
> **BENI Status:** 🔄 Planned — BERTopic / keyATM mentioned in roadmap
> **Core Idea:** Discover latent themes (topics) from word co-occurrence patterns without pre-defining them.

---

## Table of Contents

1. [Overview](#overview)
2. [Methods](#methods)
3. [Worked Example](#worked-example)
4. [Strengths & Weaknesses](#strengths--weaknesses)
5. [When to Use Level 3](#when-to-use-level-3)
6. [Method Comparison](#method-comparison)
7. [BENI Context](#beni-context)
8. [BERTopic Deep Dive](#bertopic-deep-dive)
9. [Dynamic Topic Models for Narrative Tracking](#dynamic-topic-models-for-narrative-tracking)
10. [Best Practices](#best-practices)
11. [References](#references)

---

## Overview

Topic modeling discovers latent themes (topics) from word co-occurrence patterns across a corpus. Unlike Level 1 (pre-defined lexicons) or Level 2 (labeled classification), topic modeling is **unsupervised** — it finds structure without needing pre-existing labels.

### Key Insight

**Topics emerge from data.** If a set of words consistently co-occurs across documents, those documents likely share a common theme. Topic modeling makes this pattern explicit.

### Topic vs. Narrative

A topic is **a cluster of co-occurring words.** A narrative is **a structured explanation.** Topic modeling finds the former, which may approximate the latter:

```
Topic: {oil, energy, gas, war, Russia, supply}
→ Human label: "Energy shock narrative"
→ But: lacks causality, actors, temporal structure
```

Moving from topics to narratives requires Level 5+.

---

## Methods

### LDA (Latent Dirichlet Allocation)

The classic topic model. Each document is a mixture of topics; each topic is a distribution over words.

```python
from gensim.models import LdaModel
from gensim.corpora import Dictionary

# Create dictionary and corpus
dictionary = Dictionary(tokenized_docs)
corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

# Train LDA
lda = LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=15,
    passes=10,
    alpha="auto",
    eta="auto",
)

# Get topics
topics = lda.print_topics(num_words=10)
```

**Hyperparameters:**
| Parameter | Effect | Common Range |
|-----------|--------|--------------|
| `num_topics` | Number of topics to discover | 5–50 |
| `alpha` | Document-topic sparsity | 0.01–1.0 or "auto" |
| `eta` | Topic-word sparsity | 0.01–1.0 or "auto" |
| `passes` | Training iterations | 10–1000 |

### HDP (Hierarchical Dirichlet Process)

Nonparametric variant that infers the number of topics from data:

```python
from gensim.models import HdpModel

hdp = HdpModel(corpus=corpus, id2word=dictionary)
# Number of topics is inferred automatically
```

**Trade-off:** No need to specify k, but computationally expensive for large corpora.

### NMF (Non-negative Matrix Factorization)

Matrix factorization approach that produces more focused, less overlapping topics than LDA:

```python
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(documents)

nmf = NMF(n_components=15, random_state=42)
W = nmf.fit_transform(X)       # Document-topic matrix
H = nmf.components_            # Topic-term matrix

# Top words per topic
feature_names = vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(H):
    top_words = [feature_names[i] for i in topic.argsort()[:-10-1:-1]]
```

**Best for:** Short text, focused topics, where non-negativity is natural (word counts).

### Dynamic Topic Models (DTM)

Temporal extension that tracks topic evolution over time:

```
Time 1: {oil, price, supply, OPEC, gas}
Time 2: {oil, price, demand, China, supply}
Time 3: {oil, price, war, Russia, sanctions}
```

Same topic ("energy prices") but different associated terms as context evolves.

### BERTopic

Modern embedding-based approach (bridges L3 and L4):

```
Documents → Embeddings → UMAP → HDBSCAN → c-TF-IDF → Topics
```

See [BERTopic Deep Dive](#bertopic-deep-dive) below.

---

## Worked Example

### Corpus: Bangla Economic News (2014-2020)

After running LDA with k=10:

| Topic # | Top Words (Translated) | Human Label |
|---------|----------------------|-------------|
| **1** | inflation, price, food, market, rise | Inflation narrative |
| **2** | export, garment, trade, readymade, RMG | Garment trade narrative |
| **3** | remittance, worker, abroad, income, dollar | Remittance narrative |
| **4** | election, government, policy, opposition, bill | Political economy |
| **5** | bank, loan, interest, credit, default | Banking narrative |
| **6** | budget, tax, revenue, spending, deficit | Fiscal policy |
| **7** | reserve, forex, dollar, import, pressure | Reserve crisis narrative |
| **8** | energy, power, gas, electricity, load-shedding | Energy crisis |
| **9** | climate, flood, crop, agriculture, farmer | Agricultural narrative |
| **10** | stock, market, investment, DSE, share | Stock market narrative |

### Labeling Topics as Narratives

A human reviews each topic and assigns a narrative label:

```json
{
    "topic_1": {
        "label": "Inflation narrative",
        "keywords": ["মূল্যস্ফীতি", "দাম", "খাদ্য", "বাজার"],
        "prevalence": 0.18,
        "trend": "increasing 2019–2020"
    }
}
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Description |
|----------|-------------|
| **Unsupervised** | No labels needed — discovers structure from raw text |
| **Interpretable** | Top words per topic are human-readable |
| **Temporal tracking** | DTM shows how narratives evolve |
| **Scalable** | LDA/NMF scale to millions of documents |
| **Domain-agnostic** | Same method works for economics, health, climate |

### Weaknesses

| Weakness | Description | Mitigation |
|----------|-------------|------------|
| **Topic ≠ Narrative** | Lacks causality, actors, structure | Level 5+ for narratives |
| **k selection** | LDA requires specifying topic count | HDP or coherence optimization |
| **Sensitivity** | Different runs → different topics | Set seed, multiple runs |
| **Bag-of-words** | Ignores word order and syntax | BERTopic (L4 embeddings) |
| **Static vocabulary** | Cannot handle emerging terms easily | DTM or regular retraining |

---

## When to Use Level 3

| Scenario | Recommended | Alternative |
|----------|-------------|-------------|
| Unknown corpus structure | ✅ **Level 3** (exploratory) | — |
| Tracking topic evolution | ✅ **Level 3** (DTM) | — |
| Generating topic labels for human review | ✅ **Level 3** | — |
| Pre-defined narrative categories | ❌ Better to use L1/L10 labels | Supervised classification |
| Causal narrative extraction | ❌ Requires Level 7+ | — |

---

## Method Comparison

| Method | Topic Quality | Speed | Interpretability | Temporal | k Needed |
|--------|--------------|-------|------------------|----------|----------|
| **LDA** | Good | Fast | High | Via DTM | Yes |
| **HDP** | Good | Slow | High | No | No |
| **NMF** | Very Good | Fast | Very High | No | Yes |
| **DTM** | Good | Slow | High | Yes | Yes |
| **BERTopic** | Excellent | Moderate | Moderate | Planned | No |

### Recommendation for BENI

For the BENI pipeline, BERTopic is preferred because:
1. Multilingual embeddings (E5, BGE) work well for Bangla
2. No need to pre-specify topic count
3. Produces tighter, more coherent topics than LDA
4. Can be seeded with existing lexicons

---

## BENI Context

**Current status: 🔄 Planned (exploratory)**

The BENI Roadmap mentions two topic modeling approaches:

> *"keyATM for seeded narrative themes"* (primary)
> *"BERTopic as an exploratory robustness check if embeddings behave well"* (secondary)

Neither has been implemented in the pipeline code yet.

### keyATM (Seeded Topic Model)

keyATM allows seeding topic models with prior knowledge — perfect for BENI:

```python
# Seeded keywords for each narrative
seeded_keywords = {
    "inflation": ["মূল্যস্ফীতি", "দাম", "খাদ্য মূল্য"],
    "exchange_rate": ["ডলার", "বিনিময় হার", "রিজার্ভ"],
    "trade": ["রপ্তানি", "আমদানি", "বাণিজ্য"],
    # ...
}

# keyATM uses these to guide topic discovery
# Remaining topics are learned unsupervised ("residual" topics)
```

### Why BERTopic for BENI 2.0

1. **Multilingual embeddings** work natively with Bangla
2. **Dynamic topics** via pre-computed embeddings across time periods
3. **Hierarchical topics** reveal nested structure ("inflation" → "food inflation" → "rice prices")
4. **c-TF-IDF topic representations** are human-readable
5. **Outlier handling** — documents that don't fit any topic remain unassigned rather than forced

---

## BERTopic Deep Dive

### Pipeline

```mermaid
Documents
    ↓
Sentence Embeddings (SBERT/E5/BGE)
    ↓
Dimensionality Reduction (UMAP)
    ↓
Clustering (HDBSCAN)
    ↓
Topic Representation (c-TF-IDF)
    ↓
Post-processing (merge, reduce, label)
```

### Step-by-Step Implementation

```python
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
import hdbscan
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

# 1. Load multilingual embeddings
embedding_model = SentenceTransformer("intfloat/multilingual-e5-small")

# 2. Create topic model
vectorizer_model = CountVectorizer(
    stop_words="bengali",
    ngram_range=(1, 2),
    min_df=5,
)

topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap.UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric="cosine",
    ),
    hdbscan_model=hdbscan.HDBSCAN(
        min_cluster_size=15,
        min_samples=5,
        metric="euclidean",
        prediction_data=True,
    ),
    vectorizer_model=vectorizer_model,
    verbose=True,
)

# 3. Fit and transform
topics, probabilities = topic_model.fit_transform(documents)

# 4. Inspect topics
topic_model.get_topic_info()       # Topic prevalence
topic_model.get_topic(0)           # Top words for topic 0
topic_model.visualize_barchart()   # Topic-term bar charts
topic_model.visualize_hierarchy()  # Hierarchical topic structure
```

### Dynamic Topic Tracking

```python
# Pre-compute embeddings once, then track over time
topics_over_time = topic_model.topics_over_time(
    docs=documents,
    timestamps=timestamps,
    nr_bins=79,  # 79 months
)
topic_model.visualize_topics_over_time(topics_over_time)
```

### Seeding with Existing Lexicons

```python
# Use BENI's existing lexicons as seed topics
seed_topic_list = [
    ["মূল্যস্ফীতি", "দাম", "খাদ্য মূল্য", "ভোক্তা মূল্য"],  # Inflation
    ["ডলার", "টাকা", "বিনিময় হার", "রিজার্ভ"],               # Exchange rate
    ["রপ্তানি", "আমদানি", "বাণিজ্য", "এলসি"],                # Trade
    ["বাজেট", "কর", "রাজস্ব", "ঘাটতি"],                       # Fiscal
]

topic_model = BERTopic(
    embedding_model=embedding_model,
    seed_topic_list=seed_topic_list,
)
```

---

## Dynamic Topic Models for Narrative Tracking

### The DTM Approach

Dynamic Topic Models (DTM) divide time into slices and allow topic distributions to evolve:

```python
# Pseudocode for DTM approach
time_slices = [documents_by_year[year] for year in sorted(years)]
dtm = DtmModel(corpus=corpus, time_slices=time_slices, num_topics=10)

# For topic k:
# Topic k in 2014: {oil, price, supply, stable}
# Topic k in 2020: {oil, price, war, sanctions}
# → Same topic, different framing as context evolved
```

### Narrative Applications

1. **Narrative emergence**: When does a topic first appear? (e.g., "gig economy" in Bangla news)
2. **Narrative drift**: Does "inflation" shift from "demand-pull" to "cost-push" framing?
3. **Narrative competition**: Which topics dominate during crisis vs. stable periods?

---

## Best Practices

### Choosing k

| Method | Approach |
|--------|----------|
| **Coherence score** | `CoherenceModel(model, texts, dictionary, coherence='c_v')` |
| **Perplexity** | Lower is better (but can be misleading) |
| **Visual inspection** | Are topics coherent and distinct? |
| **Downstream task** | What k optimizes your eventual goal? |

### Preprocessing for Topic Models

```python
def preprocess_for_topic_modeling(documents):
    """BENI-relevant preprocessing for topic modeling."""
    for doc in documents:
        # Remove punctuation (BENI-specific)
        doc = bangla_punct_re.sub(" ", doc)
        # Remove very short documents
        if len(doc.split()) < 5:
            continue
        # Remove numbers (usually not narrative-relevant)
        doc = re.sub(r'\d+', '', doc)
        yield doc
```

### Interpretation Protocol

For economic narratives, always have a domain expert:

1. **Review top words** for each topic
2. **Read representative documents** (highest topic probability)
3. **Assign narrative label** — is this a causal story or just a theme?
4. **Document edge cases** — topics that mix multiple narratives
5. **Release topic labels** with the dataset for reproducibility

---

## References

### Core Reading

- Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). "Latent Dirichlet Allocation." *Journal of Machine Learning Research*, 3: 993–1022.
  — The original LDA paper.

- Blei, D. M. & Lafferty, J. D. (2006). "Dynamic Topic Models." *ICML*.
  — DTM for tracking topic evolution over time.

- Grootendorst, M. (2022). "BERTopic: Neural topic modeling with a class-based TF-IDF procedure." arXiv: `2203.05794`.
  — Modern embedding-based topic modeling.

- Lee, M. et al. (2017). "keyATM: Keyword-Assisted Topic Models." arXiv: `1709.00679`.
  — Seeded topic modeling with prior keywords.

### BENI-Specific

- Nabil, A. N. (2026). "BENI Roadmap." `pipelines/BENI/management/BENI_ROADMAP.md`
  — References keyATM and BERTopic for Phase 3.

### See Also

- Level 4: [Embedding-Based Narrative Discovery](L04_embedding_based_discovery.md) — Embeddings + clustering
- Level 2: [Statistical Text Mining](L02_statistical_text_mining.md) — TF-IDF foundation

---

**Up:** [Methodologies Index](INDEX.md) | **Main:** [Narrative Extraction Methodologies](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
