> **Navigation:** [Documentation Portal](../../index.md) > [Research](../) > [Methodologies](./) > Level 9
>
> ---

# Level 9: RELATIO-Style Narrative Extraction

> **Hierarchy:** Cross-document entity-relation triple extraction and narrative grouping — inspired by the RELATIO framework (Ash, Gauthier & Widmer, 2023).
> **BENI Status:** ⬜ Not Yet Implemented
> **Core Idea:** Extract structured (actor, action, target) triples from text, aggregate them across documents, and group into coherent narratives via clustering.

---

## Table of Contents

1. [Overview](#overview)
2. [The RELATIO Framework](#the-relation-framework)
3. [Triple Extraction Methods](#triple-extraction-methods)
4. [Entity Clustering and Narrative Grouping](#entity-clustering-and-narrative-grouping)
5. [Cross-Document Aggregation](#cross-document-aggregation)
6. [Temporal Narrative Tracking](#temporal-narrative-tracking)
7. [Worked Example](#worked-example)
8. [Strengths & Weaknesses](#strengths--weaknesses)
9. [When to Use Level 9](#when-to-use-level-9)
10. [BENI Implementation Guide](#beni-implementation-guide)
11. [References](#references)

---

## Overview

RELATIO-style extraction represents a paradigm shift from document-level narrative classification to **narrative component extraction**. Rather than asking "Is this article about inflation?", it extracts atomic narrative elements — who did what to whom — and re-assembles them into narratives across thousands of documents.

### Core Idea

```
Documents (millions)
    ↓
Entity-Relation Triples: (Actor, Action, Target)
    ↓
Entity Clustering: "Government" = "Govt." = "Administration"
    ↓
Narrative Grouping: Related triples → Narrative structure
    ↓
Temporal Indexing: Narrative prevalence over time
```

### Key Distinction from Other Levels

| Level | Output | Unit of Analysis |
|-------|--------|-----------------|
| L2 (TF-IDF) | Word frequencies | Document → category |
| L4 (Embedding) | Semantic clusters | Document → cluster |
| L7 (Causal) | Cause-effect pairs | Sentence → claim |
| **L9 (RELATIO)** | **Actor-Action-Target triples** | **Document → component** |
| L10 (LLM) | Structured extraction | Document → schema |

---

## The RELATIO Framework

### Original RELATIO (Ash, Gauthier & Widmer, 2023)

RELATIO extracts **Actor-Verb-Patient (AVP)** triples from text using unsupervised dependency parsing:

```
[The government] [increased] [spending]
     Actor         Verb        Patient
```

These triples are then:
1. Clustered by entity similarity (embedding-based)
2. Aggregated across documents to find dominant narrative patterns
3. Tracked over time for narrative prevalence measurement

### Extended for Economics: AVP + SVO + Causal

For economic narrative extraction, the framework extends naturally:

| Triple Type | Components | Example |
|-------------|------------|---------|
| **AVP** (Actor-Verb-Patient) | Subject → Predicate → Object | Government → increased → spending |
| **SVO** (Subject-Verb-Object) | Agent → Action → Target | Central bank → raised → rates |
| **Causal** (Cause-Effect) | Cause → Link → Effect | Spending → causes → inflation |
| **Stance** (Actor-Stance-Target) | Evaluator → Stance → Target | Media → blames → government |

### Why RELATIO Matters for Economics

Economic narratives are naturally **compositional**:

> "The government increased spending, which caused inflation, and the central bank responded by raising rates."

This single sentence contains three triples:

```
(Government, increased, spending)
(spending, causes, inflation)
(central bank, raised, rates)
```

RELATIO-style extraction recovers all three, then aggregates across documents to answer questions like:
- In Q3 2024, which actor appears most frequently as a causal agent?
- Does "government" appear more with "spending" or "reform"?
- Which action verbs co-occur with "inflation" most frequently?

---

## Triple Extraction Methods

### Method 1: Dependency Parse Triples

```python
import spacy

nlp = spacy.load("en_core_web_trf")

def extract_avp_triples(sentence):
    """Extract Actor-Verb-Patient triples using dependency parsing."""
    doc = nlp(sentence)
    triples = []

    for token in doc:
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            # Find subject (actor)
            subjects = [child for child in token.children
                       if child.dep_ in ("nsubj", "nsubjpass")]
            # Find object (patient)
            objects = [child for child in token.children
                      if child.dep_ in ("dobj", "pobj", "attr")]

            for subj in subjects:
                for obj in objects:
                    triples.append({
                        "actor": subj.text,
                        "action": token.lemma_,
                        "target": obj.text,
                        "sentence": sentence,
                    })
    return triples
```

### Method 2: OpenIE Triples

```python
from openie import StanfordOpenIE

def extract_openie_triples(text):
    """Extract (subject, relation, object) triples using OpenIE."""
    with StanfordOpenIE() as client:
        triples = client.annotate(text)
        # triples: [{"subject": "...", "relation": "...", "object": "..."}]
    return triples
```

### Method 3: LLM-Based Triple Extraction

The most practical approach for Bangla (where dependency parsers are limited):

```python
TRIPLE_PROMPT = """
Extract ALL (actor, action, target) triples from this Bangla economic news article.

For each triple identify:
1. ACTOR: Who performed the action? (person, organization, concept)
2. ACTION: What did they do? (verb phrase)
3. TARGET: Who or what was affected?
4. CONFIDENCE: How clearly is this stated? (0.0-1.0)
5. STANCE: Is this portrayed as positive, negative, or neutral?

Economic triples only. Return as JSON array.

Article: {text}
"""

def llm_triple_extraction(text, llm_client):
    prompt = TRIPLE_PROMPT.format(text=text[:4000])
    response = llm_client(prompt)
    return json.loads(response)
```

### Method Comparison

| Method | Language Support | Precision | Recall | Cost | BENI Suitability |
|--------|-----------------|-----------|--------|------|-----------------|
| **Dependency Parse** | English only | High | Medium | Free | ❌ No Bangla model |
| **OpenIE** | English only | Medium | High | Free | ❌ No Bangla support |
| **LLM (Claude/GPT)** | All languages (zero-shot) | High | High | API cost | ✅ Best for Bangla |
| **Rule-based** | Any language | High | Low | Free | ✅ Simple baseline |

---

## Entity Clustering and Narrative Grouping

Raw triples contain surface-form variation: "government," "Govt.," "administration," "Bangladesh government" all refer to the same entity. Entity clustering resolves these into canonical forms.

### Entity Resolution Pipeline

```python
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN

class EntityResolver:
    """Cluster surface-form entities into canonical groups."""

    def __init__(self, model_name="intfloat/multilingual-e5-small"):
        self.model = SentenceTransformer(model_name)
        self.entity_clusters = {}

    def extract_entities_from_triples(self, triples):
        """Collect all unique actor and target strings from triples."""
        entities = set()
        for t in triples:
            entities.add(t["actor"])
            entities.add(t["target"])
        return list(entities)

    def cluster_entities(self, entity_strings, eps=0.3):
        """Cluster similar entity strings using embedding similarity."""
        embeddings = self.model.encode(
            [f"passage: {e}" for e in entity_strings],
            normalize_embeddings=True
        )
        clustering = DBSCAN(eps=eps, min_samples=1, metric="cosine")
        labels = clustering.fit_predict(embeddings)

        # Map: canonical name → list of surface forms
        clusters = {}
        for entity, label in zip(entity_strings, labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(entity)

        # Pick shortest/most frequent as canonical
        self.entity_clusters = {
            min(forms, key=len): forms
            for forms in clusters.values()
        }
        return self.entity_clusters

    def resolve(self, entity_string):
        """Map surface form to canonical entity name."""
        for canonical, forms in self.entity_clusters.items():
            if entity_string in forms:
                return canonical
        return entity_string  # Unknown entity
```

### Narrative Grouping

Once entities are resolved, related triples are grouped into narratives:

```python
class NarrativeGrouper:
    """Group related triples into coherent narrative structures."""

    def __init__(self):
        self.narratives = {}  # narrative_id → {triples, label, metadata}

    def group_by_shared_actor(self, triples, min_shared=3):
        """Group triples that share the same actor."""
        actor_groups = {}
        for triple in triples:
            actor = triple["resolved_actor"]
            if actor not in actor_groups:
                actor_groups[actor] = []
            actor_groups[actor].append(triple)

        # Filter: keep actors with min_shared+ triples
        return {
            actor: group for actor, group in actor_groups.items()
            if len(group) >= min_shared
        }

    def group_by_causal_chain(self, triples):
        """Connect triples where target of one is actor of another."""
        G = nx.DiGraph()
        for triple in triples:
            G.add_edge(triple["resolved_actor"],
                      triple["resolved_target"],
                      label=triple["action"],
                      triple_id=triple["id"])

        # Find chains
        chains = []
        for node in G.nodes():
            for successor in G.successors(node):
                for grandchild in G.successors(successor):
                    chains.append({
                        "chain": [node, successor, grandchild],
                        "triples": [
                            G.get_edge_data(node, successor),
                            G.get_edge_data(successor, grandchild),
                        ],
                    })
        return chains
```

---

## Cross-Document Aggregation

The power of RELATIO-style extraction: aggregating triples across millions of documents to reveal collective narrative structures.

### Triple Frequency Matrix

```python
def build_actor_action_matrix(triples_by_document):
    """
    Build (actor × action) frequency matrix across all documents.

    Returns:
        pd.DataFrame: actors × actions, values = co-occurrence count
    """
    rows = []
    for doc_id, triples in triples_by_document.items():
        for triple in triples:
            rows.append({
                "doc_id": doc_id,
                "actor": triple["resolved_actor"],
                "action": triple["action"],
                "target": triple["resolved_target"],
            })

    df = pd.DataFrame(rows)
    matrix = df.pivot_table(
        index="actor", columns="action", aggfunc="size", fill_value=0
    )
    return matrix
```

### Narrative Co-Occurrence Network

```python
def build_narrative_cooccurrence_network(triples_by_document):
    """
    Build graph where nodes are triples, edges represent co-occurrence
    in the same document.

    Returns networkx Graph for community detection.
    """
    G = nx.Graph()

    for doc_id, triples in triples_by_document.items():
        # Create representative labels for each triple
        triple_labels = [
            f"{t['resolved_actor']} → {t['action']} → {t['resolved_target']}"
            for t in triples
        ]

        # Connect all triples co-occurring in this document
        for i, label_a in enumerate(triple_labels):
            G.add_node(label_a)
            for label_b in triple_labels[i+1:]:
                if G.has_edge(label_a, label_b):
                    G[label_a][label_b]["weight"] += 1
                else:
                    G.add_edge(label_a, label_b, weight=1)

    return G
```

### Dominant Narrative Identification

```python
def identify_dominant_narratives(matrix, top_k=10):
    """Find the most frequently occurring (actor, action) pairs."""
    # Flatten the matrix
    pairs = matrix.stack().reset_index()
    pairs.columns = ["actor", "action", "frequency"]
    return pairs.sort_values("frequency", ascending=False).head(top_k)
```

---

## Temporal Narrative Tracking

### Monthly Narrative Prevalence

```python
def temporal_narrative_index(triples_by_document, freq="M"):
    """
    Compute monthly prevalence of each (actor, action) pair.

    Returns:
        pd.DataFrame: index = time periods, columns = narrative pairs
    """
    records = []
    for doc_id, triples in triples_by_document.items():
        date = doc_id_to_date[doc_id]
        period = pd.Timestamp(date).to_period(freq)
        for triple in triples:
            narrative_key = f"{triple['resolved_actor']}_{triple['action']}"
            records.append({
                "period": period,
                "narrative": narrative_key,
                "count": 1,
            })

    df = pd.DataFrame(records)
    pivot = df.pivot_table(
        index="period", columns="narrative",
        values="count", aggfunc="sum", fill_value=0
    )
    # Normalize by total triples per period
    pivot = pivot.div(pivot.sum(axis=1), axis=0)
    return pivot
```

### Narrative Entry and Exit Detection

```python
def detect_narrative_emergence(narrative_index, window=3):
    """
    Detect when new narratives emerge and old ones fade.

    A narrative has "emerged" when its prevalence exceeds a threshold
    for the first time after being absent for `window` periods.
    """
    emerged = {}
    faded = {}

    for narrative in narrative_index.columns:
        series = narrative_index[narrative]
        # Binary: above median = active
        active = series > series.median()

        # Detect transitions
        transitions = active.astype(int).diff()
        emergence_points = transitions[transitions == 1].index
        fade_points = transitions[transitions == -1].index

        if len(emergence_points) > 0:
            emerged[narrative] = emergence_points
        if len(fade_points) > 0:
            faded[narrative] = fade_points

    return emerged, faded
```

---

## Worked Example

### Input: 10 Bangla News Articles about the Economy

**Article 1:**
> *"সরকার ব্যয় বাড়িয়েছে, যা মূল্যস্ফীতি বাড়িয়েছে"*
> (Government increased spending, which increased inflation)

**Article 2:**
> *"বাংলাদেশ ব্যাংক সুদের হার বাড়িয়েছে মূল্যস্ফীতি নিয়ন্ত্রণে"*
> (Bangladesh Bank raised interest rates to control inflation)

**Article 3:**
> *"সরকারের ব্যয় নীতি ব্যবসায়ীদের উদ্বিগ্ন করেছে"*
> (Government's spending policy worried businesses)

### Step 1: Triple Extraction (via LLM)

```json
[
  {"actor": "Government", "action": "increased", "target": "spending", "doc": "A1"},
  {"actor": "spending", "action": "increased", "target": "inflation", "doc": "A1"},
  {"actor": "Bangladesh Bank", "action": "raised", "target": "interest rates", "doc": "A2"},
  {"actor": "Government's spending policy", "action": "worried", "target": "businesses", "doc": "A3"}
]
```

### Step 2: Entity Resolution

```python
resolver = EntityResolver()
triples = [...]  # From above
entities = resolver.extract_entities_from_triples(triples)
clusters = resolver.cluster_entities(entities)

# Resolved entities
# "Government's spending policy" → "Government" (canonical)
# "Government" stays "Government"
# "Bangladesh Bank" stays "Bangladesh Bank"
```

### Step 3: Resolved Triples

```json
[
  {"actor": "Government", "action": "increased", "target": "spending", "doc": "A1"},
  {"actor": "spending", "action": "increased", "target": "inflation", "doc": "A1"},
  {"actor": "Bangladesh Bank", "action": "raised", "target": "interest rates", "doc": "A2"},
  {"actor": "Government", "action": "worried", "target": "businesses", "doc": "A3"}
]
```

### Step 4: Narrative Groups

```python
# Group by shared actor
actor_groups = grouper.group_by_shared_actor(resolved_triples, min_shared=2)
# → {"Government": [triple1, triple4]}

# Causal chain detection
chains = grouper.group_by_causal_chain(resolved_triples)
# → [{
#     "chain": ["Government", "spending", "inflation"],
#     "triples": [
#       {"actor": "Government", "action": "increased", "target": "spending"},
#       {"actor": "spending", "action": "increased", "target": "inflation"},
#     ]
#   }]
```

### Step 5: Derived Index

```python
# Monthly narrative prevalence
index = temporal_narrative_index(all_triples, freq="M")
# 2024-06: Government_increased=0.15, BB_raised=0.10, ...
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Description |
|----------|-------------|
| **Compositional** | Recovers narrative structure from atomic components |
| **Cross-document** | Aggregates signals across entire corpora |
| **Entity-centric** | Directly answers "who did what" questions |
| **Causal chains** | Naturally captures A → B → C narrative sequences |
| **Economist-friendly** | Triples map to economic intuition (agents, actions, outcomes) |

### Weaknesses

| Weakness | Description | Mitigation |
|----------|-------------|------------|
| **No Bangla dependency parser** | SpaCy/Stanza Bangla models are limited | LLM-based triple extraction |
| **Entity resolution** | Surface-form variation creates sparsity | Embedding-based clustering |
| **Noise from OpenIE** | OpenIE extracts many non-narrative triples | Domain filtering, LLM validation |
| **Triple aggregation** | Naive counting misses narrative nuance | Graph-based grouping (L8) |
| **LLM cost at scale** | Million-document extraction is expensive | Use for discovery, then scale with L2 |

---

## When to Use Level 9

| Scenario | Recommended | Alternative |
|----------|-------------|-------------|
| Extracting who-did-what in economic narratives | ✅ **Level 9** | — |
| Cross-document narrative aggregation | ✅ **Level 9** | — |
| Causal chain discovery | ✅ **Level 9** | L7 for single-document |
| Rapid narrative exploration | ⚠️ High cost | L3 or L4 first |
| Simple narrative tracking | ❌ Overkill | L1 or L2 |
| Deep single-document analysis | ❌ Overkill | L10 |

---

## BENI Implementation Guide

### Phase 1: LLM-Based Triple Extraction with Existing Pipeline (2 weeks)

The quickest path: extend the existing `llm_annotate.py` prompt to extract triples.

```python
# Extend the existing annotation prompt
ENHANCED_PROMPT = """
Extract economic information from this Bangla news article.

1. Is this article economically relevant? (yes/no)
2. What is the main economic topic?
3. Extract ALL (actor, action, target) triples:
   - ACTOR: Who acts? (government, central bank, businesses, etc.)
   - ACTION: What do they do? (increase, decrease, raise, cut, etc.)
   - TARGET: What is affected? (spending, rates, inflation, growth, etc.)

Return as JSON:
{
    "economic_relevance": true/false,
    "topic": "...",
    "triples": [
        {"actor": "...", "action": "...", "target": "..."}
    ]
}

Article: {text}
"""
```

### Phase 2: Bangla Triple Extraction Baseline (1 week)

```python
# Rule-based baseline for Bangla economic triples
BANGLA_ACTION_VERBS = {
    "বাড়িয়েছে": "increased",
    "কমিয়েছে": "decreased",
    "বৃদ্ধি করেছে": "increased",
    "হ্রাস করেছে": "decreased",
    "ঘোষণা করেছে": "announced",
    "চালু করেছে": "launched",
    "পরিবর্তন করেছে": "changed",
    "স্থির করেছে": "fixed",
}

def extract_bangla_triples_rules(text):
    """Simple rule-based triple extraction for Bangla economic text."""
    doc = nlp_bn(text)
    triples = []

    for sent in doc.sents:
        for token in sent:
            if token.text in BANGLA_ACTION_VERBS:
                # Find subject (left of verb)
                actor = " ".join(
                    [t.text for t in sent if t.i < token.i and t.pos_ == "NOUN"]
                ) or "unknown"
                # Find object (right of verb)
                target = " ".join(
                    [t.text for t in sent if t.i > token.i and t.pos_ == "NOUN"]
                ) or "unknown"

                triples.append({
                    "actor": actor,
                    "action": BANGLA_ACTION_VERBS[token.text],
                    "target": target,
                    "confidence": 0.4,
                })

    return triples
```

### Phase 3: Full RELATIO Pipeline for BENI (4 weeks)

```python
class BeniRelatioPipeline:
    """Full RELATIO-style extraction pipeline for BENI."""

    def __init__(self, llm_client, e5_model):
        self.llm = llm_client
        self.resolver = EntityResolver(e5_model)
        self.grouper = NarrativeGrouper()

    def process_articles(self, articles):
        """Process a batch of articles: extract, resolve, group."""
        all_triples = []

        # Step 1: Extract triples via LLM
        for article in articles:
            triples = self.extract_triples(article["text"])
            for t in triples:
                t["doc_id"] = article["id"]
                t["date"] = article["date"]
            all_triples.extend(triples)

        # Step 2: Entity resolution
        entities = self.resolver.extract_entities_from_triples(all_triples)
        self.resolver.cluster_entities(entities)
        for t in all_triples:
            t["resolved_actor"] = self.resolver.resolve(t["actor"])
            t["resolved_target"] = self.resolver.resolve(t["target"])

        # Step 3: Narrative grouping
        groups = self.grouper.group_by_shared_actor(all_triples, min_shared=5)

        # Step 4: Build narrative index
        index = self.build_index(all_triples)

        return {
            "total_triples": len(all_triples),
            "unique_actors": len(set(t["resolved_actor"] for t in all_triples)),
            "narrative_groups": len(groups),
            "index": index,
        }

    def extract_triples(self, text):
        prompt = TRIPLE_PROMPT.format(text=text[:4000])
        response = self.llm(prompt)
        return json.loads(response)

    def build_index(self, triples):
        df = pd.DataFrame(triples)
        df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")
        index = df.groupby(["month", "resolved_actor", "action"]).size().unstack(fill_value=0)
        return index
```

### Integration with BENI Pipeline

```
Current BENI Pipeline:
Potrika Corpus → LLM Annotation → TF-IDF → Monthly Index

With RELATIO Addition:
Potrika Corpus → LLM Annotation ─┬─→ TF-IDF → Aggregate Index
                                  └─→ Triple Extraction → Entity Resolution
                                                          ↓
                                                    Narrative Groups
                                                          ↓
                                                    Triple-Based Index
```

### Infrastructure

```bash
pip install spacy openie  # For English prototyping
pip install sentence-transformers scikit-learn networkx
pip install pandas numpy matplotlib
```

### Extension to XENI Languages

The RELATIO approach is language-agnostic when using LLM-based extraction:

| Language | Dependency Parser | LLM Triple Extraction | Status |
|----------|-----------------|----------------------|--------|
| Bangla (BENI) | Limited | ✅ Claude/GPT | Ready for Phase 1 |
| Assamese (AENI) | None | ✅ Zero-shot LLM | Identical approach |
| Nepali (NENI) | None | ✅ Zero-shot LLM | Identical approach |
| Hausa (HENI) | None | ✅ Zero-shot LLM | Identical approach |

---

## References

### Core Reading

- Ash, E., Gauthier, G., & Widmer, P. (2023). "RELATIO: Text Semantics Capture Political and Economic Narratives." *Political Analysis* (Cambridge University Press). arXiv: `2108.01720`. Code: `github.com/relatio-nlp/relatio`.
  — The foundational RELATIO paper. Unsupervised AVP/SVO triplet extraction + entity clustering. U.S. Congressional Record application.

- Lange, K.-R., Reccius, M., Schmidt, T., Müller, H., Roos, M. W. M., & Jentsch, C. (2022). "Towards extracting collective economic narratives from texts." *Ruhr Economic Papers #963*. DOI: `10.4419/96973127`.
  — Augments RELATIO with coreference resolution and noise filtering. Causal linking step is core contribution. Evaluated on Financial Times data.

- Schmidt, T., Lange, K.-R., Reccius, M., Müller, H., Roos, M. W. M., & Jentsch, C. (2025). "Identifying economic narratives in large text corpora: An integrated approach using large language models." *Ruhr Economic Papers #1163*. DOI: `10.4419/96973348`.
  — Tests GPT-4o against expert-annotated gold-standard for narrative triple extraction.

### Triple Extraction & OpenIE

- Angeli, G., Premkumar, M. J., & Manning, C. D. (2015). "Leveraging Linguistic Structure For Open Domain Information Extraction." *ACL 2015*.
  — OpenIE system for open-domain triple extraction.

- Del Corro, L. & Gemulla, R. (2013). "ClausIE: clause-based open information extraction." *WWW 2013*.
  — Clause-based extraction for high-precision triples.

### Entity Resolution

- Eyal, M. et al. (2022). "Multi-lingual Entity Resolution." *EMNLP 2022*.
  — Cross-lingual entity linking relevant for XENI pipelines.

### See Also

- Level 6: [Semantic Role Extraction](L06_semantic_role_extraction.md) — SRL as alternative triple extraction
- Level 7: [Causal Narrative Extraction](L07_causal_narrative_extraction.md) — Causal triples as input to REALTIO
- Level 8: [Narrative Networks and Graphs](L08_narrative_networks_graphs.md) — Graph storage for narrative groups
- Level 10: [LLM-Based Extraction](L10_llm_based_extraction.md) — LLM as triple extraction engine

---

**Up:** [Methodologies Index](INDEX.md) | **Main:** [Narrative Extraction Methodologies](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
