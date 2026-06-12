# Level 7: Causal Narrative Extraction

> **Hierarchy:** The core of what makes a narrative a narrative — cause-effect relationships.
> **BENI Status:** ⬜ Not Yet Implemented
> **Core Idea:** Extract explicit and implicit causal claims from text — who caused what and why.

---

## Table of Contents

1. [Overview](#overview)
2. [Why Causality Matters for Economics](#why-causality-matters-for-economics)
3. [Methods Overview](#methods-overview)
4. [Rule-Based Approaches](#rule-based-approaches)
5. [ML-Based Approaches](#ml-based-approaches)
6. [Causal Extraction Systems](#causal-extraction-systems)
7. [Worked Example](#worked-example)
8. [Strengths & Weaknesses](#strengths--weaknesses)
9. [When to Use Level 7](#when-to-use-level-7)
10. [Integration with LLM Pipeline](#integration-with-llm-pipeline)
11. [BENI Implementation Guide](#beni-implementation-guide)
12. [References](#references)

---

## Overview

Causal narrative extraction identifies cause-effect relationships from text — the central component that distinguishes a narrative from a topic. When a news article says "inflation rose because of government spending," it proposes a causal model. Extracting these causal claims reveals the **economic belief system** embedded in text.

### Formal Definition

```
Narrative = Cause → Mechanism → Outcome
```

Rather than merely:

```
Narrative = Topic
```

### Economic Causal Claims

| Claim Type | Example | Causal Structure |
|------------|---------|-----------------|
| Cost-push | "Inflation rose because of supply chain disruptions" | Supply shock → Price increase |
| Demand-pull | "Government spending caused demand-pull inflation" | Fiscal expansion → Demand → Inflation |
| Monetary | "Easy monetary policy is fueling inflation" | Money supply → Prices |
| External | "Global oil prices drove domestic inflation" | Import prices → Domestic prices |
| Structural | "Weak competition is causing price increases" | Market structure → Pricing power |

---

## Why Causality Matters for Economics

Economics is fundamentally about causality. Newspaper articles about the economy are implicitly proposing causal models:

> *"Inflation is rising because government spending increased."*

This is not just a topic (inflation) or a sentiment (negative). It is a **causal claim** — a testable hypothesis about how the economy works. Extracting these claims from news text reveals:

1. **Popular causal beliefs** — What causal models are circulating in public discourse
2. **Causal contestation** — Competing explanations for the same phenomenon
3. **Narrative-driven expectations** — Causal beliefs shape inflation expectations (Andre et al., 2026)

### BENI Relevance

The BENI index currently tracks *whether* an article is about the economy. Causal extraction would track *what causal mechanism the article proposes* — a much richer signal for understanding economic belief formation.

---

## Methods Overview

| Approach | Example | Precision | Recall | When to Use |
|----------|---------|-----------|--------|-------------|
| **Rule-based** | "because", "therefore" patterns | High | Low | Quick baseline |
| **ML classifiers** | BERT fine-tuned on causal sentence detection | High | Medium | General causal extraction |
| **Sequence labeling** | Mark cause-effect spans | Medium | Medium | Span-level extraction |
| **LLM prompting** | "Extract cause-effect pairs" | High | High | Few-shot, zero-shot |
| **Causal graph extraction** | Full causal network | High | Low | Advanced research |

---

## Rule-Based Approaches

### Causal Connective Patterns

```python
import re

CAUSAL_PATTERNS = [
    # Explicit causal connectives
    (r"because\s+(.+?)(?:,|\.|;|$)", "cause→effect"),
    (r"(.+?)\s+because\s+(.+)", "effect→cause"),
    (r"\btherefore\b", "marker"),
    (r"as a result\s+(?:of\s+)?(.+)", "cause→effect"),
    (r"(?:led to|resulted in|caused|triggered)\s+(.+)", "cause→effect"),
    (r"(?:due to|owing to|attributed to)\s+(.+)", "effect→cause"),
    (r"(?:consequently|hence|thus)\s+", "marker"),
    # Economic-specific patterns
    (r"(.+?)\s+(?:push|drive|fuel|spark)\s+(?:up|down)?.+", "cause→effect"),
]

def extract_causal_rules(text):
    """Extract cause-effect pairs using rule-based patterns."""
    causes = []
    for pattern, direction in CAUSAL_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            if direction == "cause→effect" and match.groups():
                causes.append({
                    "cause": match.group(1),
                    "effect": None,  # implied by context
                    "marker": match.group(0)[:20],
                    "confidence": 0.6,
                })
            elif direction == "effect→cause" and match.groups():
                causes.append({
                    "cause": None,
                    "effect": match.group(1),
                    "marker": match.group(0)[:20],
                    "confidence": 0.6,
                })
    return causes
```

### Bangla Causal Patterns

```python
# Bangla causal connectives for BENI
BANGLA_CAUSAL_PATTERNS = [
    r"কারণ",       # because
    r"যার ফলে",    # as a result of which
    r"ফলে",        # as a result
    r"জন্য",       # due to / for
    r"হেতু",       # owing to
    r"দরুন",       # because of
    r"মূলত",       # mainly due to
    r"থেকে",       # from (causal)
]
```

---

## ML-Based Approaches

### Causal Sentence Classification

```python
from transformers import pipeline

# Fine-tuned model for causal claim detection
# (From Norouzi et al., 2025: F1 = 0.89 on social science text)
causal_detector = pipeline(
    "text-classification",
    model="causal-claim-detector",
)

def is_causal_sentence(sentence):
    result = causal_detector(sentence)
    return result[0]["label"] == "CAUSAL"
```

### Span-Level Causal Extraction

```python
from transformers import AutoTokenizer, AutoModelForTokenClassification

# Sequence labeling: B-CAUSE, I-CAUSE, B-EFFECT, I-EFFECT, O
model = AutoModelForTokenClassification.from_pretrained("causal-span-extractor")
tokenizer = AutoTokenizer.from_pretrained("causal-span-extractor")

def extract_cause_effect_spans(sentence):
    inputs = tokenizer(sentence, return_tensors="pt")
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(-1)
    # Decode: extract B-CAUSE...I-CAUSE and B-EFFECT...I-EFFECT spans
    return {"cause": "<extracted span>", "effect": "<extracted span>"}
```

---

## Causal Extraction Systems

### Lightweight Causal Graph Builder

```python
class CausalGraph:
    """Build and query a causal graph from text."""

    def __init__(self):
        self.nodes = {}      # concept → node_id
        self.edges = []      # (source, target, label, confidence)

    def add_causal_claim(self, cause, effect, confidence=1.0, marker=None):
        cause_id = self._get_or_create(cause)
        effect_id = self._get_or_create(effect)
        self.edges.append({
            "source": cause_id,
            "target": effect_id,
            "type": "causes",
            "confidence": confidence,
            "marker": marker,
        })

    def _get_or_create(self, concept):
        if concept not in self.nodes:
            self.nodes[concept] = len(self.nodes)
        return self.nodes[concept]

    def query(self, concept, direction="downstream"):
        """Get all causes or effects of a concept."""
        if direction == "downstream":
            # What does X cause?
            return [
                e for e in self.edges
                if e["source"] == self.nodes.get(concept)
            ]
        else:
            # What causes X?
            return [
                e for e in self.edges
                if e["target"] == self.nodes.get(concept)
            ]

    def to_index(self, time_period):
        """Convert causal claims to a narrative index.
        
        Measure: What proportion of causal claims involve concept X
        as cause vs. effect?
        """
        total = len(self.edges)
        if total == 0:
            return {}
        
        cause_counts = {}
        effect_counts = {}
        for edge in self.edges:
            cause = list(self.nodes.keys())[list(self.nodes.values()).index(edge["source"])]
            effect = list(self.nodes.keys())[list(self.nodes.values()).index(edge["target"])]
            cause_counts[cause] = cause_counts.get(cause, 0) + 1
            effect_counts[effect] = effect_counts.get(effect, 0) + 1
        
        return {
            "period": time_period,
            "total_claims": total,
            "cause_prevalence": {k: v/total for k, v in cause_counts.items()},
            "effect_prevalence": {k: v/total for k, v in effect_counts.items()},
        }
```

---

## Worked Example

### Input Article

> *"Inflation has surged to 9.5%, driven primarily by rising food and energy prices. The Russia-Ukraine war disrupted global supply chains, which pushed up commodity prices. Additionally, expansionary fiscal policy during the pandemic increased money supply. The Bangladesh Bank responded by raising interest rates, but economists warn that further monetary tightening could slow economic growth."*

### Causal Extraction Output

```json
{
    "causal_claims": [
        {
            "cause": "rising food and energy prices",
            "effect": "inflation surged to 9.5%",
            "marker": "driven by",
            "confidence": 0.9,
            "type": "cost_push"
        },
        {
            "cause": "Russia-Ukraine war disrupted global supply chains",
            "effect": "pushed up commodity prices",
            "marker": "disrupted...which pushed up",
            "confidence": 0.85,
            "type": "external_shock"
        },
        {
            "cause": "expansionary fiscal policy during pandemic",
            "effect": "increased money supply",
            "marker": "increased",
            "confidence": 0.7,
            "type": "demand_pull"
        },
        {
            "cause": "Bangladesh Bank raising interest rates",
            "effect": null,
            "marker": "responded by",
            "confidence": 0.8,
            "type": "policy_response",
            "intended_effect": "reduce inflation"
        },
        {
            "cause": "further monetary tightening",
            "effect": "slow economic growth",
            "marker": "could",
            "confidence": 0.5,
            "type": "predicted_consequence",
            "conditional": true
        }
    ]
}
```

### Causal Graph

```text
Russia-Ukraine War ──→ Supply Chain Disruption ──→ Commodity Prices ↑
                                                         ↓
Pandemic Fiscal Policy ──→ Money Supply ↑ ──→ Inflation 9.5%
                                                     ↓
                                          Bangladesh Bank → Rate Hike
                                                     ↓
                                          (Predicted) Slower Growth
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Description |
|----------|-------------|
| **Extracts causal structure** | The core of what makes a narrative a narrative |
| **Theory-grounded** | Causal claims are testable hypotheses |
| **Economic relevance** | Reveals the causal models driving discourse |
| **Graph-ready** | Causes and effects naturally form graphs (L8) |
| **Novel signal** | Not captured by sentiment or topic models |

### Weaknesses

| Weakness | Description | Mitigation |
|----------|-------------|------------|
| **Implicit causality** | Many causal claims lack explicit markers | Use LLM for implicit inference |
| **Counterfactuals** | "What-if" causal statements | Specialized extraction patterns |
| **Confidence calibration** | How sure are we this is causal? | LLM confidence scores |
| **Domain adaptation** | Causal patterns differ by domain | Fine-tune on economic text |
| **Evaluation** | Gold-standard causal annotations are rare | Create small evaluation set manually |

---

## When to Use Level 7

| Scenario | Recommended | Alternative |
|----------|-------------|-------------|
| Understanding why narratives exist | ✅ **Level 7** | — |
| Building causal narrative graphs | ✅ **Level 7** (required) | — |
| Analyzing blame attribution | ✅ **Level 7** | — |
| Simple narrative prevalence tracking | ❌ Overkill | L1 or L2 |
| Very noisy text | ❌ Causal patterns unreliable | L4 clustering first |

---

## Integration with LLM Pipeline

### Extended BENI Annotation Prompt

The most cost-effective approach: extend the existing LLM prompt to include causal extraction:

```python
CAUSAL_PROMPT = """
Extract ALL causal economic claims from this Bangla news article.

For each causal claim, identify:
1. CAUSE: What caused something to happen?
2. EFFECT: What happened?
3. CAUSAL_MARKER: The word or phrase indicating causality
4. TYPE: One of: cost_push, demand_pull, monetary, external_shock, policy_response, structural, other
5. CONDITIONAL: Is this a conditional claim ("if X then Y")?
6. CONFIDENCE: How clearly is this causal relationship stated? (0.0-1.0)
7. STANCE: Does the article portray this causal relationship as positive, negative, or neutral?

Return as JSON array of causal claims.
Empty array if no causal claims found.

Article text: {text}
"""
```

### Dual Role of LLM

LLMs serve two roles for causal extraction:

1. **Extract explicit causality** — Causal markers present in text
2. **Infer implicit causality** — Causal relationships implied but not marked

```python
CAUSAL_TYPES = {
    "explicit": "Use explicit markers: because, therefore, caused by, led to",
    "implicit": "Infer causality from context even without explicit markers",
    "conditional": "Extract if-then causal relationships",
}
```

---

## BENI Implementation Guide

### Phase 1: Rule-Based Baseline (1 week)

```python
def extract_bangla_causal_claims(text):
    """Bangla causal extraction using BENI's existing infrastructure."""
    claims = []

    # 1. Check for causal markers in Bangla
    for pattern in BANGLA_CAUSAL_PATTERNS:
        for match in re.finditer(pattern, text):
            # Extract surrounding context
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 100)
            context = text[start:end]

            claims.append({
                "marker": match.group(),
                "context": context,
                "confidence": 0.5,
                "method": "rule_based",
            })

    # 2. Cross-reference with valuation_target (blame attribution)
    narrative = narrative_profile(text)
    if narrative["valuation_target"]["label"] != "unnamed_system":
        claims.append({
            "implied_blame": narrative["valuation_target"]["label"],
            "force": narrative["narrative_force"]["label"],
            "confidence": 0.3,
            "method": "lexicon_inference",
        })

    return claims
```

### Phase 2: LLM-Based Extraction (2 weeks)

Using the existing BENI LLM infrastructure:

```python
from pipelines.shared.llm.clients import call_anthropic

def llm_causal_extraction(text, article_id):
    prompt = CAUSAL_PROMPT.format(text=text[:4000])
    response = call_anthropic("claude-sonnet-4-20250514", SYSTEM_PROMPT, [
        {"role": "user", "content": prompt}
    ])
    return json.loads(response)
```

### Phase 3: Causal Narrative Index

```python
def build_causal_narrative_index(articles_with_causal_claims):
    """
    Monthly index of causal claims.
    
    For each month:
    - Count claims per causal type (cost_push, demand_pull, etc.)
    - Measure: what fraction of claims blame government vs. external factors?
    - Track: which causal narratives are rising/falling?
    """
    df = pd.DataFrame(articles_with_causal_claims)
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")

    # Per-month causal type prevalence
    causal_index = df.groupby(["month", "causal_type"]).size().unstack(fill_value=0)

    # Normalize by total articles per month
    causal_index = causal_index.div(df.groupby("month").size(), axis=0)

    return causal_index
```

---

## References

### Core Reading

- Asghar, N. (2022). "A survey on extraction of causal relations from natural language text." *Knowledge and Information Systems*, 65: 773–816.
- Drury, B. et al. (2022). "A survey of the extraction and applications of causal relations." *Natural Language Engineering*, 28(3): 361–400.
- Garg, P. & Fetzer, T. (2026). "Causal Claims in Economics." arXiv: `2501.06873`.
  — Maps 44,852 economics papers into causal claim graphs. Causal edge share rose from 7.7% (1990) to 31.7% (2020).
- Norouzi, R. et al. (2025). "Capturing Causal Claims: A Fine-Tuned Text Mining Model." F1 = 0.89 on social science causal sentences.

### Economic Application

- Andre, P. et al. (2026). "Narratives about the Macroeconomy." *Review of Economic Studies*.
  — Causal evidence that narratives shape inflation expectations.
- Lange, K.-R. et al. (2022). "Towards extracting collective economic narratives from texts." *Ruhr Economic Papers #963*.
  — Causal linking as core contribution.

### See Also

- Level 8: [Narrative Networks and Graphs](L08_narrative_networks_graphs.md) — Graphs from causal claims
- Level 9: [RELATIO-Style Extraction](L09_relatio_style_extraction.md) — Entity-relation aggregation
- Level 10: [LLM-Based Extraction](L10_llm_based_extraction.md) — LLM for causal inference

---

**Up:** [Methodologies Index](INDEX.md) | **Main:** [Narrative Extraction Methodologies](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
