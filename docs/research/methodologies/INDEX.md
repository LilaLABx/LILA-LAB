> **Navigation:** [Documentation Portal](../../index.md) > [Research](../) > Methodologies — Index
>
> ---

# Narrative Extraction Methodologies — Index

> **Quick navigation guide** for the 12-level hierarchy of narrative extraction methods, from manual qualitative coding to autonomous agentic systems.
> **Related:** [Full Reference Document](../NARRATIVE_EXTRACTION_METHODOLOGIES.md) | [BENI Pipeline](../../pipelines/BENI/)

---

## The Hierarchy at a Glance

| Level | Method | Core Technique | Narrative Understanding | BENI Status |
|-------|--------|---------------|----------------------|-------------|
| **L0** | [Manual Qualitative Coding](L00_manual_qualitative_coding.md) | Human annotation, thematic analysis | Deep interpretation | ✅ Gold-standard reference set |
| **L1** | [Lexicon-Based Detection](L01_lexicon_based_detection.md) | Keyword matching, dictionaries | Topic presence | ✅ `narrative.py` — 3 Bangla lexicons |
| **L2** | [Statistical Text Mining](L02_statistical_text_mining.md) | TF-IDF, N-grams, PMI, co-occurrence | Word clusters | ✅ TF-IDF (80k features, 91.7%) |
| **L3** | [Topic Modeling](L03_topic_modeling.md) | LDA, HDP, NMF, BERTopic | Latent themes | 🔄 Planned (BERTopic, keyATM) |
| **L4** | [Embedding-Based Discovery](L04_embedding_based_discovery.md) | SBERT, E5, BGE, UMAP + HDBSCAN | Semantic clusters | ⬜ Not yet implemented |
| **L5** | [Event-Centric Extraction](L05_event_centric_extraction.md) | Event detection, temporal ordering | Narrative chains | ⬜ Not yet implemented |
| **L6** | [Semantic Role Extraction](L06_semantic_role_extraction.md) | NER, OpenIE, SRL, dependency parsing | 5W1H structure | ⬜ Not yet implemented |
| **L7** | [Causal Narrative Extraction](L07_causal_narrative_extraction.md) | Rule-based + ML cause-effect detection | Causal mechanisms | ⬜ Not yet implemented |
| **L8** | [Narrative Networks & Graphs](L08_narrative_networks_graphs.md) | Knowledge graphs, temporal KGs | Relational networks | ⬜ Not yet implemented |
| **L9** | [RELATIO-Style Extraction](L09_relatio_style_extraction.md) | Entity-relation triple grouping | Aggregated narratives | ⬜ Not yet implemented |
| **L10** | [LLM-Based Extraction](L10_llm_based_extraction.md) | Prompt-based structured output | Deep semantic extraction | ✅ `llm_annotate.py` — Claude, GPT-4o, Gemini |
| **L11** | [Agentic Discovery Systems](L11_agentic_discovery_systems.md) | Multi-agent pipelines, continuous ingestion | Autonomous observatory | ⬜ Not yet implemented |

**Legend:** ✅ Implemented | 🔄 Planned/In Progress | ⬜ Not Yet Implemented

---

## Navigation Grid

### Foundational Methods (L0–L2)

| Method | Best For | Effort | Automation |
|--------|----------|--------|------------|
| [L0: Manual Coding](L00_manual_qualitative_coding.md) | Gold-standard data, deep interpretation | High (human hours) | None |
| [L1: Lexicon-Based](L01_lexicon_based_detection.md) | Simple narrative tracking, rapid prototyping | Low | Full |
| [L2: Statistical Text Mining](L02_statistical_text_mining.md) | Broad classification, index baselines | Medium | Full |

### Discovery Methods (L3–L4)

| Method | Best For | Effort | Automation |
|--------|----------|--------|------------|
| [L3: Topic Modeling](L03_topic_modeling.md) | Latent theme discovery, narrative emergence | Medium | Full |
| [L4: Embedding Discovery](L04_embedding_based_discovery.md) | Semantic narrative clusters, zero-shot discovery | Medium | Full |

### Structural Methods (L5–L7)

| Method | Best For | Effort | Automation |
|--------|----------|--------|------------|
| [L5: Event-Centric](L05_event_centric_extraction.md) | Narrative chains, temporal sequences | High | Partial |
| [L6: Semantic Role](L06_semantic_role_extraction.md) | Who-did-what extraction, actor analysis | High | Partial |
| [L7: Causal Extraction](L07_causal_narrative_extraction.md) | Cause-effect mechanisms, blame attribution | High | Partial |

### Relational Methods (L8–L9)

| Method | Best For | Effort | Automation |
|--------|----------|--------|------------|
| [L8: Narrative Graphs](L08_narrative_networks_graphs.md) | Actor networks, cross-document relations | High | Partial |
| [L9: RELATIO-Style](L09_relatio_style_extraction.md) | Triple extraction, narrative aggregation | High | Full |

### Cutting-Edge Methods (L10–L11)

