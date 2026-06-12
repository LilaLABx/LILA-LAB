> **Navigation:** [Documentation Portal](../../index.md) > [Research](../) > [Methodologies](./) > Level 0
>
> ---

# Level 0: Manual Qualitative Coding

> **Hierarchy:** Foundation — the oldest and most trusted method for narrative extraction.
> **BENI Status:** ✅ Implemented (300-article gold-standard reference set in progress)
> **Core Idea:** Human annotators read text and assign structured codes based on interpretation.

---

## Table of Contents

1. [Overview](#overview)
2. [Techniques](#techniques)
3. [Worked Example](#worked-example)
4. [Strengths & Weaknesses](#strengths--weaknesses)
5. [When to Use Level 0](#when-to-use-level-0)
6. [BENI Implementation Detail](#beni-implementation-detail)
7. [Best Practices](#best-practices)
8. [Transitioning to Automated Levels](#transitioning-to-automated-levels)
9. [References](#references)

---

## Overview

Manual qualitative coding is the human-driven process of reading text and assigning structured codes or labels based on interpretation. It is the foundation upon which all automated narrative extraction methods are built — because every supervised method requires human-labeled training data, and every evaluation needs a gold standard.

### Key Principle

**Humans interpret meaning; machines count patterns.** Level 0 leverages human cognitive abilities — understanding context, detecting sarcasm, recognizing cultural references, and inferring implicit causality — that remain beyond automated methods.

### Role in the Hierarchy

```
L0 Manual Labels
    ↓
L1-L10 Automated Methods
    ↓
L0 Validation (Gold Standard)
```

Level 0 serves two distinct roles:
1. **Upstream:** Creates training data for supervised methods (L2, L4, L10)
2. **Downstream:** Provides gold-standard evaluation for all automated methods

---

## Techniques

### Content Analysis

The systematic categorization of text into predetermined codes.

```
Process:
1. Define coding scheme (categories, rules, examples)
2. Train annotators on pilot data
3. Annotators independently code each document
4. Measure inter-annotator agreement
5. Resolve disagreements through discussion or adjudication
6. Lock the coded dataset
```

### Thematic Coding

Inductive discovery of themes from the text itself — codes emerge from data rather than being pre-defined.

```
Process:
1. Open coding: read and assign preliminary codes to segments
2. Axial coding: group codes into categories
3. Selective coding: identify core themes
4. Iterate until theoretical saturation
```

### Grounded Theory

An iterative methodology where theory emerges systematically from data:

```
Data Collection
    ↓
Coding (open → axial → selective)
    ↓
Memo Writing
    ↓
Theoretical Sampling
    ↓
Theory Emergence
```

### Frame Analysis

Identifies how issues are presented — what is emphasized, downplayed, or omitted.

| Frame Element | Question | Example |
|--------------|----------|---------|
| Problem definition | What is the issue? | "Inflation is rising" |
| Causal attribution | Who or what caused it? | "Government overspending" |
| Moral evaluation | Is it good or bad? | "This is a crisis" |
| Treatment recommendation | What should be done? | "Cut spending immediately" |

### Narrative Inquiry

Holistic analysis of complete stories rather than coded segments. Preserves narrative structure — beginning, middle, end — and identifies plot, characters, and setting.

---

## Worked Example

### Article Text

> Inflation is rising because government spending increased. Households are struggling to afford basic goods. The central bank must act now.

### Human Annotator Codes

| Field | Code | Rationale |
|-------|------|-----------|
| Topic | Inflation | The primary subject |
| Cause | Government spending | Explicit causal claim |
| Effect | Rising prices | The outcome described |
| Actor 1 | Government | Responsible for cause |
| Actor 2 | Households | Affected by outcome |
| Actor 3 | Central Bank | Expected to respond |
| Stance | Negative | Portrayed as harmful |
| Urgency | High | "Must act now" |

### Annotator Notes

*"The article presents a clear causal narrative: government → spending → inflation → household burden. The central bank is framed as the potential solution. Tone is urgent and critical of government policy."*

---

## Strengths & Weaknesses

### Strengths

| Strength | Description |
|----------|-------------|
| **High validity** | Humans understand context, nuance, and implicit meaning |
| **Rich interpretation** | Can capture causality, stance, emotion, and cultural references |
| **Gold-standard quality** | Essential for training and evaluating automated systems |
| **Flexibility** | Adaptable to any domain, language, or research question |
| **Theory-driven** | Codes can test specific hypotheses |

### Weaknesses

| Weakness | Description | Mitigation |
|----------|-------------|------------|
| **Expensive** | Requires trained annotators, domain expertise, time | Use LLM-assisted pre-annotation (L10) |
| **Doesn't scale** | Linear cost per document | Use to create training data for automated methods |
| **Subjectivity** | Different annotators may interpret differently | Formal protocol, inter-annotator agreement targets |
| **Fatigue effects** | Quality degrades over long annotation sessions | Limit sessions, rotate tasks, include quality checks |
| **Concept drift** | Annotator understanding may shift over time | Periodic recalibration, randomized document order |

---

## When to Use Level 0

| Scenario | Recommended | Alternative |
|----------|-------------|-------------|
| Creating a gold-standard evaluation set | ✅ **Level 0** | — |
| Training data for supervised classifiers | ✅ **Level 0** (small) + L10 (large) | L10 alone if budget limited |
| Exploratory research in a new domain | ✅ **Level 0** (thematic coding) | L3/L4 topic modeling |
| Very large corpus (1M+ documents) | ❌ Too expensive | L10 → L2/L4 pipeline |
| Real-time narrative tracking | ❌ Too slow | L1 or L10 automated |

---

## BENI Implementation Detail

### Code References

| File | Purpose | Key Details |
|------|---------|-------------|
| `pipelines/BENI/annotation/ANNOTATOR_GUIDE.md` | Human annotator instructions | Protocols, code definitions, edge case handling |
| `pipelines/BENI/annotation/ANNOTATION_SCHEMA.md` | 12-field annotation schema | Current binary + planned multiclass expansion |
| `pipelines/BENI/annotation/ADJUDICATION_PROTOCOL.md` | Disagreement resolution | Majority voting, tiebreaker rules, Cohen's κ targets |
| `pipelines/BENI/annotation/label_config.xml` | Label Studio config | XML for Label Studio interface |
| `pipelines/BENI/annotation/export_for_labelstudio.py` | Export to Label Studio | Batch preparation, stratified sampling |
| `pipelines/BENI/annotation/adjudicate.py` | Agreement computation | Cohen's κ, confusion matrices, per-field reports |
| `pipelines/BENI/annotation/setup_project.py` | Project setup | Label Studio project creation |

### Current Implementation

The BENI pipeline uses Level 0 at three points:

1. **300-article locked reference set** (in progress):
   - Stratified sample: economic + non-economic, across sections/time
   - 7 fields annotated per article
   - Locked after final adjudication — no further label changes
   - Serves as the exclusive evaluation benchmark

2. **Multi-LLM adjudication** (operational):
   - LLM annotations (L10) are treated as "annotators"
   - Cohen's κ computed between Claude, GPT-4o, Gemini
   - Majority-vote consensus with confidence weighting

3. **Keyword label quality audit** (exploratory):
   - Human review of keyword-based labels (L1)
   - Schema coverage validation via manual inspection

### Annotation Schema (Current)

```json
{
  "economic_relevance": "Economic | Not Economic",
  "confidence": "1 (guessing) | 2 (fairly sure) | 3 (certain)",
  "difficulty": "Clear-cut | Borderline",
  "economic_topic": "inflation | exchange_rate | reserves | banking | fiscal_policy | trade | employment | growth_investment | other",
  "narrative_force": "crisis | burden | blame | reform | stability | uncertainty | resilience | neutral",
  "valuation_target": "government | central_bank | banks | businesses | market_actors | global_economy | households | unnamed_system",
  "sentiment": "negative | neutral | positive"
}
```

### Quality Targets

| Metric | Target |
|--------|--------|
| Cohen's κ (LLM self-consistency) | ≥ 0.80 |
| Cohen's κ (human-human) | ≥ 0.70 |
| Cohen's κ (human-LLM) | ≥ 0.60 |
| Macro F1 (economic_relevance) | ≥ 0.80 |
| Macro F1 (economic_topic) | ≥ 0.75 |
| Macro F1 (narrative_force) | ≥ 0.60 |

---

## Best Practices

### Designing an Annotation Protocol

1. **Start small**: Pilot with 20-30 documents before scaling
2. **Define edge cases explicitly**: What counts as "borderline"? How to handle mixed-language text?
3. **Include "impossible" documents**: Some documents genuinely cannot be coded — document the criteria for exclusion
4. **Stratify your sample**: Ensure your gold set represents the full diversity of your corpus
5. **Lock and publish**: Once agreed, freeze the reference set and never change labels

### Training Annotators

1. **Codebook training**: Annotators read and discuss the codebook together
2. **Pilot annotation**: 20 documents annotated independently, then discussed
3. **Calibration**: Compare Cohen's κ after each batch; discuss disagreements
4. **Ongoing monitoring**: Track per-annotator agreement trends

### Measuring Agreement

| Metric | What It Measures | Interpretation |
|--------|-----------------|----------------|
| **Cohen's κ** | Agreement beyond chance | κ ≥ 0.80 = strong, ≥ 0.60 = moderate |
| **Krippendorff's α** | Generalizes to 2+ annotators | Same thresholds |
| **Percent agreement** | Raw agreement rate | Misleading for rare categories |
| **Fleiss' κ** | Multi-annotator agreement | Use for 3+ annotators |

---

## Transitioning to Automated Levels

Manual coding (L0) is not an end in itself — it enables automated methods. The standard transition path:

```
L0: Manual Labels (300-1,000 documents)
    ↓
L10: LLM Pre-annotation (same schema, same documents)
    ↓
L0+L10: Agreement analysis → Refine prompt/labels
    ↓
L10: LLM annotation at scale (all documents)
    ↓
L2: Classifier training on LLM labels (any corpus size)
    ↓
L0: Final validation on the locked reference set
```

For the BENI pipeline, this means:

1. **Complete** the 300-article reference set (L0)
2. **Compare** LLM labels against it (L10 vs L0)
3. **Adjust** LLM prompts based on systematic disagreements
4. **Scale** LLM annotation to all 664K articles
5. **Train** the TF-IDF/BanglaBERT classifier on scaled labels
6. **Validate** every model iteration against the locked L0 set

---

## References

### Core Reading

- Krippendorff, K. (2018). *Content Analysis: An Introduction to Its Methodology.* 4th ed. SAGE.
  — The definitive text on content analysis methodology.

- Charmaz, K. (2014). *Constructing Grounded Theory.* 2nd ed. SAGE.
  — Grounded theory methodology for qualitative coding.

- Neuendorf, K. A. (2016). *The Content Analysis Guidebook.* 2nd ed. SAGE.
  — Practical guide to designing content analysis studies.

### BENI-Specific

- Nabil, A. N. (2026). "BENI Annotation Schema." `pipelines/BENI/annotation/ANNOTATION_SCHEMA.md`
- Nabil, A. N. (2026). "BENI Annotator Guide." `pipelines/BENI/annotation/ANNOTATOR_GUIDE.md`
- Nabil, A. N. (2026). "BENI Adjudication Protocol." `pipelines/BENI/annotation/ADJUDICATION_PROTOCOL.md`

### See Also

- Level 10: [LLM-Based Narrative Extraction](L10_llm_based_extraction.md) — LLM as annotator
- Level 1: [Lexicon-Based Narrative Detection](L01_lexicon_based_detection.md) — First automated step

---

**Up:** [Methodologies Index](INDEX.md) | **Main:** [Narrative Extraction Methodologies](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
