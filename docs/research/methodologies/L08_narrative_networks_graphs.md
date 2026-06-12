> **Navigation:** [Documentation Portal](../../index.md) > [Research](../) > [Methodologies](./) > Level 8
>
> ---

# Level 8: Narrative Networks and Graphs

> **Hierarchy:** Narratives become graph structures — nodes are actors, concepts, and events; edges are causal, supporting, opposing, or temporal relations.
> **BENI Status:** ⬜ Not Yet Implemented
> **Core Idea:** Construct and query graph representations of narrative structures to reveal how actors, events, and causal claims connect across documents and time.

---

## Table of Contents

1. [Overview](#overview)
2. [Why Graphs for Narratives](#why-graphs-for-narratives)
3. [Graph Components](#graph-components)
4. [Narrative Graph Types](#narrative-graph-types)
5. [Knowledge Graphs for Narratives](#knowledge-graphs-for-narratives)
6. [Temporal Knowledge Graphs](#temporal-knowledge-graphs)
7. [Cross-Platform Narrative Templates](#cross-platform-narrative-templates)
8. [Worked Example](#worked-example)
9. [Strengths & Weaknesses](#strengths--weaknesses)
10. [When to Use Level 8](#when-to-use-level-8)
11. [BENI Implementation Guide](#beni-implementation-guide)
12. [References](#references)

---

## Overview

Narrative networks and graphs elevate narrative extraction from isolated document-level claims to **relational structures** that span entire corpora. Where Level 7 extracts individual causal claims, Level 8 connects those claims into networks — revealing how actors, events, concepts, and causal mechanisms relate to one another across thousands of documents.

### Key Principle

**Narratives are inherently relational.** A narrative about "government spending causing inflation" involves multiple entities (government, central bank, consumers), events (budget announcement, price increases), and causal links. Representing these as a graph enables queries that are impossible with flat document representations:

- Which actors are most central to economic narratives in 2024?
- How does the "inflation" narrative connect to the "election" narrative?
- Which causal claims co-occur most frequently?

---

## Why Graphs Matter for Economics

Economic narratives are particularly well-suited to graph representations because:

| Characteristic | Implication | Graph Benefit |
|----------------|-------------|---------------|
| **Multiple actors** | Government, central bank, firms, households | Actor centrality analysis |
| **Causal chains** | A → B → C → D | Path traversal and pattern mining |
| **Temporal evolution** | Narratives change over time | Temporal subgraph comparison |
| **Cross-domain spread** | Economic → Political → Social | Cross-domain edge detection |
| **Competing narratives** | Different causal explanations for same phenomenon | Structural equivalence analysis |

### BENI Relevance

The BENI index currently tracks *whether* an article is economic and *what narrative force* it uses. Narrative graphs would track *how economic narratives connect to each other* — revealing narrative ecosystems rather than isolated threads.

---

## Graph Components

### Nodes

| Node Type | Description | Examples |
|-----------|-------------|----------|
| **Actor** | Entity that acts or is acted upon | Government, Bangladesh Bank, IMF, Consumers |
| **Concept** | Abstract economic idea | Inflation, Growth, Stability, Crisis |
| **Event** | Discrete occurrence | Rate hike, Budget announcement, Election |
| **Causal Claim** | Cause-effect statement | "Spending → Inflation" |
| **Document** | Source article | Article ID, metadata |

### Edges

| Edge Type | Description | Symbol |
|-----------|-------------|--------|
| **Causes** | Direct causal relation | → |
| **Supports** | Reinforces or agrees with | + |
| **Opposes** | Contradicts or undermines | − |
| **Temporal** | Chronological ordering | \< \> |
| **Mentions** | Document references entity | — |
| **Hierarchical** | Is-a, part-of relationship | ⊂ |
| **Co-occurs** | Statistical co-occurrence | ∼ |

### Graph Schema

```json
{
  "nodes": [
    {"id": "govt", "type": "actor", "label": "Government", "properties": {}},
    {"id": "inflation", "type": "concept", "label": "Inflation", "properties": {}},
    {"id": "rate_hike_2024", "type": "event", "label": "Rate Hike June 2024", "properties": {"date": "2024-06-15"}},
    {"id": "claim_001", "type": "causal_claim", "label": "Spending drives inflation", "properties": {"confidence": 0.92}}
  ],
  "edges": [
    {"source": "govt", "target": "inflation", "type": "causes", "weight": 0.85, "temporal": "2024-01/2024-06"},
    {"source": "inflation", "target": "rate_hike_2024", "type": "causes", "weight": 0.9},
    {"source": "claim_001", "target": "govt", "type": "mentions", "weight": 1.0}
  ]
}
```

---

## Narrative Graph Types

### Type 1: Actor-Concept Graph

Nodes are actors and economic concepts. Edges represent which actors are associated with which concepts. Reveals **blame attribution** patterns.

```python
import networkx as nx

def build_actor_concept_graph(annotated_articles):
    """Build graph connecting actors to economic concepts they're linked with."""
    G = nx.Graph()
    for article in annotated_articles:
        actor = article["valuation_target"]
        concept = article["economic_topic"]
        G.add_edge(actor, concept, weight=G.get_edge_data(actor, concept, {}).get("weight", 0) + 1)
    return G
```

### Type 2: Event Chain Graph

Directed graph where nodes are events and edges are temporal or causal links. Reveals **narrative sequences**.

```python
def build_event_chain(events_with_temporal_order):
    """Build a directed graph of causally and temporally linked events."""
    G = nx.DiGraph()
    for i, event_a in enumerate(events_with_temporal_order):
        for event_b in events_with_temporal_order[i+1:]:
            if is_causally_linked(event_a, event_b):
                G.add_edge(event_a["id"], event_b["id"], relation="causes")
            elif is_temporally_ordered(event_a, event_b):
                G.add_edge(event_a["id"], event_b["id"], relation="precedes")
    return G
```

### Type 3: Causal Claim Graph

Nodes are causal claims (from Level 7). Edges represent shared actors, concepts, or mechanisms. Reveals **narrative competition and reinforcement**.

```python
def build_causal_claim_graph(causal_claims):
    """Connect causal claims that share actors or concepts."""
    G = nx.Graph()
    for claim in causal_claims:
        G.add_node(claim["id"], label=claim["text"], type=claim["type"])
    # Connect claims sharing the same cause or effect
    for c1 in causal_claims:
        for c2 in causal_claims:
            if c1["id"] >= c2["id"]:
                continue
            if c1["cause"] == c2["cause"] or c1["effect"] == c2["effect"]:
                G.add_edge(c1["id"], c2["id"], relation="shares_component")
            if c1["cause"] == c2["effect"] or c1["effect"] == c2["cause"]:
                G.add_edge(c1["id"], c2["id"], relation="opposes")
    return G
```

### Type 4: Document-Entity Graph

Bipartite graph linking documents to entities they mention. Enables **cross-document narrative aggregation**.

```python
def build_document_entity_graph(documents, extracted_entities):
    """Bipartite graph: documents ↔ entities."""
    G = nx.Graph()
    for doc_id, entities in zip(documents, extracted_entities):
        for entity in entities:
            G.add_edge(f"doc:{doc_id}", f"entity:{entity['name']}",
                       weight=entity["mentions"], type="mentions")
    return G
```

---

## Knowledge Graphs for Narratives

### From Triples to Narrative Graphs

The most direct path from Level 6/7 data to a narrative graph:

```
Article Text
    ↓
Entity Extraction (L6) → (Actor, Action, Target) triples
Causal Extraction (L7) → (Cause, Relation, Effect) triples
    ↓
Triple Aggregation → Knowledge Graph
    ↓
Graph Queries → Narrative Insights
```

### Storage Options

| Storage | Best For | Query Language | BENI Suitability |
|---------|----------|----------------|------------------|
| **NetworkX** | Research, prototyping | Python-native | ✅ Best for initial exploration |
| **Neo4j** | Production graph DB | Cypher | ⭐ When scaling to 100K+ nodes |
| **RDF/SPARQL** | Linked data, interoperability | SPARQL | 🔄 If integrating with external KGs |
| **iGraph** | Large-scale graph analytics | Python, R | ⭐ For fast centrality/community detection |
| **PyTorch Geometric** | GNN-based analysis | Python | 🔄 For advanced graph ML |

### NetworkX Narrative Graph

```python
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

class NarrativeGraph:
    """Full narrative graph with query capabilities."""

    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_causal_claim(self, claim_id, cause, effect, claim_type,
                         source_doc=None, date=None, confidence=1.0):
        """Add a causal claim as graph edges."""
        # Add nodes
        self.graph.add_node(cause, type="concept", node_type="cause")
        self.graph.add_node(effect, type="concept", node_type="effect")
        # Add edge
        self.graph.add_edge(cause, effect, key=claim_id,
                            relation="causes", type=claim_type,
                            source=source_doc, date=date,
                            confidence=confidence)

    def add_actor(self, actor_id, actor_type):
        self.graph.add_node(actor_id, type="actor", actor_type=actor_type)

    def add_actor_claim(self, actor_id, claim_id, role="agent"):
        self.graph.add_edge(actor_id, claim_id, relation=role)

    def centrality_by_type(self, node_type):
        """Compute degree centrality for a specific node type."""
        subgraph = nx.Graph(self.graph)
        nodes = [n for n, d in self.graph.nodes(data=True)
                 if d.get("type") == node_type]
        if not nodes:
            return {}
        sub = subgraph.subgraph(nodes)
        return nx.degree_centrality(sub)

    def most_central_actors(self, top_k=10):
        """Which actors appear most in narrative structures."""
        cent = self.centrality_by_type("actor")
        return sorted(cent.items(), key=lambda x: x[1], reverse=True)[:top_k]

    def narrative_communities(self):
        """Detect narrative communities using Louvain algorithm."""
        G_simple = nx.Graph(self.graph)
        from networkx.algorithms.community import louvain_communities
        return louvain_communities(G_simple)

    def temporal_subgraph(self, start_date, end_date):
        """Extract subgraph for a specific time period."""
        edges = [
            (u, v, k, d) for u, v, k, d in self.graph.edges(data=True, keys=True)
            if d.get("date") and start_date <= d["date"] <= end_date
        ]
        sg = nx.MultiDiGraph()
        for u, v, k, d in edges:
            sg.add_edge(u, v, key=k, **d)
        return sg

    def narrative_drift(self, period_a, period_b):
        """Measure how narrative structure changes between two periods."""
        ga = self.temporal_subgraph(period_a[0], period_a[1])
        gb = self.temporal_subgraph(period_b[0], period_b[1])
        # Graph edit distance or Jaccard similarity on edges
        edges_a = set(ga.edges())
        edges_b = set(gb.edges())
        if not edges_a and not edges_b:
            return 1.0
        jaccard = len(edges_a & edges_b) / len(edges_a | edges_b)
        return 1 - jaccard  # drift score: 0 = identical, 1 = completely different
```

---

## Temporal Knowledge Graphs

Temporal knowledge graphs (TKGs) add a time dimension — edges are valid only during specific time windows. This is essential for narrative tracking because narratives evolve.

### TKG Representation

```python
class TemporalNarrativeGraph:
    """Narrative graph with time-aware edges."""

    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.temporal_edges = {}  # (u, v, k) → (start, end)

    def add_temporal_edge(self, u, v, key, start_date, end_date=None, **attrs):
        self.graph.add_edge(u, v, key=key, **attrs)
        self.temporal_edges[(u, v, key)] = (start_date, end_date)

    def query_at_time(self, date):
        """Return graph snapshot at a specific date."""
        sg = nx.MultiDiGraph()
        for u, v, k, d in self.graph.edges(data=True, keys=True):
            start, end = self.temporal_edges.get((u, v, k), (None, None))
            if start and start <= date:
                if end is None or date <= end:
                    sg.add_edge(u, v, key=k, **d)
        return sg
```

### TKG Query Examples

```python
# What causal claims were active in Q3 2024?
q3_2024 = tkg.query_at_time("2024-07-01")
print(f"Active causal edges: {q3_2024.number_of_edges()}")

# How did the blame attribution graph evolve?
for quarter in ["2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4"]:
    sg = tkg.query_at_time(quarter)
    govt_blame = sum(1 for _, v, d in sg.edges(data=True)
                     if v == "government" and d.get("stance") == "negative")
    print(f"{quarter}: Government blame mentions = {govt_blame}")
```

---

## Cross-Platform Narrative Templates

One of the most advanced applications of narrative graphs: modeling how the same narrative manifests across different platforms (news, social media, policy speeches).

### Template Approach (Salloum et al., 2025)

```
Cross-Platform Narrative Template = {
    "core_narrative": "Government spending causes inflation",
    "platform_variants": {
        "news": "Fiscal expansion drives price increases",
        "social": "Govt is printing too much money!!!!",
        "speech": "We must exercise fiscal discipline to contain inflation"
    },
    "actors": ["Government", "Central Bank"],
    "temporal_trace": ["2024-01: news spike", "2024-02: social amplification",
                       "2024-03: policy response"],
    "cross_platform_edges": [
        {"from": "news_article_001", "to": "social_post_005", "relation": "amplifies"},
        {"from": "social_post_005", "to": "speech_012", "relation": "influences"}
    ]
}
```

### BENI Relevance for Cross-Platform Graphs

BENI currently tracks newspaper narratives only. Extending to cross-platform graphs would enable:

1. **Narrative amplification** — Do social media narratives amplify or distort news narratives?
2. **Platform lead-lag** — Which platform leads on which economic narrative?
3. **Narrative contagion** — How do narratives spread from news to social media to policy?
4. **Cross-language narrative graphs** — How does the same economic narrative differ across Bangla, English, and other languages in the XENI framework?

---

## Worked Example

### Scenario

Tracking the "inflation" narrative across Bangla news in June 2024 — building a narrative graph from 500 articles.

### Step 1: Extract Narrative Components

Using existing LLM pipeline (Level 10) to extract actors, events, and causal claims:

```json
{
  "articles_processed": 500,
  "actors_extracted": ["Government", "Bangladesh Bank", "Consumers",
                       "Businesses", "IMF", "Farmers"],
  "events_detected": ["Rate hike June 2024", "Budget announcement",
                      "Flood damage assessment", "Export growth report"],
  "causal_claims": [
    {"cause": "government spending", "effect": "inflation", "count": 145},
    {"cause": "supply chain disruption", "effect": "food prices", "count": 98},
    {"cause": "rate hike", "effect": "slower growth", "count": 72}
  ]
}
```

### Step 2: Construct Narrative Graph

```python
ng = NarrativeGraph()

# Add causal claims
ng.add_causal_claim("c1", "government spending", "inflation",
                    "demand_pull", confidence=0.85)
ng.add_causal_claim("c2", "supply chain disruption", "food prices",
                    "cost_push", confidence=0.9)
ng.add_causal_claim("c3", "rate hike", "slower growth",
                    "policy_response", confidence=0.75)

# Add actors
ng.add_actor("Government", "fiscal_authority")
ng.add_actor("Bangladesh Bank", "monetary_authority")
ng.add_actor("Consumers", "household")

# Connect actors to claims
ng.add_actor_claim("Government", "c1")
ng.add_actor_claim("Bangladesh Bank", "c3")
```

### Step 3: Query the Graph

```python
# Most central actors
print(ng.most_central_actors(top_k=5))
# → [("Government", 0.42), ("Bangladesh Bank", 0.38), ("Consumers", 0.21), ...]

# Narrative communities
communities = ng.narrative_communities()
for i, comm in enumerate(communities):
    print(f"Community {i}: {comm}")
# → Community 0: {government spending, inflation, Government, demand_pull}
# → Community 1: {supply chain, food prices, Farmers, cost_push}
# → Community 2: {rate hike, slower growth, Bangladesh Bank, policy_response}
```

### Step 4: Visualize Narrative Structure

```text
                  ┌──────────────────┐
                  │   Government     │
                  └────────┬─────────┘
                           │ [blamed for]
                           ▼
                  ┌──────────────────┐
         ┌───────│ government spending│───────┐
         │       └──────────────────┘       │
         │ [causes]                         │ [causes]
         ▼                                   ▼
┌──────────────────┐               ┌──────────────────┐
│    Inflation     │               │   Rate Hike      │
└──────────────────┘               └────────┬─────────┘
         │                                    │ [causes]
         │                                    ▼
         │                           ┌──────────────────┐
         └───────────────────────────│  Slower Growth   │
                                     └──────────────────┘

                  ┌──────────────────┐
                  │ Supply Chain     │──→ Food Prices
                  └──────────────────┘
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Description |
|----------|-------------|
| **Relational understanding** | Captures how narratives connect, not just what they contain |
| **Cross-document synthesis** | Aggregates signals across thousands of documents |
| **Actor centrality** | Quantifies which actors dominate narrative discourse |
| **Community detection** | Discovers latent narrative groupings |
| **Temporal comparison** | Measures narrative drift over time |
| **Visualization** | Graphs are inherently visual and interpretable |

### Weaknesses

| Weakness | Description | Mitigation |
|----------|-------------|------------|
| **Construction complexity** | Building quality graphs requires robust extraction upstream | Leverage existing L10 pipeline |
| **Scalability** | Million-node graphs require specialized infrastructure | Batch processing, graph DBs |
| **Noise sensitivity** | Poor entity resolution creates spurious edges | Deduplication, confidence thresholds |
| **Temporal sparsity** | Short time windows may produce sparse graphs | Aggregation windows (monthly) |
| **Interpretation** | Graph metrics need narrative interpretation | Domain-aware analysis protocols |

---

## When to Use Level 8

| Scenario | Recommended | Alternative |
|----------|-------------|-------------|
| Analyzing actor dominance in narratives | ✅ **Level 8** | — |
| Tracking narrative evolution over time | ✅ **Level 8** | — |
| Cross-document narrative aggregation | ✅ **Level 8** | — |
| Detecting narrative communities | ✅ **Level 8** | — |
| Simple narrative prevalence tracking | ❌ Overkill | L1 or L2 |
| Single-document causal extraction | ❌ Overkill | L7 or L10 |
| First-time corpus exploration | ❌ Overkill | L3 or L4 first |

---

## BENI Implementation Guide

### Phase 1: NetworkX Prototype (2 weeks)

The quickest path: build narrative graphs using the existing LLM annotation output.

```python
import json
import networkx as nx
from collections import Counter
from pathlib import Path

def build_beni_narrative_graph(annotations_dir):
    """Build narrative graph from BENI LLM annotations."""
    G = nx.MultiDiGraph()
    annotation_files = Path(annotations_dir).glob("*.json")

    for file in annotation_files:
        with open(file) as f:
            data = json.load(f)

        # Extract annotation fields
        article_id = data.get("article_id")
        topic = data.get("economic_topic")
        force = data.get("narrative_force")
        target = data.get("valuation_target")
        sentiment = data.get("sentiment")

        # Add nodes
        if topic:
            G.add_node(f"topic:{topic}", type="topic")
        if force:
            G.add_node(f"force:{force}", type="narrative_force")
        if target:
            G.add_node(f"target:{target}", type="valuation_target")

        # Add edges linking them
        if topic and target:
            G.add_edge(f"topic:{topic}", f"target:{target}",
                       relation="mentions", article=article_id,
                       sentiment=sentiment)

    return G
```

### Phase 2: Temporal Narrative Graph (2 weeks)

Add time-awareness using BENI's 79-month window:

```python
def build_temporal_beni_graph(annotations_df):
    """Build monthly narrative graphs from BENI annotations."""
    tng = TemporalNarrativeGraph()
    annotations_df["month"] = pd.to_datetime(annotations_df["date"]).dt.to_period("M")

    for month, group in annotations_df.groupby("month"):
        for _, row in group.iterrows():
            # Monthly edges
            tng.add_temporal_edge(
                f"topic:{row['economic_topic']}",
                f"target:{row['valuation_target']}",
                key=row["article_id"],
                start_date=month.start_time,
                end_date=month.end_time,
                sentiment=row["sentiment"],
                force=row["narrative_force"],
            )

    return tng

# Query: How did government blame evolve?
govt_blame_series = []
for month in beni_months:
    sg = tng.query_at_time(month)
    blame_edges = [
        d for _, _, d in sg.edges(data=True)
        if "government" in str(d.get("target", ""))
        and d.get("sentiment") == "negative"
    ]
    govt_blame_series.append(len(blame_edges))
```

### Phase 3: Narrative Index from Graph (1 week)

```python
def graph_based_narrative_index(tng, months):
    """Compute narrative indices from graph properties."""
    indices = []
    for month in months:
        sg = tng.query_at_time(month)
        if sg.number_of_nodes() == 0:
            continue

        # Graph-level metrics
        density = nx.density(sg)
        n_components = nx.number_weakly_connected_components(sg)

        # Actor centrality
        centrality = nx.degree_centrality(sg)
        top_actors = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]

        indices.append({
            "month": month,
            "nodes": sg.number_of_nodes(),
            "edges": sg.number_of_edges(),
            "density": density,
            "narrative_communities": n_components,
            "top_actors": [a for a, _ in top_actors],
            "actor_concentration": top_actors[0][1] if top_actors else 0,
        })

    return pd.DataFrame(indices)
```

### Integration with Existing BENI Pipeline

```
BENI TF-IDF Index  ──→  Article-level relevance
            ↓
BENI LLM Annotation  ──→  Narrative components (topics, actors, forces)
            ↓
    Narrative Graph  ──→  Relational structure
            ↓
 Graph Narrative Index  ──→  Density, centrality, community metrics
            ↓
   BENI 2.0 Indices  ──→  Richer narrative measurement
```

### Infrastructure Requirements

```bash
pip install networkx pandas matplotlib  # Phase 1
pip install neo4j py2neo               # Phase 2 (optional, for scale)
pip install python-louvain             # Phase 3 (community detection)
```

---

## References

### Core Reading

- Salloum, C. et al. (2025). "Modeling cross-platform narrative templates: a temporal knowledge graph approach." *Social Network Analysis and Mining*, 15: 14. DOI: `10.1007/s13278-025-01429-8`.
  — Temporal KGs for cross-platform narrative analysis. Applied to 26,000+ posts across Instagram, TikTok, X, YouTube.

- Tian, Q. et al. (2026). "Narrative Knowledge Weaver." *ICLR 2026*.
  — Multi-agent framework: adaptive schema induction → reflection-augmented extraction → normalization-before-merge → Event Plot Graphs (EPGs). Outperforms GraphRAG on narrative QA.

- Garg, P. & Fetzer, T. (2026). "Causal Claims in Economics." arXiv: `2501.06873`.
  — 44,852 economics papers → directed causal claim graphs. Causal edge share rose from 7.7% (1990) to 31.7% (2020).

### Narrative Graphs

- Norambuena, B. K., Mitra, T., & North, C. (2023). "A Survey on Event-based News Narrative Extraction." *ACM Computing Surveys*, 55(14s): 1–39.
  — Three resolution levels for narrative graphs: events as sentences, documents, clusters.

- Lange, K.-R. et al. (2022). "Towards extracting collective economic narratives from texts." *Ruhr Economic Papers #963*.
  — Causal linking as core contribution toward narrative graphs.

### Tools

- Hagberg, A. et al. (2008). "Exploring Network Structure, Dynamics, and Function using NetworkX." *SciPy 2008*.
  — NetworkX: Python graph library for narrative graph prototyping.

- Neo4j Graph Platform. — Production graph database for narrative graphs at scale.

### See Also

- Level 6: [Semantic Role Extraction](L06_semantic_role_extraction.md) — Entity-relation triples feed graph construction
- Level 7: [Causal Narrative Extraction](L07_causal_narrative_extraction.md) — Causal claims as graph edges
- Level 9: [RELATIO-Style Extraction](L09_relatio_style_extraction.md) — Cross-document aggregation into narrative structures
- Level 11: [Agentic Discovery Systems](L11_agentic_discovery_systems.md) — Continuous graph updating

---

**Up:** [Methodologies Index](INDEX.md) | **Main:** [Narrative Extraction Methodologies](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