| Method | Best For | Effort | Automation |
|--------|----------|--------|------------|
| [L10: LLM-Based](L10_llm_based_extraction.md) | Deep semantic extraction, gold labels | Medium (API cost) | Full |
| [L11: Agentic Systems](L11_agentic_discovery_systems.md) | Continuous monitoring, emergence detection | Very High | Autonomous |

---

## Quick Selection Guide

| If you want to... | Start at Level | Then Consider |
|-------------------|---------------|---------------|
| Count how often a narrative appears | **L1: Lexicon** | L2 for refinement |
| Discover what narratives exist in a corpus | **L4: Embedding** or **L3: Topic Model** | L10 for validation |
| Extract who is doing what | **L6: Semantic Role** | L9 for cross-document |
| Extract causal claims | **L7: Causal** | L10 for implicit causality |
| Build a narrative network | **L8: Narrative Graphs** | L7 for causal edges |
| Extract narratives at scale | **L10: LLM-Based** | Distil to L2 for production |
| Build continuous monitoring | **L11: Agentic** | L8 + L10 as foundations |
| Create gold-standard evaluation data | **L0: Manual Coding** | Validate L10 against it |

---

## BENI Implementation Map

### Currently Implemented

```
Potrika Corpus (664K articles)
    │
    ├── L10: LLM Annotation (llm_annotate.py)
    │   └── Claude, GPT-4o, Gemini ensemble
    │
    ├── L1: Lexicon Scoring (narrative.py)
    │   └── Force, target, topic Bangla lexicons
    │
    ├── L2: TF-IDF Classifier (train.py)
    │   └── 80k features, 91.7% accuracy
    │
    ├── L0: Manual Reference Set
    │   └── 300-article gold standard (in progress)
    │
    └── L10→L2: Calibrated Index (build_narrative_index.py)
        └── 79-month BENI Economic Index
```

### Planned

| Phase | Levels | Timeline | Components |
|-------|--------|----------|------------|
| **Phase 1** | L4 + L3 | Q3 2026 | Embedding clustering, BERTopic, dynamic topics |
| **Phase 2** | L10→L7 | Q4 2026 | Causal extraction in LLM prompt, schema update |
| **Phase 3** | L8 | Q1 2027 | Narrative graph construction, actor networks |
| **Phase 4** | L5 + L6 | Q1 2027 | Event detection, semantic role labeling |
| **Phase 5** | L9 | Q2 2027 | RELATIO-style cross-document aggregation |
| **Phase 6** | L11 | H2 2027 | Continuous ingestion, agentic discovery |

---

## Methodology Dependencies

```
L0 (Manual) ────────────────────────────── validates all levels
    │
L1 (Lexicon) ── seeds ──► L4 (Embedding)
    │
L2 (Statistical) ── baseline for all levels
    │
L3 (Topic) ── feeds ──► L8 (Narrative Graphs)
    │
L4 (Embedding) ── clusters ──► L8, L9
    │
L5 (Event) ── events ──► L8 (Graph nodes)
    │
L6 (Semantic Role) ── triples ──► L8, L9
    │
L7 (Causal) ── claims ──► L8 (Graph edges), L9
    │
L8 (Graphs) ── structure ──► L11 (Observatory)
    │
L9 (RELATIO) ── narratives ──► L11
    │
L10 (LLM) ── extraction engine ──► L5, L6, L7, L8, L9
    │
L11 (Agentic) ── orchestrates L4, L8, L10
```

---

## Key References

### Foundational Papers

| Paper | Level(s) | Contribution |
|-------|----------|--------------|
| Shiller (2017) — "Narrative Economics" | All | Foundation for quantitative narrative measurement |
| Roos & Reccius (2021) | All | Collective Economic Narrative (CEN) framework |
| Ash, Gauthier & Widmer (2023) — RELATIO | L9 | Entity-relation triple extraction for narratives |
| Andre et al. (2026) | All | Causal evidence that narratives shape expectations |

### Survey Papers

| Paper | Coverage | Key Contribution |
|-------|----------|-----------------|
| Norambuena et al. (2023) | L5–L11 | 3-resolution event narrative extraction survey |
| Santana et al. (2023) | All | End-to-end narrative extraction pipeline survey |

### BENI Papers

| Paper | Levels | Link |
|-------|--------|------|
| Nabil (2026) — BENI v1.0 Dataset | L10, L2 | `dataset/BENI/beni-v1/` |
| Nabil (2026) — BENI Global 10 | L10 | 10-language economic dataset |
| Nabil (2026) — LILA Lab | All | XENI pipeline framework |

---

## Relationship to Main Document

This index provides quick navigation to individual methodology pages. For the full integrated reference — including the complete hierarchy description, BENI 2.0 architecture proposal, research frontier analysis, and comprehensive references — see the main document:

➡️ **[Narrative Extraction Methodologies — Full Reference](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)**

---

**Next:** [L00: Manual Qualitative Coding](L00_manual_qualitative_coding.md) (start here for gold-standard data) | **Main:** [Full Reference](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
