> **Navigation:** [Documentation Portal](../../index.md) > [Research](../) > [Methodologies](./) > Level 6
>
> ---

# Level 6: Semantic Role and Narrative Structure Extraction

> **Hierarchy:** Extracts the 5W1H framework — Who did what, to whom, why, and when?
> **BENI Status:** ⬜ Not Yet Implemented
> **Core Idea:** Decompose sentences into structured roles (actor, action, recipient, purpose) to extract narrative components.

---

## Table of Contents

1. [Overview](#overview)
2. [The 5W1H Framework](#the-5w1h-framework)
3. [Key Techniques](#key-techniques)
4. [Worked Example](#worked-example)
5. [Strengths & Weaknesses](#strengths--weaknesses)
6. [When to Use Level 6](#when-to-use-level-6)
7. [BENI Context & Recommendations](#beni-context--recommendations)
8. [Implementation Guide](#implementation-guide)
9. [Integration with LLM Pipeline](#integration-with-llm-pipeline)
10. [References](#references)

---

## Overview

Semantic role labeling (SRL) identifies the predicate-argument structure of sentences — essentially answering: **who did what to whom, when, where, and why?** For narrative extraction, this transforms unstructured text into structured narrative components.

### Key Insight

**Narratives are about actors performing actions for reasons.** Level 6 makes this structure explicit by extracting:

- **Who** is acting? (Actor identification)
- **What** are they doing? (Action extraction)
- **To/for whom?** (Recipient/beneficiary)
- **Why?** (Purpose/cause)
- **When?** (Temporal context)
- **How?** (Manner/instrument)

---

## The 5W1H Framework

### Narrative Roles

| Role | Question | Example | NLP Task |
|------|----------|---------|----------|
| **Actor** | Who? | The central bank | Named Entity Recognition |
| **Action** | Did what? | Raised interest rates | Relation Extraction |
| **Recipient** | To whom? | Commercial banks | Dependency Parsing |
| **Purpose** | Why? | To combat inflation | Semantic Role Labeling |
| **Temporal** | When? | In July 2024 | Time Expression Extraction |
| **Manner** | How? | By 50 basis points | Adverbial extraction |

### Narrative Schema

```
[Actor] → [Action] → [Recipient] → [Purpose] → [Outcome]

Government → Increases → Spending → Stimulate economy → Inflation
Central Bank → Raises → Rates → Combat inflation → Slower growth
Exporters → Benefit from → Taka depreciation → Boost competitiveness → Higher exports
```

---

## Key Techniques

### Named Entity Recognition (NER)

Identify actors, organizations, locations, and other entities:

```python
import spacy

nlp = spacy.load("xx_ent_wiki_sm")  # Multi-language

def extract_actors(text):
    doc = nlp(text)
    actors = []
    for ent in doc.ents:
        if ent.label_ in ("ORG", "PERSON", "GPE"):
            actors.append({
                "text": ent.text,
                "type": ent.label_,
                "role": infer_economic_role(ent.text),
            })
    return actors

def infer_economic_role(entity_text):
    """Map named entities to economic actor types."""
    economic_roles = {
        "Bangladesh Bank": "central_bank",
        "সরকার": "government",  # government
        "আইএমএফ": "international_org",  # IMF
    }
    return economic_roles.get(entity_text, "other")
```

### Relation Extraction

Extract relationships between entities:

```python
# OpenIE-style extraction
# (Actor) --[Action]→ (Recipient)

def extract_relations(doc):
    relations = []
    for token in doc:
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            subject = [w for w in token.children if w.dep_ == "nsubj"]
            objects = [w for w in token.children if w.dep_ == "dobj"]
            if subject and objects:
                relations.append({
                    "subject": subject[0].text,
                    "verb": token.lemma_,
                    "object": objects[0].text,
                    "sentence": token.sent.text,
                })
    return relations
```

### Semantic Role Labeling (SRL)

Full predicate-argument structure:

```python
# Using AllenNLP or similar
from allennlp.predictors import Predictor

predictor = Predictor.from_path(
    "https://storage.googleapis.com/allennlp-public-models/bert-base-srl-2020.03.24.tar.gz"
)

def extract_semantic_roles(sentence):
    result = predictor.predict(sentence=sentence)
    roles = []
    for verb_info in result["verbs"]:
        tags = verb_info["tags"]
        roles.append({
            "verb": verb_info["verb"],
            "arguments": parse_srl_tags(tags, result["words"]),
        })
    return roles

# Parse BIO tags into argument structure
def parse_srl_tags(tags, words):
    args = {}
    current_arg = None
    for word, tag in zip(words, tags):
        if tag.startswith("B-"):
            current_arg = tag[2:]
            args[current_arg] = word
        elif tag.startswith("I-") and current_arg:
            args[current_arg] += " " + word
    return args
```

### OpenIE Extraction

Open-domain information extraction:

```python
from openie import StanfordOpenIE

with StanfordOpenIE() as client:
    triples = client.annotate(sentence)
    for triple in triples:
        print(f"({triple['subject']}, {triple['relation']}, {triple['object']})")
```

### Dependency Parsing

Grammatical relation extraction for narrative structure:

```python
def extract_narrative_structure(doc):
    """Extract narrative structure using dependency parsing."""
    structures = []
    for sent in doc.sents:
        structure = {"sentence": sent.text, "roles": {}}

        for token in sent:
            # Identify the main verb (narrative action)
            if token.dep_ == "ROOT":
                structure["action"] = token.lemma_

                # Find subject (actor)
                for child in token.children:
                    if child.dep_ == "nsubj":
                        structure["actor"] = child.text
                    elif child.dep_ == "dobj":
                        structure["recipient"] = child.text
                    elif child.dep_ == "advmod" and child.text in ("because", "to", "for"):
                        # Purpose clause
                        for grandchild in child.subtree:
                            structure["purpose"] = " ".join(
                                [t.text for t in child.subtree]
                            )

        structures.append(structure)
    return structures
```

---

## Worked Example

### Input Sentence

> "The central bank raised interest rates to combat inflation."

### Full SRL Output

```json
{
    "verb": "raised",
    "arguments": {
        "ARG0": "The central bank",     // Agent/Actor
        "ARG1": "interest rates",       // Theme/Patient
        "ARG2": "to combat inflation",  // Purpose/Goal
        "V": "raised"                   // Verb
    }
}
```

### Narrative Schema Output

```json
{
    "narrative": {
        "actor": {
            "text": "The central bank",
            "type": "central_bank",
            "normalized": "Bangladesh Bank",
            "role": "policy_maker"
        },
        "action": {
            "verb": "raised",
            "type": "monetary_policy_tightening",
            "magnitude": null,
            "instrument": "interest rates"
        },
        "purpose": {
            "text": "to combat inflation",
            "type": "causal_purpose",
            "target": "inflation",
            "intended_outcome": "reduce inflation"
        },
        "temporal": {
            "text": null,
            "relative": false
        }
    }
}
```

### Multiple Role Extraction Across Document

| Sentence | Actor | Action | Recipient | Purpose |
|----------|-------|--------|-----------|---------|
| S1: "Government increased spending" | Government | Increased | Spending | — |
| S2: "This drove up inflation" | Spending (implied) | Drove up | Inflation | — |
| S3: "Central bank raised rates to slow economy" | Central Bank | Raised | Rates | To slow economy |
| S4: "Households struggled with higher prices" | Households | Struggled | — | With higher prices |

**Aggregated narrative:**
```
Government → Increased Spending → Drove Inflation → Central Bank Raised Rates → Households Struggled
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Description |
|----------|-------------|
| **Structured output** | Explicit actor-action-purpose triples |
| **Interpretable** | Each extracted role is human-readable |
| **Causal transparency** | Purpose field captures "why" |
| **Cross-document synthesis** | Same actor across documents |
| **Schema-driven** | Compatible with knowledge graphs (L8) |

### Weaknesses

| Weakness | Description | Mitigation |
|----------|-------------|------------|
| **Language-dependent** | SRL models primarily available for English | Use multilingual models or LLM (L10) |
| **Sentence-level** | Cannot handle cross-sentence roles | Coreference resolution |
| **Error propagation** | Errors in NER → errors in roles | Ensemble methods |
| **Implicit roles** | Not all roles are explicitly stated | LLM for implicit inference |
| **Computational cost** | Full SRL is expensive | Use LLM as SRL proxy |

---

## When to Use Level 6

| Scenario | Recommended | Alternative |
|----------|-------------|-------------|
| Building narrative knowledge graphs | ✅ **Level 6** (required) | — |
| Extracting who-did-what | ✅ **Level 6** | — |
| Actor-centric narrative analysis | ✅ **Level 6** | — |
| Simple narrative classification | ❌ Overkill | L2 or L10 |
| Very large corpus | ❌ Expensive per-document | L1 or L2 approximation |

---

## BENI Context & Recommendations

**Current status: ⬜ Not Yet Implemented**

The BENI pipeline's closest approach to Level 6 is the LLM annotation prompt in `llm_annotate.py`, which asks for `valuation_target` (who is responsible) and `narrative_force` (the nature of the action). However, this is implicit SRL — the LLM performs role assignment internally, but no explicit 5W1H structure is extracted.

### How the LLM Prompt Acts as Implicit SRL

```json
// Current BENI LLM output (implicit roles)
{
    "economic_topic": "inflation",
    "narrative_force": "blame",
    "valuation_target": "government",
    "sentiment": "negative"
}
```

### Proposed Explicit SRL Extension

```json
// Enhanced BENI LLM output (explicit roles)
{
    "narratives": [
        {
            "actor": {
                "text": "সরকার",
                "normalized": "government",
                "type": "government"
            },
            "action": {
                "text": "ব্যয় বৃদ্ধি করেছে",
                "normalized": "increased spending",
                "type": "fiscal_expansion"
            },
            "recipient": null,
            "purpose": null,
            "effect": {
                "text": "মূল্যস্ফীতি বেড়েছে",
                "normalized": "inflation increased",
                "type": "price_level"
            },
            "causal_marker": "কারণ",
            "temporal": "2024-06"
        }
    ]
}
```

### Implementation via Existing LLM Infrastructure

The BENI pipeline already has all the infrastructure needed:

```python
# Add to existing llm_annotate.py prompt
SRL_PROMPT_EXTENSION = """
Extract the narrative structure for each economic claim in the article.
Return an array of narrative objects, each containing:
- actor: who or what is acting
- action: what they did (verb phrase)
- recipient: who/what was affected (if any)
- purpose: why they did it (if stated)
- effect: what resulted (if stated)
- causal_marker: "because", "therefore", "led to", or null
- temporal: when this happened
"""
```

---

## Implementation Guide

### Lightweight SRL for Bangla

```python
from transformers import pipeline

# Use multilingual NER + dependency parsing
nlp = spacy.load("xx_ent_wiki_sm")

class NarrativeRoleExtractor:
    def __init__(self, actor_lexicon=None):
        self.nlp = spacy.load("xx_ent_wiki_sm")
        self.actor_lexicon = actor_lexicon or {
            "সরকার": "government",
            "বাংলাদেশ ব্যাংক": "central_bank",
            "আইএমএফ": "international_org",
            # ... extend from narrative.py valuation_target lexicon
        }

    def extract_roles(self, text):
        doc = self.nlp(text)
        narratives = []

        for sent in doc.sents:
            roles = self._extract_sentence_roles(sent)
            if roles:
                narratives.append(roles)

        return narratives

    def _extract_sentence_roles(self, sent):
        roles = {"sentence": sent.text, "actor": None, "action": None}

        # Find main verb
        for token in sent:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                roles["action"] = token.lemma_

                # Find subject
                for child in token.children:
                    if child.dep_ == "nsubj":
                        text = child.text
                        roles["actor"] = {
                            "text": text,
                            "normalized": self.actor_lexicon.get(text, text),
                        }
        return roles if roles["actor"] else None
```

### LLM-Based SRL (Recommended for BENI)

```python
class LLMSemanticRoleExtractor:
    """Uses the existing BENI LLM infrastructure for SRL."""

    def __init__(self, llm_client):
        self.llm = llm_client
        self.srl_prompt = """
        Extract the semantic roles from the following Bangla economic text.

        For each economic action described, identify:
        1. ACTOR: Who performed the action?
        2. ACTION: What did they do? (verb phrase)
        3. RECIPIENT: Who or what was affected?
        4. PURPOSE/CAUSE: Why was this done?
        5. OUTCOME: What resulted?
        6. TEMPORAL: When did this happen?

        Return as JSON array.

        Text: {text}
        """

    def extract(self, text):
        prompt = self.srl_prompt.format(text=text[:4000])
        response = self.llm(prompt)
        return json.loads(response)
```

---

## Integration with LLM Pipeline

The most practical path for BENI is to extend the existing LLM prompt rather than building a separate SRL system:

```python
# Current prompt (L10)
BASE_PROMPT = """Annotate for: economic_relevance, confidence, difficulty,
economic_topic, sentiment, narrative_force, valuation_target, notes"""

# Extended prompt (L10 + L6)
EXTENDED_PROMPT = """{BASE_PROMPT}

Additionally, extract the narrative structure for each claim:
- For each actor-action pair in the article
- Return as structured JSON with actor, action, recipient, purpose, effect
- Include the normalization of actors to standard types
"""
```

### Benefits of Integration

1. **No new infrastructure** — Uses existing LLM clients in `shared/llm/clients.py`
2. **Consistent schema** — SRL fields align with existing `valuation_target` field
3. **Validation against L0** — SRL extraction can be validated on the 300-article reference set
4. **Gradual rollout** — Add SRL fields as optional; extract when needed

---

## References

### Core Reading

- Santana, B. et al. (2023). "A survey on narrative extraction from textual data." *Artificial Intelligence Review*, 56(8): 8393–8435.
- Palmer, M., Gildea, D., & Kingsbury, P. (2005). "The Proposition Bank: A Corpus Annotated with Semantic Roles." *Computational Linguistics*, 31(1): 71–106.
- Angeli, G., Premkumar, M. J. J., & Manning, C. D. (2015). "Leveraging Linguistic Structure For Open Domain Information Extraction." *ACL*.

### Tools

- **AllenNLP**: State-of-the-art SRL for English
- **spaCy**: Dependency parsing + NER (multilingual)
- **Stanford NLP**: OpenIE for triple extraction
- **HuggingFace Transformers**: Zero-shot NER and relation extraction

### See Also

- Level 7: [Causal Narrative Extraction](L07_causal_narrative_extraction.md) — Next step from roles
- Level 5: [Event-Centric Extraction](L05_event_centric_extraction.md) — Events from roles
- Level 8: [Narrative Graphs](L08_narrative_networks_graphs.md) — Graph from roles
- Level 10: [LLM-Based Extraction](L10_llm_based_extraction.md) — LLM as SRL proxy

---

**Up:** [Methodologies Index](INDEX.md) | **Main:** [Narrative Extraction Methodologies](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
