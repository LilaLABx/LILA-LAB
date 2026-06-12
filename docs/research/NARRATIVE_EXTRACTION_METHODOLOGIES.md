> **Navigation:** [Documentation Portal](../index.md) > Research > Methodologies Reference
>
> ---

# Narrative Extraction Methodologies: A Hierarchical Framework

> **Status:** Living reference document for BENI and future XENI narrative extraction research.
> **Scope:** Covers 12 levels of narrative extraction sophistication, from manual qualitative coding to agentic LLM discovery systems.
> **Purpose:** Maps current BENI implementation against the hierarchy, identifies gaps, and proposes a BENI 2.0 architecture.

---

## Table of Contents

1. [Introduction: What Is a Narrative?](#introduction-what-is-a-narrative)
2. [The Hierarchy at a Glance](#the-hierarchy-at-a-glance)
3. [Level 0: Manual Qualitative Coding](#level-0-manual-qualitative-coding)
4. [Level 1: Lexicon-Based Narrative Detection](#level-1-lexicon-based-narrative-detection)
5. [Level 2: Statistical Text Mining](#level-2-statistical-text-mining)
6. [Level 3: Topic Modeling](#level-3-topic-modeling)
7. [Level 4: Embedding-Based Narrative Discovery](#level-4-embedding-based-narrative-discovery)
8. [Level 5: Event-Centric Narrative Extraction](#level-5-event-centric-narrative-extraction)
9. [Level 6: Semantic Role and Narrative Structure Extraction](#level-6-semantic-role-and-narrative-structure-extraction)
10. [Level 7: Causal Narrative Extraction](#level-7-causal-narrative-extraction)
11. [Level 8: Narrative Networks and Graphs](#level-8-narrative-networks-and-graphs)
12. [Level 9: RELATIO-Style Narrative Extraction](#level-9-relatio-style-narrative-extraction)
13. [Level 10: LLM-Based Narrative Extraction](#level-10-llm-based-narrative-extraction)
14. [Level 11: Agentic Narrative Discovery Systems](#level-11-agentic-narrative-discovery-systems)
15. [BENI Current Implementation Mapping](#beni-current-implementation-mapping)
16. [BENI 2.0: Proposed Architecture](#beni-20-proposed-architecture)
17. [Research Frontier & Open Problems](#research-frontier--open-problems)
18. [References](#references)

---

## Introduction: What Is a Narrative?

A clear definition from the economic narrative literature grounds the hierarchy:

> A narrative is not just a topic. It is a structured explanation involving actors, events, and often cause-effect relationships that explain how the world works.

This definition carries three critical implications for methodology design:

1. **Narrative ≠ Topic** — Topics are static categories (e.g., "inflation"). Narratives are dynamic sequences with structure (e.g., "government spending caused demand-pull inflation").
2. **Narratives have structure** — They involve actors (who), actions (what), and causal links (why). Extracting this structure requires more than keyword counting.
3. **Narratives explain** — They propose mechanisms that connect causes to outcomes. This makes causal extraction a central challenge.

The hierarchy below progresses from methods that detect *whether* a narrative exists to methods that extract *what the narrative is, who drives it, and how it propagates*.

---

## The Hierarchy at a Glance

| Level | Method | Core Technique | Narrative Understanding | BENI Status | Details |
|-------|--------|---------------|----------------------|-------------|---------|
| **L0** | Manual Qualitative Coding | Human annotation, thematic analysis | Deep interpretation | ✅ Gold-standard reference set (300 articles planned) | [Full page](methodologies/L00_manual_qualitative_coding.md) |
| **L1** | Lexicon-Based | Keyword matching, dictionaries | Topic presence | ✅ `narrative.py` — Bangla lexicons for force, target, topic | [Full page](methodologies/L01_lexicon_based_detection.md) |
| **L2** | Statistical Text Mining | TF-IDF, N-grams, PMI, co-occurrence | Word clusters | ✅ TF-IDF baseline (80k features, 91.7% accuracy) | [Full page](methodologies/L02_statistical_text_mining.md) |
| **L3** | Topic Modeling | LDA, HDP, NMF, BERTopic | Latent themes | 🔄 BERTopic mentioned as exploratory robustness check | [Full page](methodologies/L03_topic_modeling.md) |
| **L4** | Embedding-Based | SBERT, E5, BGE, UMAP + HDBSCAN | Semantic clusters | ⬜ Not yet implemented | [Full page](methodologies/L04_embedding_based_discovery.md) |
| **L5** | Event-Centric | Event detection, temporal ordering | Narrative chains | ⬜ Not yet implemented | [Full page](methodologies/L05_event_centric_extraction.md) |
| **L6** | Semantic Role | NER, OpenIE, SRL, dependency parsing | 5W1H structure | ⬜ Not yet implemented | [Full page](methodologies/L06_semantic_role_extraction.md) |
| **L7** | Causal Extraction | Rule-based + ML cause-effect detection | Causal mechanisms | ⬜ Not yet implemented | [Full page](methodologies/L07_causal_narrative_extraction.md) |
| **L8** | Narrative Graphs | Knowledge graphs, temporal KGs | Relational networks | ⬜ Not yet implemented | [Full page](methodologies/L08_narrative_networks_graphs.md) |
| **L9** | RELATIO-Style | Entity-relation grouping across documents | Aggregated narratives | ⬜ Not yet implemented | [Full page](methodologies/L09_relatio_style_extraction.md) |
| **L10** | LLM-Based | Prompt-based extraction, structured output | Deep semantic extraction | ✅ `llm_annotate.py` — Claude, GPT-4o, Gemini ensemble | [Full page](methodologies/L10_llm_based_extraction.md) |
| **L11** | Agentic Systems | Multi-agent discovery, clustering, verification | Autonomous narrative observatory | ⬜ Not yet implemented | [Full page](methodologies/L11_agentic_discovery_systems.md) |

**Legend:** ✅ Implemented | 🔄 Planned/In Progress | ⬜ Not Yet Implemented

---

## Level 0: Manual Qualitative Coding

> 📖 **Dedicated methodology page:** [`methodologies/L00_manual_qualitative_coding.md`](methodologies/L00_manual_qualitative_coding.md) — full techniques, worked examples, BENI annotation schema, quality targets, and best practices.

The oldest and still most trusted method. Produces gold-standard data for training and evaluating automated systems.

### Techniques

- **Content analysis** — Systematic categorization of text into predetermined codes
- **Thematic coding** — Inductive discovery of themes from the text itself
- **Grounded theory** — Iterative code development where theory emerges from data
- **Frame analysis** — Identifying how issues are presented, what is emphasized or omitted
- **Narrative inquiry** — Holistic analysis of stories as complete units

### Example

**Text:**
> Inflation is rising because government spending increased.

**Human annotator codes:**
- Topic: Inflation
- Cause: Government spending
- Effect: Inflation rise
- Stance: Negative
- Actor: Government

### Strengths

- **High validity** — Human interpretation captures nuance and context
- **Rich interpretation** — Can identify implicit causality, sarcasm, cultural references
- **Gold-standard creation** — Essential for training and evaluating automated methods

### Weaknesses

- **Expensive** — Requires trained annotators, domain expertise
- **Doesn't scale** — Linear cost per document
- **Subjectivity** — Inter-annotator agreement requires careful protocol design

### BENI Context

**Current status: ✅ Implemented (in progress)**

The BENI pipeline uses human annotation at several stages:

1. **300-article locked reference set** — A gold-standard evaluation set with manual labels for economic relevance, topic, sentiment, narrative force, and valuation target. This serves as the ground truth for classifier evaluation. See [`pipelines/BENI/annotation/ANNOTATOR_GUIDE.md`](../../pipelines/BENI/annotation/ANNOTATOR_GUIDE.md).

2. **Adjudication protocol** — A formal process for resolving disagreements between LLM annotators, documented in [`pipelines/BENI/annotation/ADJUDICATION_PROTOCOL.md`](../../pipelines/BENI/annotation/ADJUDICATION_PROTOCOL.md).

3. **Annotation schema** — A 12-field schema covering economic relevance, topic, narrative force, valuation target, and sentiment. See [`pipelines/BENI/annotation/ANNOTATION_SCHEMA.md`](../../pipelines/BENI/annotation/ANNOTATION_SCHEMA.md).

### Guidance

- **For BENI:** Complete the 300-article reference set. Lock it. Use as the exclusive evaluation benchmark for all future classifier comparisons.
- **For new pipelines:** Start with 100–300 manually annotated articles per domain per language. This small investment pays enormous dividends in evaluation reliability.

---

## Level 1: Lexicon-Based Narrative Detection

> 📖 **Dedicated methodology page:** [`methodologies/L01_lexicon_based_detection.md`](methodologies/L01_lexicon_based_detection.md) — full Bangla lexicons, scoring functions, BBN index details, negation handling, and improvement path.

The simplest automated approach. Counts occurrences of pre-defined words and phrases associated with specific narratives.

### Techniques

- **Keyword matching** — Exact string matching against narrative dictionaries
- **Dictionary-based scoring** — Weighted term lists with polarity or intensity scores
- **Rule-based patterns** — Regular expressions for multi-word narrative expressions

### Example

**Inflation narrative lexicon:**
```
inflation, prices, cost of living, food prices, fuel costs, price hike
```

**Count occurrences per document → aggregate by time period → narrative prevalence index**

### Applications

- Narrative prevalence tracking over time
- Narrative frequency indices (monthly, quarterly)
- Media sentiment indices (early approaches)

### Weakness

**Finds topics, not narratives.** A keyword match for "inflation" tells you the word appeared, not whether the article tells a causal story about inflation. This is the central limitation that motivates all higher levels.

### BENI Context

**Current status: ✅ Implemented**

The BENI pipeline uses lexicon-based extraction in [`pipelines/BENI/experiment/beni_pilot/narrative.py`](../../pipelines/BENI/experiment/beni_pilot/narrative.py) with three Bangla lexicons:

| Lexicon | Categories | Example Terms |
|---------|-----------|---------------|
| **Narrative Force** | 8 categories | সংকট (crisis), দুর্ভোগ (burden), ব্যর্থতা (blame), সংস্কার (reform) |
| **Valuation Target** | 8 categories | সরকার (government), বাংলাদেশ ব্যাংক (central bank), ভোক্তা (households) |
| **Economic Topic** | 10 categories | মূল্যস্ফীতি (inflation), ডলার (exchange rate), রপ্তানি (trade) |

The `narrative_profile()` function scores each article against all lexicons and returns the top labels with match counts. This is a **Level 1** method (keyword matching with scoring), not a true narrative extraction.

### Limitations in BENI Context

- The lexicons are hand-built and may miss evolving narrative language
- No weighting for term importance within categories
- Cannot distinguish "inflation is rising" from "inflation is under control"
- Binary matching — no fuzzy or semantic matching

### Improvement Path → L4

The lexicons should be used as **seed terms** for embedding-based expansion (see Level 4), where semantically similar terms are discovered automatically.

---

## Level 2: Statistical Text Mining

> 📖 **Dedicated methodology page:** [`methodologies/L02_statistical_text_mining.md`](methodologies/L02_statistical_text_mining.md) — full TF-IDF configuration, 91.7% accuracy results, index construction pipeline, and top discriminative features.

Narratives approximated through word distributions and co-occurrence patterns without requiring pre-defined dictionaries.

### Techniques

- **TF-IDF** — Term frequency-inverse document frequency weighting
- **N-grams** — Multi-word sequences (bigrams, trigrams) capturing phrasal narratives
- **PMI (Pointwise Mutual Information)** — Measuring how often words co-occur more than expected by chance
- **Co-occurrence networks** — Graph of words that frequently appear together

### Example

**Words frequently co-occurring:**
```
inflation ↔ food ↔ supply chain ↔ imports
```

**Possible narrative cluster:** *Supply-chain-driven inflation*

### Outputs

- Word networks showing narrative associations
- Emerging theme detection via burst analysis
- Term frequency time series for narrative tracking

### Weakness

**No causal understanding.** Statistical patterns can suggest narrative clusters but cannot distinguish "A causes B" from "A and B are correlated." This requires higher-level methods.

### BENI Context

**Current status: ✅ Implemented**

The BENI pipeline uses TF-IDF as its primary classifier approach:

- **Vectorizer:** `TfidfVectorizer(max_features=80000, min_df=2, ngram_range=(1,2))`
- **Classifier:** `OneVsRestClassifier(LogisticRegression(class_weight='balanced'))`
- **Performance:** 91.7% accuracy, 0.894 macro F1 on economic relevance

This is a **Level 2** method for classification, not narrative extraction per se. The TF-IDF features capture discriminative words for economic vs. non-economic articles, but do not explicitly model narrative structure.

### TF-IDF Index Results

| Metric | Value |
|--------|-------|
| Monthly observations | 79 (Jun 2014 – Dec 2020) |
| Mean economic share | 38.9% |
| CPI level correlation | r = −0.75 (p < 0.001) |
| FX level correlation | r = −0.72 (p < 0.001) |
| Reserves level correlation | r = −0.77 (p < 0.05) |
| First-differenced CPI correlation | r = −0.04 (n.s.) |

The strong level correlations but weak detrended correlations suggest the TF-IDF index captures structural narrative shifts but not short-term noise. This may improve with BanglaBERT (Level 4+).

---

## Level 3: Topic Modeling

> 📖 **Dedicated methodology page:** [`methodologies/L03_topic_modeling.md`](methodologies/L03_topic_modeling.md) — full method comparison table, keyATM seeding, BERTopic pipeline code, and dynamic topic tracking.

The first major step toward latent narrative discovery — topics emerge from statistical patterns rather than being pre-defined.

### Methods

| Method | Type | Strengths | Weaknesses |
|--------|------|-----------|------------|
| **LDA** | Probabilistic | Interpretable topics, well-established | Needs k specified, bag-of-words |
| **HDP** | Bayesian nonparametric | Automatic topic count | Computationally expensive |
| **NMF** | Matrix factorization | Fast, parts-based | Sensitive to initialization |
| **Dynamic Topic Models** | Temporal LDA | Topic evolution over time | Complex inference |
| **BERTopic** | Embedding-based | Semantic topics, interpretable | Sensitive to embedding quality |

### Example

**Topic:**
```
oil, energy, gas, war, Russia, supply
```

**Human labels:**
> Energy shock narrative

### Advanced Variant

**Dynamic Topic Models (DTM)** track how topics change over time:
- Did the "inflation" topic shift from "demand-driven" to "supply-chain" framing between 2021–2023?
- Which narratives are emerging? Which are fading?

### Used In

- News media analysis
- Political communication
- Economic narrative tracking
- Scientific literature mapping

### BENI Context

**Current status: 🔄 Planned (exploratory)**

BERTopic is mentioned in the BENI Roadmap as an "exploratory robustness check" and `keyATM` (seeded topic model) as the primary topic modeling approach:

> *"BERTopic as an exploratory robustness check if embeddings behave well"* — BENI_ROADMAP.md

Neither has been implemented in the pipeline code yet.

### Why BERTopic for BENI 2.0

BERTopic is particularly well-suited for narrative extraction in low-resource languages because:

1. **Multilingual embeddings** — Works with SentenceTransformers (E5, BGE) that support 100+ languages
2. **Dynamic topics** — Can track how narrative themes evolve over the 79-month BENI window
3. **Hierarchical topics** — Reveals nested narrative structures (e.g., "inflation" → "food inflation" → "rice prices")
4. **Interpretable** — c-TF-IDF topic representations are human-readable

---

## Level 4: Embedding-Based Narrative Discovery

> 📖 **Dedicated methodology page:** [`methodologies/L04_embedding_based_discovery.md`](methodologies/L04_embedding_based_discovery.md) — full E5 model comparison, UMAP+HDBSCAN pipeline, narrative cluster discovery, and 3-phase BENI implementation plan.

Modern semantic clustering using dense vector representations, capturing meaning beyond keyword overlap.

### Methods

| Model | Type | Language Support | Notes |
|-------|------|-----------------|-------|
| **Word2Vec** | Static word embeddings | Per-language training | Requires large corpus |
| **Doc2Vec** | Document embeddings | Per-language training | Captures document-level semantics |
| **SBERT** | Sentence transformer | 50+ languages | Sentence-level similarity |
| **E5** | Multilingual embedding | 100+ languages | State-of-the-art retrieval |
| **BGE** | BAAI general embedding | 100+ languages | Strong on semantic tasks |
| **Instructor** | Instruction-tuned | English + emerging | Task-adaptive embeddings |

### Pipeline

```
Document
    ↓
Embedding (SBERT/E5/BGE)
    ↓
Dimensionality Reduction (UMAP)
    ↓
Clustering (HDBSCAN)
    ↓
Narrative Cluster
```

### Advantages

- **Captures semantics beyond keywords** — "food prices rise", "grocery costs increase", and "higher market prices" cluster together despite zero keyword overlap
- **Multilingual by design** — Embedding models like E5 and BGE support Bangla, Assamese, Nepali, and other BENI target languages
- **No training data required** — Zero-shot narrative discovery

### BENI Context

**Current status: ⬜ Not yet implemented**

The BENI pipeline does not currently use embedding-based narrative discovery. The closest approach is the BanglaBERT classifier, which uses transformer embeddings for *classification* (economic vs. not economic) rather than *narrative discovery*.

### Recommendations

1. **Extend BanglaBERT embeddings** to narrative clustering tasks, not just classification
2. **Use E5 or BGE** for Bangla document embeddings (they support Bengali natively)
3. **UMAP + HDBSCAN pipeline** for narrative cluster discovery
4. **Seed with lexicon terms** from `narrative.py` for semi-supervised narrative discovery

---

## Level 5: Event-Centric Narrative Extraction

> 📖 **Dedicated methodology page:** [`methodologies/L05_event_centric_extraction.md`](methodologies/L05_event_centric_extraction.md) — full event detection methods, temporal linking, narrative chain construction, and LLM-based event extraction approach.

Narratives become sequences of events. Rather than treating a document as a bag of topics, event-centric extraction identifies what happened, when, and in what order.

### Components

#### Event Detection

Identify discrete events from text:

```
Event: Inflation increased
Temporal anchor: Q3 2022
Event: Central bank raised rates
Temporal anchor: Q4 2022
```

#### Event Linking

Connect causally or temporally related events:

```
Event A (Inflation increased) → Event B (Central bank raised rates)
```

#### Temporal Ordering

Assign timestamps and order events chronologically:

```
2021-Q4: Pandemic supply disruptions
    → 2022-Q1: Inflation accelerates
    → 2022-Q2: Central bank signals tightening
    → 2022-Q3: First rate hike
```

### Tools

| Tool | Task | Notes |
|------|------|-------|
| **MAUI** | Event extraction | Rule-based + ML |
| **OpenIE** | Relation extraction | Open-domain |
| **FRED** | Event extraction | Frame-based |
| **TimeML** | Temporal annotation | ISO standard |

### Output: Narrative Chain

```
Pandemic
    ↓
Supply disruptions
    ↓
Inflation
    ↓
Rate hikes
```

This is a genuine narrative chain — events linked by cause and time.

### BENI Context

**Current status: ⬜ Not yet implemented**

Event-centric extraction is not part of the current BENI pipeline. The pilot builds a monthly aggregate index, not event sequences.

### Relevance for BENI 2.0

Event-centric extraction would enable:

1. **Narrative lead analysis** — Do economic events appear in news before they appear in official statistics?
2. **Section migration tracking** — When an event (e.g., "inflation") appears in Economy section vs. National section
3. **Narrative acceleration** — How quickly do events chain together during crisis periods vs. stable periods?

---

## Level 6: Semantic Role and Narrative Structure Extraction

> 📖 **Dedicated methodology page:** [`methodologies/L06_semantic_role_extraction.md`](methodologies/L06_semantic_role_extraction.md) — full 5W1H framework, NER/RE/SRL/OpenIE techniques, integration path via existing LLM pipeline, and Bangla role extractor.

Extracts the 5W1H framework — Who did what, to whom, why, and when? — from narrative text.

### The 5W1H Framework

| Element | Question | Example |
|---------|----------|---------|
| **Actor** | Who? | The central bank |
| **Action** | Did what? | Raised interest rates |
| **Recipient** | To whom? | Commercial banks |
| **Purpose** | Why? | To combat inflation |
| **Temporal** | When? | In July 2024 |
| **Manner** | How? | By 50 basis points |

### Techniques

| Technique | Task | Maturity |
|-----------|------|----------|
| **NER** | Named Entity Recognition | Mature |
| **Relation Extraction** | Entity-relation triple extraction | Mature |
| **Semantic Role Labeling** | Predicate-argument structure | Research-grade |
| **OpenIE** | Open-domain information extraction | Production-ready |
| **Dependency Parsing** | Grammatical relation extraction | Mature |

### Example

**Sentence:**
> The central bank raised interest rates to combat inflation.

**Output:**

| Role | Value |
|------|-------|
| Actor | Central Bank |
| Action | Raise rates |
| Instrument | Interest rates |
| Purpose | Combat inflation |

**Narrative schema:**
```
Actor → Action → Outcome
```

### BENI Context

**Current status: ⬜ Not yet implemented**

The BENI pipeline does not perform semantic role labeling or structured narrative extraction. The closest is the LLM annotation prompt in `llm_annotate.py`, which asks for actor, cause, effect, and stance as JSON fields — effectively using the LLM as an implicit SRL system.

### Recommendation

Structured SRL would allow BENI to extract not just *whether* an article is about inflation, but *who* the article blames for inflation and *what* causal mechanism it proposes. This is a key step toward Level 7 (causal extraction).

---

## Level 7: Causal Narrative Extraction

> 📖 **Dedicated methodology page:** [`methodologies/L07_causal_narrative_extraction.md`](methodologies/L07_causal_narrative_extraction.md) — full rule-based patterns for Bangla causal connectives, ML approaches, causal graph builder, and 3-phase BENI implementation plan.

This is where economic narrative research currently focuses. Extracts explicit cause-effect relationships from text — the core of what makes a narrative a narrative rather than a topic.

### Formal Definition

Narrative = **Cause** → **Mechanism** → **Outcome**

rather than merely

Narrative = **Topic**

### Methods

#### Rule-Based Approaches

Pattern-based extraction using causal connectives:

| Pattern | Example |
|---------|---------|
| `because` | "Prices rose because of supply shortages" |
| `therefore` | "Demand increased, therefore prices rose" |
| `caused by` | "Inflation was caused by fiscal expansion" |
| `resulted in` | "The policy resulted in higher prices" |
| `led to` | "Supply disruptions led to inflation" |

#### ML-Based Approaches

| Model | Task | Performance |
|-------|------|-------------|
| **BERT fine-tuned** | Cause-effect classification | State-of-the-art |
| **RoBERTa** | Causal relation extraction | Strong on SemEval tasks |
| **DeBERTa** | Causal reasoning | Best on multiple benchmarks |
| **T5/LLM** | Generative causal extraction | Emerging |

#### Causal Extraction Systems

| System | Approach | Notes |
|--------|----------|-------|
| **Causality Extractor** | Pattern + ML hybrid | General domain |
| **Event-Causality** | Event-pair classification | Temporal + causal |
| **Causal-BERT** | Fine-tuned BERT | SemEval 2020 task |
| **CONNA** | Attention-based | Discourse-aware |

### Why This Matters for Economics

Economic narratives are fundamentally causal. When a news article says "inflation is rising because of government spending," it is proposing a causal model of the economy. Extracting these causal claims — regardless of their accuracy — reveals the **economic belief system** of a society.

### BENI Context

**Current status: ⬜ Not yet implemented**

The BENI pipeline's LLM annotation prompt asks for `narrative_force` (crisis, blame, reform, etc.) but does not explicitly extract cause-effect relations. The `llm_annotate.py` prompt includes causal indicators implicitly through the valuation target field (who is responsible), but this is a proxy, not a causal extraction system.

### Recommendation

The LLM annotation prompt should be extended to include:
```json
{
  "cause": "Government spending increase",
  "effect": "Rising inflation",
  "mechanism": "Demand-pull",
  "causal_confidence": 0.85,
  "causal_marker": "because",
  "stance_on_cause": "negative"
}
```

This would move BENI from Level 10 (LLM-based annotation) to Level 7 (causal extraction) simultaneously.

---

## Level 8: Narrative Networks and Graphs

> 📖 **Dedicated methodology page:** [`methodologies/L08_narrative_networks_graphs.md`](methodologies/L08_narrative_networks_graphs.md) — full knowledge graph construction, temporal KG techniques, cross-platform narrative templates, and NetworkX implementation code.

Narratives become graph structures where nodes represent actors, concepts, and events, and edges represent causal, supporting, opposing, or temporal relations.

### Graph Components

**Nodes:**
- Actors (government, central bank, businesses, households)
- Concepts (inflation, growth, stability)
- Events (rate hike, budget announcement, election)

**Edges:**
- Causes (→)
- Supports (+)
- Opposes (−)
- Temporal (before, after, during)
- Hierarchical (is-a, part-of)

### Example Graph

```
Ukraine War
    ↓ [causes]
Energy Prices ↑
    ↓ [causes]
Inflation ↑
    ↓ [causes]
Rate Hikes → [opposes] Growth
    ↓ [causes]
Household Burden ↑
```

### Methods

| Method | Description | Tools |
|--------|-------------|-------|
| **Knowledge Graphs** | Entity-relation triples from text | Neo4j, RDF, SPARQL |
| **Narrative Graphs** | Narrative-specific KG | Narrative ML frameworks |
| **Temporal Knowledge Graphs** | KG with time-dimension | tKGM, T-GCN |
| **Cross-Platform Narrative Graphs** | Multi-source narrative integration | Social network analysis |

### Recent Advances

Cross-platform narrative graph approaches model how narratives spread across news, social media, and speeches. This is particularly relevant for BENI's plan to extend to 10 languages — understanding how narratives travel across linguistic boundaries.

### BENI Context

**Current status: ⬜ Not yet implemented**

The BENI pipeline does not construct narrative graphs. The index is a univariate time series, not a relational graph.

### Relevance for BENI 2.0

Narrative graphs would enable:

1. **Section migration visualization** — How economic narratives move across Economy → Politics → National → Editorial sections
2. **Actor-network analysis** — Which actors (government, central bank, businesses) are most central to economic narratives over time
3. **Cross-language narrative mapping** — How the same narrative (e.g., "inflation") is framed differently in Bangla vs. Assamese vs. Nepali
4. **Narrative contagion detection** — When narratives jump from one domain to another (e.g., economic → political)

---

## Level 9: RELATIO-Style Narrative Extraction

> 📖 **Dedicated methodology page:** [`methodologies/L09_relatio_style_extraction.md`](methodologies/L09_relatio_style_extraction.md) — full RELATIO framework details, triple extraction methods (parse/OpenIE/LLM), entity clustering, cross-document aggregation, and BENI implementation pipeline.

One of the most influential narrative-specific frameworks in computational economics. RELATIO extracts structured entity-relation triples and groups them into coherent narratives across document collections.

### Core Mechanism

```
Entity A (Government)
    ↓ relation (increases)
Entity B (Spending)
    ↓ relation (causes)
Entity C (Inflation)
```

These triples are extracted from millions of documents and aggregated to identify dominant narrative structures.

### Key Features

| Feature | Description |
|---------|-------------|
| **Entity extraction** | Political and economic actors, concepts |
| **Relation extraction** | Actions, causations, associations |
| **Narrative grouping** | Graph-based aggregation of related triples |
| **Temporal indexing** | Narrative prevalence over time |
| **Cross-document aggregation** | Million-scale narrative synthesis |

### Economic Applications

RELATIO-style extraction is much closer to what economists call a narrative:

- Extracts explicit causal claims from text
- Groups them into coherent story structures
- Tracks how causal claims evolve over time
- Distinguishes between competing narratives about the same economic phenomenon

### BENI Context

**Current status: ⬜ Not yet implemented**

The BENI pipeline currently aggregates at the article level (economic vs. not economic per article), not the entity-relation level. RELATIO-style extraction would represent a paradigm shift from document classification to narrative component extraction.

### Implementation Path

1. Begin with OpenIE or similar for triple extraction
2. Define economic entity types (actors, instruments, outcomes)
3. Group related triples into narrative clusters
4. Track narrative prevalence over time
5. Combine with LLM-based validation (Level 10)

---

## Level 10: LLM-Based Narrative Extraction

> 📖 **Dedicated methodology page:** [`methodologies/L10_llm_based_extraction.md`](methodologies/L10_llm_based_extraction.md) — full prompt engineering guide, structured output extraction, multi-LLM ensemble methods, confidence calibration, cost analysis, and BENI `llm_annotate.py` details.

Current state-of-the-art for narrative extraction from text. LLMs can perform all lower-level tasks (keyword spotting, classification, event extraction, causal detection) within a single prompt, with deep semantic understanding.

### Prompt-Based Extraction

**Input:**
```
Extract all economic narratives from the following Bangla news article.
Return structured JSON with actor, cause, effect, stance, and confidence.
```

**Output:**
```json
{
  "narratives": [
    {
      "actor": "Government",
      "cause": "Higher spending",
      "effect": "Inflation",
      "stance": "negative",
      "confidence": 0.92
    }
  ]
}
```

### Structured Extraction

Modern LLM pipelines return structured output with:

| Field | Type | Example |
|-------|------|---------|
| Narrative | string | "Government spending drives inflation" |
| Cause | string | "Fiscal expansion" |
| Effect | string | "Price level increase" |
| Actors | list[string] | ["Government", "Bangladesh Bank"] |
| Stance | string | "negative" |
| Confidence | float | 0.85 |
| Evidence | string | "The article states: 'inflation rose because...'" |

### Advantages

- **Implicit causality handling** — LLMs can infer causal relationships not marked by explicit connectives
- **Long document understanding** — Can process entire articles, not just sentences
- **Multiple narrative extraction** — Can identify competing or complementary narratives in the same document
- **Cross-lingual transfer** — Zero-shot extraction works across languages, critical for XENI pipelines

### Weaknesses

- **Hallucination** — LLMs may extract narratives not actually present in text
- **Reproducibility concerns** — Same prompt + same article may give different results across runs
- **Cost** — API-based extraction at scale is expensive
- **Latency** — Real-time extraction is challenging with current API tiers

### BENI Context

**Current status: ✅ Implemented**

The BENI pipeline uses LLM annotation as its primary labeling method:

| Provider | Model | Role |
|----------|-------|------|
| **Anthropic** | Claude Sonnet 4 | Primary annotator, 2 passes for self-consistency |
| **OpenAI** | GPT-4o | Ensemble member for multi-LLM agreement |
| **Google** | Gemini | Alternative provider for robustness |

The annotation prompt (`llm_annotate.py`) extracts 8 fields per article:

1. `economic_relevance` — Binary classification
2. `confidence` — 1–3 ordinal
3. `difficulty` — Clear-cut vs. Borderline
4. `economic_topic` — 12-category topic classification
5. `sentiment` — Negative/neutral/positive
6. `narrative_force` — 8-category narrative framing
7. `valuation_target` — 8-category responsibility assignment
8. `notes` — Free-text reasoning

### Current Limitations

1. **Binary extraction only** — The current prompt classifies articles, but does not extract the narrative text itself
2. **Single-pass for most fields** — Narrative force and valuation target use one LLM call, not ensemble
3. **No causal extraction** — The schema asks for stance and force, but not explicit cause-effect relations
4. **Temperature 0.0** — Deterministic but may miss valid alternative interpretations

### Recommended Improvements

1. **Add explicit cause-effect extraction** to the prompt schema
2. **Extract narrative text spans** — "Which sentence contains the narrative?"
3. **Multi-turn extraction** — First pass: extract candidate narratives. Second pass: validate and refine
4. **Confidence calibration** — Use logprobs or consistency across passes for confidence estimation

---

## Level 11: Agentic Narrative Discovery Systems (Emerging Frontier)

> 📖 **Dedicated methodology page:** [`methodologies/L11_agentic_discovery_systems.md`](methodologies/L11_agentic_discovery_systems.md) — full multi-agent architecture, continuous ingestion pipeline, emergence detection, autonomous narrative observatory design, and XENI multi-language coordination.

The emerging paradigm where narrative extraction becomes an autonomous, continuous discovery process rather than a one-time extraction.

### Pipeline

```
Document Collection (continuous)
    ↓
LLM Extractor (multiple models, cross-validation)
    ↓
Narrative Clustering (embedding + topic model)
    ↓
Narrative Graph Construction (entity-relation-temporal)
    ↓
Temporal Evolution Tracking (emerge, diffuse, compete)
    ↓
Human Verification Loop (active learning for edge cases)
```

### System Capabilities

A Level 11 system continuously discovers:

| Capability | Description |
|------------|-------------|
| **Narrative emergence** | When does a new narrative first appear? |
| **Narrative diffusion** | How does it spread across sources, sections, and platforms? |
| **Narrative competition** | Which narratives coexist, and which dominate over time? |
| **Narrative decay** | When do narratives fade or get replaced? |
| **Cross-platform tracking** | How do narratives differ across news, social media, speeches? |

### Architecture Components

| Component | Function | Tools |
|-----------|----------|-------|
| **Continuous ingestion** | Stream documents from multiple sources | News APIs, scrapers, RSS |
| **LLM extraction service** | Structured narrative extraction | Claude, GPT-4o, open-source LLMs |
| **Clustering engine** | Narrative discovery and grouping | BERTopic, HDBSCAN, UMAP |
| **Graph database** | Narrative relationship storage | Neo4j, NetworkX |
| **Temporal analyzer** | Time-series narrative tracking | Dynamic topic models, change-point detection |
| **Verification loop** | Human-in-the-loop validation | Active learning, uncertainty sampling |

### BENI Context

**Current status: ⬜ Not yet implemented**

BENI is currently a batch-process pipeline (collect → annotate → classify → index), not a continuous agentic system. The pilot index covers 2014–2020. Real-time or near-real-time narrative tracking would require a Level 11 architecture.

### Relevance for BENI 2.0

1. **Continuous tracking** — Extend beyond 2020 with automated collection and near-real-time indexing
2. **Cross-platform integration** — News + social media + policy speeches
3. **Multi-language coordination** — Agentic discovery across all 10 XENI languages
4. **Early warning system** — Detect emerging economic narratives before they appear in official statistics

---

## BENI Current Implementation Mapping

### Pipeline Component → Methodology Level

| BENI Component | File | Level(s) | Description |
|----------------|------|----------|-------------|
| **LLM Annotation** | `annotation/llm_annotate.py` | L10 | Claude/GPT-4o/Gemini prompt-based extraction |
| **Multi-LLM Ensemble** | `annotation/multi_llm_ensemble.py` | L10 | Cross-model agreement for robustness |
| **Active Learning** | `annotation/run_active_learning.py` | L0 | Human-in-the-loop refinement |
| **Lexicon Scoring** | `experiment/beni_pilot/narrative.py` | L1 | Bangla lexicons for force, target, topic |
| **TF-IDF Classifier** | `experiment/beni_pilot/train.py` | L2 | 80k-feature TF-IDF + logistic regression |
| **BanglaBERT** | `experiment/beni_pilot/banglabert.py` | L4 | Transformer classifier (wired, untrained) |
| **Narrative Index** | `experiment/beni_pilot/build_index.py` | L2 | Monthly aggregate of article-level predictions |
| **Index Calibration** | `indices/eco/build_narrative_index.py` | L10→L2 | LLM-calibrated TF-IDF base rates |
| **Macro Validation** | `experiment/beni_pilot/correlate.py` | — | CPI, FX, reserve correlations |
| **Human Annotation** | `annotation/ANNOTATOR_GUIDE.md` | L0 | 300-article gold-standard reference set |

### Current BENI Pipeline Flow

```
           L1/L2                    L10                    L2/L4                  L2
Raw Corpus ──────→ TF-IDF/BERT ──────→ LLM Ensemble ──────→ Classifier ──────→ Narrative Index
                      ↓                  ↓
                  L1 Lexicons        L10 Structured
                  (narrative.py)     Extraction
                                      (llm_annotate.py)
```

### Methodology Coverage Summary

| Level | BENI Status | Key Gap |
|-------|------------|---------|
| L0: Manual | ✅ Gold-standard reference set in progress | Need to lock and publish |
| L1: Lexicon | ✅ Bangla lexicons for 3 dimensions | Limited vocabulary, no weighting |
| L2: Statistical | ✅ TF-IDF baseline at 91.7% accuracy | Detrended correlations weak |
| L3: Topic Modeling | 🔄 BERTopic / keyATM planned | Not yet implemented |
| L4: Embedding | ⬜ (BanglaBERT is classifier, not discovery) | No narrative clustering pipeline |
| L5: Event-Centric | ⬜ Not implemented | No event detection or temporal linking |
| L6: Semantic Role | ⬜ Not implemented | No SRL or 5W1H extraction |
| L7: Causal | ⬜ Not implemented | No explicit cause-effect extraction |
| L8: Narrative Graphs | ⬜ Not implemented | No graph construction |
| L9: RELATIO-Style | ⬜ Not implemented | No entity-relation aggregation |
| L10: LLM-Based | ✅ Multi-provider ensemble | Missing causal extraction, no span-level |
| L11: Agentic | ⬜ Not implemented | Batch-only, no continuous discovery |

---

## BENI 2.0: Proposed Architecture

Building on the hierarchy mapping above, BENI 2.0 should combine multiple levels into an integrated pipeline that moves beyond sentiment tracking toward a **computational economic narrative infrastructure**.

### Architecture

```
                         ┌──────────────────────────────────────────┐
                         │         DATA ACQUISITION LAYER           │
                         │  News (RSS, API) │ Social │ Speeches     │
                         └────────────────────┬─────────────────────┘
                                              ↓
                         ┌──────────────────────────────────────────┐
                         │         LEVEL 4: EMBEDDING LAYER         │
                         │  BGE/E5 Multilingual Document Embeddings  │
                         │  ↓ UMAP ↓ HDBSCAN                        │
                         │  Narrative Cluster Discovery              │
                         └────────────────────┬─────────────────────┘
                                              ↓
                         ┌──────────────────────────────────────────┐
                         │     LEVEL 3: TOPIC MODELING LAYER         │
                         │  BERTopic with seeded topic refinement    │
                         │  Dynamic topic tracking over time         │
                         └────────────────────┬─────────────────────┘
                                              ↓
                         ┌──────────────────────────────────────────┐
                         │       LEVEL 10: LLM EXTRACTION LAYER      │
                         │  Multi-provider ensemble (L0→L10→L7)      │
                         │  ↓ Cause-Effect Detection (L7)           │
                         │  ↓ Semantic Role Labeling (L6)            │
                         └────────────────────┬─────────────────────┘
                                              ↓
                         ┌──────────────────────────────────────────┐
                         │      LEVEL 8: NARRATIVE GRAPH LAYER       │
                         │  Actors + Events + Causes → Graph DB      │
                         │  Temporal Knowledge Graph                  │
                         └────────────────────┬─────────────────────┘
                                              ↓
                         ┌──────────────────────────────────────────┐
                         │      LEVEL 2: INDEX CONSTRUCTION LAYER    │
                         │  Monthly Narrative Indices                │
                         │  Per-topic, Per-force, Per-actor          │
                         └────────────────────┬─────────────────────┘
                                              ↓
                         ┌──────────────────────────────────────────┐
                         │          VALIDATION LAYER                 │
                         │  Macroeconomic indicators (CPI, FX, etc.) │
                         │  Narrative lead analysis                  │
                         └──────────────────────────────────────────┘
```

### Data Model

For each article, BENI 2.0 should store a rich structured record:

```json
{
  "article_id": "beni_2024_001234",
  "source": "Prothom Alo",
  "date": "2024-06-15",
  "section": "Economy",
  "headline": "...",
  "text": "...",
  "embedding": [0.123, -0.456, ...],
  "topic_cluster": "inflation_food",
  "topic_confidence": 0.87,
  "narratives": [
    {
      "text": "government spending drives inflation",
      "cause": "government spending increase",
      "effect": "rising inflation",
      "actor": "government",
      "stance": "negative",
      "causal_marker": "because",
      "confidence": 0.92,
      "span": [120, 145]
    }
  ],
  "narrative_force": "blame",
  "valuation_target": "government",
  "sentiment": "negative",
  "entities": [
    {"name": "Bangladesh Bank", "type": "central_bank", "mentions": 3}
  ],
  "events": [
    {"type": "rate_hike", "date": "2024-06-10", "confidence": 0.95}
  ],
  "has_causal_claim": true,
  "narrative_graph_id": "ng_789"
}
```

### Monthly Index Expansion

| Current Index | BENI 2.0 Additional Indices |
|---------------|---------------------------|
| BENI Aggregate Economic Index | BENI Inflation Narrative Index |
| — | BENI Exchange-Rate Pressure Index |
| — | BENI Blame Index (who gets blamed for economic conditions) |
| — | BENI Narrative Force Index (crisis vs. stability balance) |
| — | BENI Actor Centrality Index (which actors dominate narratives) |
| — | BENI Narrative Velocity Index (how fast narratives change) |
| — | BENI Section Migration Score (cross-section narrative spread) |

### Validation Extension

| Current | BENI 2.0 |
|---------|----------|
| CPI level correlation | CPI nowcasting with MIDAS regression |
| FX level correlation | Narrative lead-lag analysis (Granger causality) |
| Reserves correlation | Narrative velocity → volatility forecasting |
| — | Narrative-implied inflation expectations vs. survey measures |
| — | Cross-language narrative convergence (BENI + AENI + NENI) |

### Implementation Priority

| Phase | Levels | Components | Timeline |
|-------|--------|------------|----------|
| **Phase 1** | L4 + L3 | Embedding-based narrative clustering, BERTopic, dynamic topics | Q3 2026 |
| **Phase 2** | L10→L7 | Enhanced LLM extraction with cause-effect, causal schema update | Q4 2026 |
| **Phase 3** | L8 | Narrative graph construction, actor-event networks | Q1 2027 |
| **Phase 4** | L5 + L6 | Event detection, semantic role labeling, narrative chains | Q1 2027 |
| **Phase 5** | L9 | RELATIO-style cross-document aggregation | Q2 2027 |
| **Phase 6** | L11 | Continuous ingestion, agentic discovery, multi-language coordination | H2 2027 |

---

## Research Frontier & Open Problems

### Current Frontier (2025–2026)

The cutting edge of economic narrative extraction sits at the intersection of:

1. **Causal extraction** (Level 7) — Moving from topic detection to mechanism extraction remains the central challenge
2. **LLM-based extraction** (Level 10) — Reliability, reproducibility, and cost at scale
3. **Cross-lingual transfer** — Do extraction methods trained on English economic text transfer to Bangla, Hausa, or Vietnamese?
4. **Validation methodology** — How do we validate a narrative index when the ground truth is also a contested narrative?

### Open Problems for BENI

1. **Detrended correlation** — The BENI TF-IDF index shows strong level correlations but weak detrended correlations. Is this a model limitation (TF-IDF) or a structural feature (economic news share is slow-moving)?
2. **Section-aware index construction** — The BENI Novelty Agenda proposes treating newspaper sections as distinct institutional spaces. How do we weight narratives across sections?
3. **Narrative vs. sentiment** — The BENI index currently measures economic *relevance* (presence/absence), not *valence* (positive/negative) or *causal structure* (why). Which matters more for nowcasting?
4. **Gold-standard scarcity** — With only 300 planned manually annotated articles, how do we reliably evaluate LLM extraction quality?
5. **Temporal validation** — The current index runs 2014–2020. Extending to 2025+ requires continuous data collection and model updating.

### Future Directions

- **Multimodal narrative extraction** — Integrating text + images + audio for richer narrative understanding
- **Narrative forecasting** — Using narrative graph dynamics to forecast economic events before they materialize in statistics
- **Causal narrative competition** — Modeling multiple competing causal narratives about the same economic phenomenon

---

## References

### Narrative Economics — Foundational

1. Shiller, R. J. (2017). "Narrative Economics." *American Economic Review*, 107(4): 967–1004. DOI: `10.1257/aer.107.4.967`.
   — The foundational text. Introduces epidemic models for narrative transmission.

2. Roos, M. W. M. & Reccius, M. (2021). "Narratives in Economics." *Ruhr Economic Papers #922*.
   — Defines the Collective Economic Narrative (CEN): a sense-making story about an economically relevant topic, shared by a group, that suggests actions. Five essential characteristics.

3. Andre, P., Haaland, I., Roth, C., Wiederholt, M., & Wohlfart, J. (2026). "Narratives about the Macroeconomy." *Review of Economic Studies* (accepted).
   — DAG-based narrative extraction from 10,000+ US households. Demonstrates that narratives causally shape inflation expectations.

4. Blesse, S., Gruendler, K., Heil, P., & Hermes, H. (2025). "Demand for Economic Narratives." *IZA DP #18205*.
   — Households' willingness to pay for narratives exceeds $4. Accuracy concerns and motivated beliefs both drive demand.

### Survey Papers

5. Norambuena, B. K., Mitra, T., & North, C. (2023). "A Survey on Event-based News Narrative Extraction." *ACM Computing Surveys*, 55(14s): 1–39. DOI: `10.1145/3584741`. arXiv: `2302.08351`.
   — Screened 900+ articles. Three resolution levels: events as sentences, documents, clusters.

6. Santana, B., Campos, R., Amorim, E., Jorge, A., Silvano, P., & Nunes, S. (2023). "A survey on narrative extraction from textual data." *Artificial Intelligence Review*, 56(8): 8393–8435. DOI: `10.1007/s10462-022-10338-7`.
   — Organizes the field as a pipeline: preprocessing → component identification → linkage → formal representation → evaluation.

7. Asghar, N. (2022). "A survey on extraction of causal relations from natural language text." *Knowledge and Information Systems*, 65: 773–816. arXiv: `2101.06426`.
   — Three causal forms: explicit intra-sentential, implicit, inter-sentential. Covers knowledge-based, statistical ML, and deep learning approaches.

8. Drury, B., Gonçalo Oliveira, H., & de Andrade Lopes, A. (2022). "A survey of the extraction and applications of causal relations." *Natural Language Engineering*, 28(3): 361–400. DOI: `10.1017/S135132492100036X`.
   — Comprehensive survey of practical causal extraction applications. Transformer-XL advances.

### Causal Extraction & Narrative Graphs

9. Garg, P. & Fetzer, T. (2026). "Causal Claims in Economics." arXiv: `2501.06873`. Code: `github.com/prashgarg/CausalClaimsInEconomics`.
   — 44,852 economics papers (1980–2023) → directed causal claim graphs. Causal edge share rose from 7.7% (1990) to 31.7% (2020). Multi-stage LLM pipeline.

10. Norouzi, R., Kleinberg, B., Vermunt, J. K., & van Lissa, C. J. (2025). "Capturing Causal Claims: A Fine-Tuned Text Mining Model."
    — Fine-tuned BERT on 529 manually annotated causal sentences (social science). F1 = 0.89. Documents domain shift bias (~5% drop).

11. Tian, Q. et al. (2026). "Narrative Knowledge Weaver." *ICLR 2026*.
    — Multi-agent framework: adaptive schema induction → reflection-augmented extraction → normalization-before-merge → Event Plot Graphs (EPGs). Outperforms GraphRAG on narrative QA.

12. Salloum, C. et al. (2025). "Modeling cross-platform narrative templates: a temporal knowledge graph approach." *Social Network Analysis and Mining*, 15: 14. DOI: `10.1007/s13278-025-01429-8`.
    — Temporal KGs for cross-platform narrative analysis. Applied to 26,000+ posts across Instagram, TikTok, X, YouTube.

### LLM & RELATIO-Style Extraction

13. Ash, E., Gauthier, G., & Widmer, P. (2023). "RELATIO: Text Semantics Capture Political and Economic Narratives." *Political Analysis* (Cambridge University Press). arXiv: `2108.01720`. Code: `github.com/relatio-nlp/relatio`.
    — Unsupervised AVP/SVO triplet extraction + entity clustering (KMeans/HDBSCAN on embeddings). U.S. Congressional Record application.

14. Schmidt, T., Lange, K.-R., Reccius, M., Müller, H., Roos, M. W. M., & Jentsch, C. (2025). "Identifying economic narratives in large text corpora: An integrated approach using large language models." *Ruhr Economic Papers #1163*. DOI: `10.4419/96973348`.
    — Tests GPT-4o against expert-annotated gold-standard narratives. Finds LLMs fall short of expert-level performance on complex documents.

15. Lange, K.-R., Reccius, M., Schmidt, T., Müller, H., Roos, M. W. M., & Jentsch, C. (2022). "Towards extracting collective economic narratives from texts." *Ruhr Economic Papers #963*. DOI: `10.4419/96973127`.
    — Augments RELATIO with coreference resolution and noise filtering. Causal linking step is core contribution. Evaluated on Financial Times data.

### BENI & Multilingual Economic NLP

16. Nabil, A. N. (2026). "BENI v1.0: A Harmonised Bangla News Dataset for Economic Narrative Measurement." *HuggingFace Datasets*. DOI: `10.5281/zenodo.20585401`.
    — 1.47M Bangla news articles (2014–2024), deduplicated, with economic seed labels, TF-IDF predictions, and monthly narrative index.

17. Nabil, A. N. (2026). "BENI Global 10: A Multilingual Economic News Dataset for Narrative Measurement." arXiv: `2606.10225`. Code: `github.com/nabil0x/beni-multilingual`.
    — 522K economically relevant articles from 2.8M raw documents across 10 languages. Keyword-translation filtering, streaming pipeline, XLM-R macro F1 > 0.88.

18. Nabil, A. N. (2026). "LILA Lab: Language Intelligence for Low-resource Applications." GitHub. URL: `github.com/LilaLABx/LILA-LAB`.
    — Open-source XENI pipeline framework for emerging-economy languages. BENI is the flagship pipeline.

19. Nabil, A. N. (2026). "Potrika: A Bangla News Corpus." *Mendeley Data*, v4. DOI: `10.17632/v362rp78dc.4`.
    — 664K Bangla news articles (2014–2020), 6 newspapers, 39 CSV files. Primary data source for BENI.

### BERTopic in Financial/Economic NLP

20. Jehnen, S. et al. (2025). "FinTextSim: A Fine-Tuned Sentence Transformer for Financial Text." arXiv: `2504.15683`. Code: `github.com/JehnenS/FinTextSim`.
    — BERTopic with domain-specific embeddings: topic accuracy 0.81 vs 0.06 for all-MiniLM on financial text.

21. Grootendorst, M. (2022). "BERTopic: Neural topic modeling with a class-based TF-IDF procedure." arXiv: `2203.05794`.
    — BERTopic algorithm: sentence embeddings → UMAP → HDBSCAN → c-TF-IDF topic representation.

### Tool & Methodology References

22. Reimers, N. & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks." *EMNLP 2019*.
    — SBERT for dense document embeddings in narrative discovery.

23. Wang, L. et al. (2024). "Multilingual E5 Text Embeddings: A Technical Report." arXiv: `2402.05672`.
    — State-of-the-art multilingual embeddings supporting Bangla and other XENI target languages.

24. McInnes, L. & Healy, J. (2018). "UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction." *JOSS*.
    — Dimensionality reduction for narrative embedding visualization and clustering.

25. McInnes, L. et al. (2017). "hdbscan: Hierarchical density based clustering." *JOSS*.
    — HDBSCAN for narrative cluster identification from embeddings.

26. Lazer, D. et al. (2009). "Computational Social Science." *Science*, 323(5915): 721–723.
    — The computational social science paradigm that motivates narrative measurement.

---

## Appendix A: Quick Reference — Level Selection Guide

| If you want to... | Start at Level | Full Methodology Page |
|-------------------|---------------|----------------------|
| Count how often a narrative appears | L1: Lexicon | [→](methodologies/L01_lexicon_based_detection.md) |
| Discover what narratives exist in a corpus | L3: Topic Modeling / L4: Embedding | [→](methodologies/L03_topic_modeling.md) / [→](methodologies/L04_embedding_based_discovery.md) |
| Extract who is doing what | L6: Semantic Role | [→](methodologies/L06_semantic_role_extraction.md) |
| Extract causal claims | L7: Causal Extraction | [→](methodologies/L07_causal_narrative_extraction.md) |
| Build a narrative network | L8: Narrative Graphs | [→](methodologies/L08_narrative_networks_graphs.md) |
| Extract narratives at scale with deep understanding | L10: LLM-Based | [→](methodologies/L10_llm_based_extraction.md) |
| Build a continuous narrative monitoring system | L11: Agentic | [→](methodologies/L11_agentic_discovery_systems.md) |
| Create gold-standard evaluation data | L0: Manual Coding | [→](methodologies/L00_manual_qualitative_coding.md) |

## Appendix B: Quick Reference — Level × Language Matrix for XENI

| Language | L0 Manual | L1 Lexicon | L2 TF-IDF | L3 Topic | L4 Embedding | L10 LLM |
|----------|-----------|------------|-----------|----------|--------------|---------|
| **BENI** (Bangla) | ✅ In progress | ✅ 3 lexicons | ✅ 91.7% acc | 🔄 Planned | ⬜ | ✅ Multi-LLM |
| **AENI** (Assamese) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| **NENI** (Nepali) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| **HENI** (Hausa) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| **KIENI** (Swahili) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| **VIENI** (Vietnamese) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| **TIENI** (Tagalog) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| **IDENI** (Indonesian) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| **CENI** (Chittagonian) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| **SENI** (Sylheti) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

**Key insight:** BENI's Level 10 (LLM) pipeline can be applied to any language with zero-shot transfer. The main gap for new XENI pipelines is L0–L4. LLMs can bootstrap annotation while lower-level resources are developed.
