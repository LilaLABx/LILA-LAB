> **Navigation:** [Documentation Portal](../../index.md) > [Research](../) > [Methodologies](./) > Level 5
>
> ---

# Level 5: Event-Centric Narrative Extraction

> **Hierarchy:** Narratives become sequences of events — what happened, when, and in what order.
> **BENI Status:** ⬜ Not Yet Implemented
> **Core Idea:** Identify discrete events from text, link them temporally and causally, and track how event chains form narrative structures.

---

## Table of Contents

1. [Overview](#overview)
2. [Core Components](#core-components)
3. [Event Detection Methods](#event-detection-methods)
4. [Event Linking](#event-linking)
5. [Temporal Ordering](#temporal-ordering)
6. [Worked Example](#worked-example)
7. [Strengths & Weaknesses](#strengths--weaknesses)
8. [When to Use Level 5](#when-to-use-level-5)
9. [BENI Context & Recommendations](#beni-context--recommendations)
10. [Implementation Guide](#implementation-guide)
11. [References](#references)

---

## Overview

Event-centric narrative extraction treats narratives as sequences of causally and temporally linked events. Rather than classifying whole documents as "about inflation," it identifies the specific events within each document — "inflation increased," "central bank raised rates," "GDP slowed" — and traces how they connect.

### Key Insight

**Narratives are event chains, not topic labels.** "The central bank raised rates because inflation increased" contains two events connected by causality. A document classifier sees "inflation and interest rates" (topic). An event extraction system sees "Event A → Event B" (narrative).

---

## Core Components

### Event Detection

Identify what happened from text:

```json
{
    "events": [
        {
            "type": "monetary_policy",
            "action": "rate_hike",
            "subject": "Bangladesh Bank",
            "object": "policy_rate",
            "magnitude": "50 basis points",
            "time": "2024-07-15"
        }
    ]
}
```

### Event Linking

Connect causally or temporally related events:

```json
{
    "event_links": [
        {
            "source": "Inflation increased to 9.5%",
            "target": "Central bank raised rates by 50bps",
            "relation": "causes",
            "confidence": 0.92
        }
    ]
}
```

### Temporal Ordering

Assign timestamps and sequence events:

```text
2024-Q1: Inflation accelerates (9.2% → 9.5%)
    ↓
2024-Q2: Central bank signals tightening
    ↓
2024-Q3: First rate hike (50bps)
    ↓
2024-Q4: Inflation moderates (9.5% → 9.1%)
```

---

## Event Detection Methods

### Pattern-Based Detection

Use linguistic patterns for event triggers:

```python
import re

EVENT_PATTERNS = {
    "rate_change": r"(rate|interest rate)\s+(hike|cut|raised|lowered|increased|decreased)",
    "inflation_change": r"inflation\s+(rose|fell|increased|decreased|accelerated|slowed)",
    "policy_action": r"(central bank|Bangladesh Bank|monetary policy)\s+(announced|decided|declared)",
}

def detect_events(text):
    events = []
    for event_type, pattern in EVENT_PATTERNS.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            events.append({
                "type": event_type,
                "trigger": match.group(),
                "span": match.span(),
                "sentence": extract_sentence(text, match.start()),
            })
    return events
```

### ML-Based Detection

Fine-tuned transformer for event extraction:

```python
from transformers import pipeline

# Zero-shot event detection
classifier = pipeline("text-classification",
    model="event-extraction-model")

# OR: fine-tune on economic event data
# See: MAUI, RAMS, ACE event schemas
```

### Event Types for Economics

| Event Type | Examples | Triggers |
|------------|----------|----------|
| **Monetary policy** | Rate hike, rate cut, QE | "raised rates", "tightened" |
| **Inflation** | Price increase, deflation | "inflation rose", "prices surged" |
| **Fiscal policy** | Budget, tax change, spending | "announced budget", "cut taxes" |
| **Trade** | Export growth, tariff | "exports increased", "trade deficit" |
| **Financial** | Market crash, bank failure | "stock market fell", "bank defaulted" |
| **Employment** | Job growth, unemployment | "employment rose", "jobless rate" |

---

## Event Linking

### Temporal Linking

```python
def link_events_temporally(events):
    """Link events that occur in the same document or nearby time."""
    links = []
    for i, e1 in enumerate(events):
        for j, e2 in enumerate(events[i+1:], i+1):
            if same_sentence(e1, e2):
                # Likely causally related
                links.append((e1, e2, "same_sentence"))
            elif e1["time"] <= e2["time"]:
                links.append((e1, e2, "temporal_order"))
    return links
```

### Causal Linking

```python
CAUSAL_MARKERS = [
    "because", "therefore", "caused by", "resulted in",
    "led to", "consequently", "due to", "as a result",
]

def link_events_causally(text, events):
    """Link events connected by causal markers."""
    links = []
    for match in re.finditer(r"(?i)" + "|".join(CAUSAL_MARKERS), text):
        # Find events before and after the causal marker
        before = find_nearest_event(events, match.start(), direction="before")
        after = find_nearest_event(events, match.end(), direction="after")
        if before and after:
            links.append({
                "source": before,
                "target": after,
                "relation": "causes",
                "marker": match.group(),
            })
    return links
```

---

## Temporal Ordering

### Time Expression Extraction

```python
import dateparser

def extract_time_expressions(text):
    """Extract and normalize temporal expressions."""
    patterns = [
        r"in\s+(January|February|...|December)\s+\d{4}",
        r"Q[1-4]\s+\d{4}",
        r"\d{4}-\d{2}-\d{2}",
        r"last\s+(month|year|quarter)",
        r"next\s+(month|year|quarter)",
    ]
    times = []
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            parsed = dateparser.parse(match.group())
            if parsed:
                times.append({
                    "expression": match.group(),
                    "parsed": parsed,
                    "span": match.span(),
                })
    return times
```

### Narrative Chain Construction

```python
class NarrativeChain:
    def __init__(self):
        self.events = []
        self.links = []

    def add_event(self, event):
        self.events.append(event)

    def add_link(self, source_idx, target_idx, relation):
        self.links.append((source_idx, target_idx, relation))

    def to_sequence(self):
        """Sort events temporally and return narrative chain."""
        sorted_events = sorted(self.events, key=lambda e: e.get("time", ""))
        return [
            {
                "step": i,
                "event": e["action"],
                "time": e.get("time", "unknown"),
                "antecedent": self.events[l[0]]["action"]
                for l in self.links if l[1] == i
            }
            for i, e in enumerate(sorted_events)
        ]
```

---

## Worked Example

### Input: News Article Snippet

> "Inflation accelerated to 9.5% in June 2024, driven by rising food and energy prices. The Bangladesh Bank responded in July by raising the policy rate by 50 basis points. Governor Abdur Rouf Talukder stated that further tightening may be needed if inflation does not moderate. However, industry groups warned that higher rates would hurt investment and employment."

### Event Extraction Output

```json
{
    "document_events": [
        {
            "id": 1,
            "action": "inflation_accelerated",
            "subject": "inflation",
            "object": "9.5%",
            "time": "2024-06",
            "trigger": "accelerated",
            "sentence": 0
        },
        {
            "id": 2,
            "action": "prices_rose",
            "subject": "food and energy prices",
            "relation": "cause_of_1",
            "trigger": "driven by",
            "sentence": 0
        },
        {
            "id": 3,
            "action": "rate_hike",
            "subject": "Bangladesh Bank",
            "object": "50 basis points",
            "time": "2024-07",
            "trigger": "raising",
            "sentence": 1
        },
        {
            "id": 4,
            "action": "tightening_signaled",
            "subject": "Governor",
            "condition": "if inflation does not moderate",
            "sentence": 2
        },
        {
            "id": 5,
            "action": "investment_harm_predicted",
            "subject": "industry groups",
            "object": "investment and employment",
            "sentence": 3
        }
    ]
}
```

### Narrative Chain

```text
2024-06: Food & energy prices rise
    ↓ [causes]
2024-06: Inflation accelerates to 9.5%
    ↓ [causes]
2024-07: Bangladesh Bank raises rate 50bps
    ├── → [if inflation persists] Further tightening
    └── → [warned by industry] Hurts investment & employment
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Description |
|----------|-------------|
| **Genuine narrative structure** | Events + links > topic labels |
| **Temporal tracking** | When did each narrative step occur? |
| **Causal transparency** | Which events cause which outcomes? |
| **Granularity** | Sentence-level, not document-level |
| **Cross-document synthesis** | Same event chain across articles |

### Weaknesses

| Weakness | Description | Mitigation |
|----------|-------------|------------|
| **Complex implementation** | Multiple sub-tasks (detection, linking, ordering) | Start with LLM-based (L10) |
| **Event schema design** | What counts as an event? | Use economic event taxonomy |
| **Coreference resolution** | "The Bank" = "Bangladesh Bank" | Add coref pre-processing |
| **Temporal ambiguity** | "Last month" relative to what? | Normalize to absolute dates |

---

## When to Use Level 5

| Scenario | Recommended | Alternative |
|----------|-------------|-------------|
| Tracking causal narrative chains | ✅ **Level 5** | — |
| Narrative lead analysis (events before stats) | ✅ **Level 5** | — |
| Section migration analysis | ✅ **Level 5** | — |
| Document-level narrative classification | ❌ Overkill | L2 or L10 |
| Exploring new domain | ❌ Too complex initially | L3 or L4 first |

---

## BENI Context & Recommendations

**Current status: ⬜ Not Yet Implemented**

The BENI pipeline currently operates at the document level — classifying whole articles as "economic" or "not." There is no event extraction, temporal linking, or narrative chain construction.

### How BENI Could Use Event Extraction

1. **Narrative lead analysis:**
   - Extract events from news articles
   - Compare event dates to official statistics dates
   - Quantify how far in advance news narratives anticipate official data

2. **Section migration tracking:**
   - Extract the same event (e.g., "inflation reached 9.5%") across sections
   - Measure time lag between Economy section → National → Politics → Editorial
   - This directly enables the **Sectional Migration Hypothesis**

3. **Narrative acceleration:**
   - During crisis periods, event chains are shorter (events happen faster)
   - Quantify: average time between linked events during crisis vs. normal periods

### Recommended Approach

Start with **LLM-based event extraction** rather than building a custom event detection system:

```python
EVENT_EXTRACTION_PROMPT = """Extract ALL economic events from the following Bangla news article.

For each event, return:
- action: what happened
- subject: who/what performed the action
- object: what/who was affected
- time: when it happened (exact date or relative)
- trigger: the word/phrase that signals this event

Also return temporal and causal links between events.

Format as JSON array."""

# Use existing BENI LLM infrastructure
response = call_anthropic(EVENT_EXTRACTION_PROMPT, article_text)
events = json.loads(response)
```

---

## Implementation Guide

### Lightweight Event Extraction

```python
import spacy
from collections import defaultdict

def extract_event_triples(text, nlp_model):
    """
    Extract subject-verb-object triples as candidate events.
    Uses spaCy dependency parsing.
    """
    doc = nlp_model(text)
    events = []

    for sent in doc.sents:
        for token in sent:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                subject = None
                objects = []

                for child in token.children:
                    if child.dep_ in ("nsubj", "nsubjpass"):
                        subject = child.text
                    elif child.dep_ in ("dobj", "pobj", "attr"):
                        objects.append(child.text)

                if subject:
                    events.append({
                        "subject": subject,
                        "action": token.lemma_,
                        "object": " ".join(objects) if objects else None,
                        "sentence": sent.text,
                    })

    return events

# For Bangla: use a multilingual spaCy model
# nlp = spacy.load("xx_ent_wiki_sm")  # Multi-language model
```

### Full Pipeline

```python
class EventCentricNarrativeExtractor:
    def __init__(self, llm_client, nlp_model=None):
        self.llm = llm_client
        self.nlp = nlp_model

    def extract(self, text):
        # Method 1: LLM-based (recommended)
        llm_events = self._extract_via_llm(text)

        # Method 2: Dependency-based (if nlp model available)
        if self.nlp:
            dep_events = extract_event_triples(text, self.nlp)
            # Merge: LLM provides semantics, dependency provides coverage
            return self._merge_events(llm_events, dep_events)

        return llm_events

    def build_narrative_chain(self, events):
        """Link events into a narrative chain."""
        chain = NarrativeChain()
        for event in events:
            chain.add_event(event)

        # Link temporally
        for i, e1 in enumerate(events):
            for j, e2 in enumerate(events[i+1:], i+1):
                if self._is_causal(e1, e2):
                    chain.add_link(i, j, "causes")

        return chain.to_sequence()
```

---

## References

### Core Reading

- Norambuena, B. K., Mitra, T., & North, C. (2023). "A Survey on Event-based News Narrative Extraction." *ACM Computing Surveys*, 55(14s): 1–39. DOI: `10.1145/3584741`.
- Chambers, N. & Jurafsky, D. (2008). "Unsupervised Learning of Narrative Event Chains." *ACL*.
- Mostafazadeh, N. et al. (2016). "A Corpus and Cloze Evaluation for Deeper Understanding of Commonsense Stories." *NAACL*.

### Tools

- **spaCy**: Dependency parsing for SVO extraction
- **AllenNLP**: Semantic Role Labeling
- **FRED**: Frame-based event extraction
- **TimeML**: Temporal annotation standard

### See Also

- Level 6: [Semantic Role Extraction](L06_semantic_role_extraction.md) — Who did what to whom
- Level 7: [Causal Narrative Extraction](L07_causal_narrative_extraction.md) — Cause-effect from events

---

**Up:** [Methodologies Index](INDEX.md) | **Main:** [Narrative Extraction Methodologies](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
