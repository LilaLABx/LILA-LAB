> **Navigation:** [Documentation Portal](../../index.md) > [Research](../) > [Methodologies](./) > Level 10
>
> ---

# Level 10: LLM-Based Narrative Extraction

> **Hierarchy:** Current state-of-the-art for narrative extraction — LLMs can perform all lower-level tasks within a single prompt with deep semantic understanding.
> **BENI Status:** ✅ Implemented (primary annotation method — Claude, GPT-4o, Gemini ensemble)
> **Core Idea:** Use large language models as narrative extraction devices — prompt them to read text and return structured narrative components.

---

## Table of Contents

1. [Overview](#overview)
2. [Why LLMs for Narrative Extraction](#why-llms-for-narrative-extraction)
3. [Prompt Engineering for Narrative Extraction](#prompt-engineering-for-narrative-extraction)
4. [Structured Output Extraction](#structured-output-extraction)
5. [Multi-LLM Ensemble Methods](#multi-llm-ensemble-methods)
6. [Confidence Calibration](#confidence-calibration)
7. [Cost and Scalability](#cost-and-scalability)
8. [Worked Example](#worked-example)
9. [Strengths & Weaknesses](#strengths--weaknesses)
10. [When to Use Level 10](#when-to-use-level-10)
11. [BENI Implementation Details](#beni-implementation-details)
12. [Recommended Improvements](#recommended-improvements)
13. [References](#references)

---

## Overview

LLM-based narrative extraction uses large language models (Claude, GPT-4o, Gemini) as programmable annotation devices. Rather than building specialized classifiers for each narrative dimension, a single prompt instructs the LLM to extract all relevant narrative components — topic, actors, causal claims, stance, and confidence — in structured JSON format.

### Key Principle

**LLMs collapse the hierarchy.** A single Level 10 prompt can perform keyword spotting (L1), classification (L2), event extraction (L5), semantic role labeling (L6), and causal detection (L7) simultaneously. The trade-off: cost, reproducibility, and hallucination risk.

### The Core Paradigm

```
Raw Text
    ↓
LLM Prompt: "Extract narrative components as JSON"
    ↓
Structured Output: { topic, actors, cause, effect, stance, confidence }
    ↓
Validation: Self-consistency, cross-model agreement, human audit
```

---

## Why LLMs for Narrative Extraction

### The Case for LLMs

| Advantage | Description | BENI Impact |
|-----------|-------------|-------------|
| **Zero-shot capability** | Extract narratives without training data | Bootstrap new languages instantly |
| **Deep understanding** | Grasp implicit causality, sarcasm, cultural context | Richer narrative extraction than any lower level |
| **Multilingual** | Work across all XENI target languages | Single pipeline for 10 languages |
| **Multi-task** | Extract topic + actors + causality + stance in one call | Collapse L0–L9 into single prompt |
| **Adaptable** | Change schema by editing prompt text | Rapid iteration on annotation schema |

### The Case Against LLMs

| Disadvantage | Description | Mitigation |
|--------------|-------------|------------|
| **Hallucination** | May extract narratives not present | Self-consistency checks, confidence calibration |
| **Reproducibility** | Same prompt + text → different results | Temperature 0, multiple passes |
| **Cost** | API-based at scale is expensive | Use for gold labels, distil to cheaper models |
| **Latency** | Real-time extraction challenging | Batch processing, smaller models |
| **Drift** | Model updates change behavior | Version-pin models, monitor distributions |

---

## Prompt Engineering for Narrative Extraction

### Prompt Architecture

Effective narrative extraction prompts have four components:

```
1. ROLE: "You are an expert economic narrative annotator..."
2. TASK: "Extract all economic narratives from the following text..."
3. SCHEMA: "Return a JSON object with these fields: ..."
4. CONSTRAINTS: "Only extract explicitly stated narratives..."
```

### BENI's Current Prompt (from `llm_annotate.py`)

```python
SYSTEM_PROMPT = """You are an expert annotator for economic news content in Bengali.
You are building the Bangla Economic Narrative Index (BENI).
Your task is to classify Bengali news articles across multiple dimensions.

Read each article carefully and respond with a JSON object containing
your annotations. Be precise and consistent."""

USER_PROMPT_TEMPLATE = """Annotate the following Bengali news article according
to the BENI schema.

ARTICLE ID: {article_id}
ARTICLE TEXT:
{text}

Respond with a JSON object containing exactly these fields:

1. "economic_relevance": "Economic" or "Not Economic"
2. "confidence": Integer 1-3
3. "difficulty": "Clear-cut" or "Borderline"
4. "economic_topic": One of 12 categories
5. "sentiment": "negative", "neutral", or "positive"
6. "narrative_force": One of 8 categories
7. "valuation_target": One of 8 categories
8. "notes": Brief reasoning (optional)
"""
```

### Prompt Design Principles for Narrative Extraction

| Principle | Bad Practice | Good Practice |
|-----------|-------------|---------------|
| **Specific schema** | "Extract the narrative" | "Return JSON with exactly: actor, cause, effect, stance" |
| **Category examples** | "Classify the topic" | "Topic must be one of: inflation_prices, exchange_rate_reserves, ..." |
| **Edge case handling** | No guidance | "If no economic narrative exists, return empty array" |
| **Explicit constraints** | "Be careful" | "Do NOT extract narratives that are only implied" |
| **Output format** | Free text | Strict JSON with required fields |

### Advanced Prompt: Causal Narrative Extraction

```python
CAUSAL_NARRATIVE_PROMPT = """
Extract ALL economic narratives from this Bangla news article.

For each narrative, identify:
1. NARRATIVE_TEXT: A concise summary of the narrative (1 sentence)
2. ACTOR: Who is driving the narrative? (government, central bank, businesses, etc.)
3. CAUSE: What caused the economic condition?
4. EFFECT: What is the economic outcome?
5. MECHANISM: How does the cause lead to the effect?
6. STANCE: positive, negative, or neutral?
7. CONFIDENCE: 0.0-1.0
8. EVIDENCE_SPAN: Exact quote from the article supporting this narrative

Economic narratives only. If no economic narrative is present, return empty array.

Return as JSON:
{
    "narratives": [
        {
            "narrative_text": "...",
            "actor": "...",
            "cause": "...",
            "effect": "...",
            "mechanism": "...",
            "stance": "negative",
            "confidence": 0.92,
            "evidence_span": "..."
        }
    ]
}

Article: {text}
"""
```

---

## Structured Output Extraction

### JSON Mode / Structured Output

Modern LLM APIs support guaranteed structured output:

```python
import anthropic

client = anthropic.Anthropic()

def extract_narrative_structured(text, article_id):
    """Use Claude's structured output for guaranteed JSON."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": USER_PROMPT_TEMPLATE.format(
                article_id=article_id, text=text
            )
        }],
        # Enable structured output
        extra_headers={"anthropic-structured-output": "true"}
    )
    return json.loads(response.content[0].text)
```

### Schema Validation

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional

class EconomicNarrative(BaseModel):
    """Validated schema for economic narrative extraction."""
    narrative_text: str = Field(description="Summary of the narrative")
    actor: str = Field(description="Entity driving the narrative")
    cause: str = Field(description="Causal factor")
    effect: str = Field(description="Economic outcome")
    mechanism: Literal[
        "cost_push", "demand_pull", "monetary", "external_shock",
        "policy_response", "structural", "other"
    ] = Field(description="Causal mechanism")
    stance: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_span: Optional[str] = Field(None)

class NarrativeExtractionResult(BaseModel):
    narratives: list[EconomicNarrative]

def validate_extraction(raw_json: dict) -> NarrativeExtractionResult:
    """Validate LLM output against schema."""
    return NarrativeExtractionResult.model_validate(raw_json)
```

### Post-Processing Pipeline

```python
def post_process_narratives(raw_output: str, article_id: str) -> dict:
    """Clean and validate LLM narrative output."""
    try:
        # Parse JSON
        data = json.loads(raw_output)

        # Validate schema
        validated = validate_extraction(data)

        # Add metadata
        return {
            "article_id": article_id,
            "narratives": [n.model_dump() for n in validated.narratives],
            "narrative_count": len(validated.narratives),
            "extraction_status": "success",
        }

    except (json.JSONDecodeError, ValidationError) as e:
        # Fallback: extract JSON from markdown
        json_match = re.search(r'```json\n(.*?)\n```', raw_output, re.DOTALL)
        if json_match:
            return post_process_narratives(json_match.group(1), article_id)

        return {
            "article_id": article_id,
            "narratives": [],
            "narrative_count": 0,
            "extraction_status": f"failed: {str(e)}",
        }
```

---

## Multi-LLM Ensemble Methods

BENI uses a multi-provider ensemble to improve reliability. Three independent LLMs annotate each article, and disagreements are adjudicated.

### Ensemble Architecture

```python
class NarrativeEnsemble:
    """Multi-LLM ensemble for narrative extraction."""

    def __init__(self):
        self.annotators = {
            "claude": ClaudeAnnotator("claude-sonnet-4-20250514"),
            "gpt4o": GPTAnnotator("gpt-4o"),
            "gemini": GeminiAnnotator("gemini-2.0-flash"),
        }

    def annotate(self, text: str, article_id: str) -> dict:
        results = {}
        for name, annotator in self.annotators.items():
            try:
                results[name] = annotator.annotate(text, article_id)
            except Exception as e:
                results[name] = {"error": str(e)}

        return {
            "article_id": article_id,
            "individual": results,
            "ensemble": self.adjudicate(results),
        }

    def adjudicate(self, results: dict) -> dict:
        """Adjudicate disagreements across annotators."""
        # Collect non-error results
        valid = {k: v for k, v in results.items() if "error" not in v}

        if not valid:
            return {"status": "all_failed"}

        # Majority vote for categorical fields
        economic_votes = [
            v["economic_relevance"] for v in valid.values()
            if "economic_relevance" in v
        ]
        majority_relevance = max(set(economic_votes), key=economic_votes.count)

        # Average confidence scores
        confidences = [
            v.get("confidence", 0) for v in valid.values()
            if isinstance(v.get("confidence"), (int, float))
        ]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        # Agreement rate
        agreement = economic_votes.count(majority_relevance) / len(economic_votes)

        return {
            "status": "adjudicated",
            "economic_relevance": majority_relevance,
            "confidence": round(avg_confidence, 2),
            "agreement_rate": round(agreement, 2),
            "annotator_count": len(valid),
        }
```

### Agreement Analysis

```python
def analyze_ensemble_agreement(ensemble_results):
    """Analyze agreement patterns across annotators."""
    df = pd.DataFrame(ensemble_results)

    # Per-field agreement rates
    fields = ["economic_relevance", "economic_topic", "sentiment",
              "narrative_force", "valuation_target"]

    for field in fields:
        # Pairwise agreement
        agreements = []
        for _, row in df.iterrows():
            values = [v.get(field) for v in row["individual"].values()
                     if isinstance(v, dict) and field in v]
            if len(values) >= 2:
                # All agree?
                all_same = len(set(values)) == 1
                agreements.append(all_same)

        if agreements:
            print(f"{field}: {sum(agreements)}/{len(agreements)} "
                  f"full agreement ({sum(agreements)/len(agreements):.1%})")
```

### When to Use Each Agreement Strategy

| Strategy | When | Method |
|----------|------|--------|
| **Majority vote** | 3+ annotators, categorical fields | Most common label wins |
| **Average** | Continuous fields, all competent | Mean confidence score |
| **Weighted** | Known annotator quality differences | Performance-weighted average |
| **Conservative** | High-stakes classification | All must agree → label, else abstain |
| **Adjudication** | Gold-standard creation | Human resolves disagreements |

---

## Confidence Calibration

LLMs are notoriously overconfident. Calibration is essential for reliable narrative indices.

### Self-Consistency

```python
def self_consistency_check(text, article_id, n_passes=3):
    """Run multiple annotation passes and measure consistency."""
    results = []
    for pass_num in range(n_passes):
        # Vary seed to get different samples
        result = call_llm(text, article_id, seed=pass_num * 100)
        results.append(result)

    # Consistency metrics
    relevance_labels = [r["economic_relevance"] for r in results]
    consistency = relevance_labels.count(relevance_labels[0]) / len(relevance_labels)

    return {
        "passes": results,
        "consistency": consistency,
        "is_reliable": consistency >= 0.67,  # 2/3 agreement
    }
```

### Logprob-Based Confidence

```python
def extract_with_logprobs(text, prompt_template):
    """Extract confidence from model log probabilities."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt_template.format(text=text)}],
        # Request token-level logprobs
        extra_headers={"anthropic-logprobs": "true"},
    )

    # Parse response and extract confidence tokens
    content = response.content[0].text
    data = json.loads(content)

    # Add logprob-based confidence adjustment
    if "confidence" in data and isinstance(data["confidence"], (int, float)):
        # Adjust: if logprobs indicate uncertainty, reduce confidence
        data["confidence"] = adjust_by_logprobs(
            data["confidence"], response.logprobs
        )

    return data
```

### Calibration Across Aggregates

```python
def calibrate_ensemble_predictions(ensemble_results, human_labels):
    """Calibrate LLM confidence against human gold standard."""
    # For each annotator, compute calibration curve
    calibration = {}

    for annotator in ["claude", "gpt4o", "gemini"]:
        confidences = []
        accuracies = []

        for result, human in zip(ensemble_results, human_labels):
            pred = result["individual"].get(annotator, {})
            if "confidence" in pred:
                confidences.append(pred["confidence"])
                accuracies.append(
                    1 if pred.get("economic_relevance") == human["relevance"] else 0
                )

        # Bin by confidence
        bins = pd.cut(confidences, bins=5)
        bin_accuracy = pd.DataFrame({"conf": confidences, "acc": accuracies})\
            .groupby(bins)["acc"].mean()

        calibration[annotator] = bin_accuracy.to_dict()

    return calibration
```

---

## Cost and Scalability

### BENI Cost Analysis

| Operation | Provider | Cost per 1K Articles | Notes |
|-----------|----------|---------------------|-------|
| Basic relevance + topic | Claude Sonnet 4 | ~$3-5 | Short prompt, few tokens |
| Full narrative extraction | Claude Sonnet 4 | ~$8-12 | Extended prompt, more output |
| Ensemble (3 models) | All three | ~$20-30 | Full cross-validation |
| Active learning batch | Claude Sonnet 4 | ~$5-8 | Only uncertain articles |

### Scaling Strategies

```python
class ScalableNarrativeExtractor:
    """Cost-efficient narrative extraction at scale."""

    def __init__(self, llm_client, classifier_model):
        self.llm = llm_client
        self.classifier = classifier_model  # Cheap L2 classifier

    def extract_batch(self, articles, budget=0.10):
        """
        Extract narratives within a per-article budget.

        Strategy:
        - Use cheap classifier (L2) for broad screening
        - Use LLM (L10) only for articles the classifier is uncertain about
        - Use ensemble only for a random sample for quality monitoring
        """
        results = []

        for article in articles:
            # Step 1: Cheap classifier
            classifier_pred = self.classifier.predict([article["text"]])[0]
            classifier_prob = self.classifier.predict_proba([article["text"]])[0].max()

            # Step 2: Decide on LLM necessity
            if classifier_prob > 0.95:
                # High confidence — skip LLM
                results.append({
                    "article_id": article["id"],
                    "economic_relevance": classifier_pred,
                    "confidence": classifier_prob,
                    "method": "classifier_only",
                })
            elif classifier_prob > 0.7:
                # Medium confidence — single LLM pass
                llm_result = self.llm_extract(article["text"])
                results.append({
                    "article_id": article["id"],
                    **llm_result,
                    "method": "llm_single",
                })
            else:
                # Low confidence — full ensemble
                ensemble_result = self.ensemble_extract(article["text"])
                results.append({
                    "article_id": article["id"],
                    **ensemble_result,
                    "method": "llm_ensemble",
                })

        return results
```

### Cost Optimization Matrix

| Method | Cost/Article | Quality | When to Use |
|--------|-------------|---------|-------------|
| **Classifier-only** (L2) | ~$0.00001 | Good for binary | Clear-cut articles (80%+ of corpus) |
| **Single LLM pass** (L10) | ~$0.003 | Very good | Uncertain articles (15%) |
| **LLM ensemble** (L10) | ~$0.01 | Excellent | Gold-standard creation (5%) |
| **Human audit** (L0) | ~$1.00 | Ground truth | Validation set only |

---

## Worked Example

### Input Bangla Article

> *"বাংলাদেশে মূল্যস্ফীতি বেড়ে ৯.৫% হয়েছে, যা প্রধানত খাদ্য ও জ্বালানির দাম বৃদ্ধির কারণে। সরকার বলেছে, তারা দাম নিয়ন্ত্রণে ব্যবস্থা নিচ্ছে। কিন্তু অর্থনীতিবিদরা বলছেন, বর্তমান নীতি যথেষ্ট নয়। বাংলাদেশ ব্যাংক সুদের হার বাড়ানোর সংকেত দিয়েছে।"*
>
> (Inflation in Bangladesh has risen to 9.5%, mainly due to rising food and energy prices. The government says it is taking measures to control prices. But economists say current policies are not enough. The Bangladesh Bank has signaled raising interest rates.)

### LLM Extraction Output

```json
{
    "economic_relevance": "Economic",
    "confidence": 3,
    "difficulty": "Clear-cut",
    "economic_topic": "inflation_prices",
    "sentiment": "negative",
    "narrative_force": "crisis_warning",
    "valuation_target": "government",
    "narratives": [
        {
            "narrative_text": "Food and energy price increases are driving inflation to crisis levels",
            "actor": "global_market",
            "cause": "rising food and energy prices",
            "effect": "inflation at 9.5%",
            "mechanism": "cost_push",
            "stance": "negative",
            "confidence": 0.95,
            "evidence_span": "মূল্যস্ফীতি বেড়ে ৯.৫% হয়েছে, যা প্রধানত খাদ্য ও জ্বালানির দাম বৃদ্ধির কারণে"
        },
        {
            "narrative_text": "Government policies are insufficient to control inflation",
            "actor": "government",
            "cause": "inadequate policy measures",
            "effect": "uncontrolled inflation",
            "mechanism": "policy_response",
            "stance": "negative",
            "confidence": 0.85,
            "evidence_span": "অর্থনীতিবিদরা বলছেন, বর্তমান নীতি যথেষ্ট নয়"
        },
        {
            "narrative_text": "Central bank will raise interest rates to combat inflation",
            "actor": "central_bank",
            "cause": "rising inflation",
            "effect": "interest rate hike",
            "mechanism": "monetary",
            "stance": "neutral",
            "confidence": 0.90,
            "evidence_span": "বাংলাদেশ ব্যাংক সুদের হার বাড়ানোর সংকেত দিয়েছে"
        }
    ],
    "has_causal_claim": true,
    "causal_claims": [
        {"cause": "rising food and energy prices", "effect": "inflation 9.5%", "type": "cost_push"},
        {"cause": "inadequate policies", "effect": "uncontrolled inflation", "type": "policy_failure"}
    ]
}
```

### Ensemble Comparison

```text
Field              | Claude    | GPT-4o    | Gemini    | Agreement
-------------------|-----------|-----------|-----------|----------
economic_relevance | Economic  | Economic  | Economic  | ✅ 3/3
economic_topic     | inflation | inflation | inflation | ✅ 3/3
sentiment          | negative  | negative  | negative  | ✅ 3/3
narrative_force    | crisis    | crisis    | burden    | ⚠️ 2/3
valuation_target   | govt      | govt      | central_bk| ⚠️ 2/3
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Description |
|----------|-------------|
| **Deep semantic understanding** | Captures implicit causality, cultural context, nuance |
| **Zero-shot cross-lingual** | Works for all XENI languages without training data |
| **Multi-task** | Single prompt performs L1–L9 tasks simultaneously |
| **Rapid iteration** | Schema changes = prompt changes, no model retraining |
| **Human-aligned** | Extracts narratives the way a human reader would |

### Weaknesses

| Weakness | Description | Mitigation |
|----------|-------------|------------|
| **Hallucination** | May extract narratives not in text | Self-consistency, evidence spans |
| **Reproducibility** | Non-deterministic output | Temperature 0, version pinning |
| **Cost at scale** | API cost for millions of documents | Distillation to cheaper models |
| **Latency** | Slow for real-time applications | Batch processing, smaller models |
| **Model drift** | Updates change behavior | Monitor distributions, pin versions |
| **Bias** | Training data biases affect extraction | Regular bias audits |

---

## When to Use Level 10

| Scenario | Recommended | Alternative |
|----------|-------------|-------------|
| Gold-standard annotation creation | ✅ **Level 10** + L0 human validation | — |
| Extracting complex narrative structure | ✅ **Level 10** | L7 may miss implicit causality |
| Cross-lingual narrative extraction | ✅ **Level 10** | — |
| Rapid schema prototyping | ✅ **Level 10** | Edit prompt, not model |
| Million-document corpus | ⚠️ Cost-prohibitive alone | Distil to L2 classifier |
| Real-time extraction | ❌ Too slow | L2 or L1 for speed |
| Fully reproducible research | ⚠️ Use with care | Pin models, temperature 0 |

---

## BENI Implementation Details

### Current BENI LLM Pipeline

**File:** [`pipelines/BENI/annotation/llm_annotate.py`](../../pipelines/BENI/annotation/llm_annotate.py)

**Architecture:**

```
Article (JSON batch)
    ↓
LLM Annotator (2 passes per article for self-consistency)
    ↓
    ├── Pass 1: seed=42, temperature=0.0
    └── Pass 2: seed=2024, temperature=0.2
    ↓
Structured Output: 8-field JSON schema
    ↓
Analysis: agreement, confidence, cost reporting
```

**Supported Providers:**

| Provider | Model | Key Variable |
|----------|-------|-------------|
| Anthropic | Claude Sonnet 4 | `ANTHROPIC_API_KEY` |
| OpenAI | GPT-4o | `OPENAI_API_KEY` |
| Google | Gemini 2.0 Flash | `GEMINI_API_KEY` |

**Current Schema (8 fields):**

1. `economic_relevance` — "Economic" / "Not Economic"
2. `confidence` — 1 (guessing) to 3 (certain)
3. `difficulty` — "Clear-cut" / "Borderline"
4. `economic_topic` — 12 categories (inflation_prices, exchange_rate_reserves, ...)
5. `sentiment` — negative / neutral / positive
6. `narrative_force` — 8 categories (crisis_warning, blame_criticism, ...)
7. `valuation_target` — 8 categories (government, central_bank, ...)
8. `notes` — Free-text reasoning

### Current Limitations

1. **Binary extraction only** — Classifies articles but does not extract narrative text spans
2. **Single-pass for most fields** — Only relevance uses ensemble; force and target use one model
3. **No explicit causal extraction** — Schema lacks cause-effect fields
4. **Temperature 0.0** — Deterministic but may miss valid alternative interpretations
5. **No span-level evidence** — Cannot trace which sentence supports which label

### Running the Pipeline

```bash
# Single provider, single pass
python3 llm_annotate.py \
    --provider anthropic \
    --model claude-sonnet-4-20250514 \
    --input exports/beni_300_batch.json \
    --output exports/llm_pass1.json \
    --pass-id 1

# Multi-provider ensemble
python3 multi_llm_ensemble.py \
    --input exports/beni_300_batch.json \
    --output exports/ensemble_results.json

# Analyze consistency
python3 analyze_llm_annotations.py \
    --pass1 exports/llm_pass1.json \
    --pass2 exports/llm_pass2.json \
    --output exports/llm_report.json
```

---

## Recommended Improvements

### Priority 1: Causal Extraction (HIGH)

Extend the prompt to extract explicit cause-effect relations:

```python
ENHANCED_SCHEMA = {
    "economic_relevance": "Economic | Not Economic",
    "economic_topic": "12 categories",
    "sentiment": "negative | neutral | positive",
    "narrative_force": "8 categories",
    "valuation_target": "8 categories",
    "causal_claims": [  # NEW
        {
            "cause": "What caused the condition?",
            "effect": "What is the outcome?",
            "mechanism": "cost_push | demand_pull | monetary | external_shock | policy_response | structural | other",
            "confidence": 0.0-1.0,
            "evidence_span": "Supporting quote from article"
        }
    ]
}
```

### Priority 2: Span-Level Evidence (HIGH)

Require the LLM to cite specific spans, enabling:
- Verifiability of each label
- Training data for sequence labeling models
- Richer downstream analysis

### Priority 3: Multi-Turn Extraction (MEDIUM)

```python
# Turn 1: Extract candidate narratives
# Turn 2: Validate and refine
# Turn 3: Cross-check with extracted evidence spans
```

### Priority 4: Confidence Calibration (MEDIUM)

```python
# Use logprobs for token-level confidence
# Calibrate against human gold standard
# Report calibrated confidence in index construction
```

### Priority 5: Distillation to Cheaper Models (LOW)

```python
# Use LLM outputs as training data for:
# - BanglaBERT (L4 classifier)
# - TF-IDF (L2 classifier)
# - Small fine-tuned models for production
```

---

## References

### Core Reading

- Schmidt, T., Lange, K.-R., Reccius, M., Müller, H., Roos, M. W. M., & Jentsch, C. (2025). "Identifying economic narratives in large text corpora: An integrated approach using large language models." *Ruhr Economic Papers #1163*. DOI: `10.4419/96973348`.
  — Tests GPT-4o against expert-annotated gold-standard. LLMs fall short of expert-level on complex documents.

- Tian, Q. et al. (2026). "Narrative Knowledge Weaver." *ICLR 2026*.
  — Multi-agent framework with adaptive schema induction and reflection-augmented extraction.

- Ash, E., Gauthier, G., & Widmer, P. (2023). "RELATIO: Text Semantics Capture Political and Economic Narratives." *Political Analysis*.
  — LLM-based triple extraction as alternative to dependency parsing.

### Prompt Engineering

- White, J. et al. (2023). "Prompt Patterns for Structured LLM Output." arXiv: `2302.11382`.
  — Patterns for reliable structured extraction.

- Reynolds, L. & McDonell, K. (2021). "Prompt Programming for Large Language Models." arXiv: `2102.07350`.
  — Foundations of prompt-based extraction.

### BENI-Specific

- Nabil, A. N. (2026). "BENI LLM Annotation Pipeline." `pipelines/BENI/annotation/llm_annotate.py`.
  — Current BENI implementation — 8-field schema with Claude/GPT-4o/Gemini ensemble.

- Nabil, A. N. (2026). "BENI v1.0 Dataset Annotation." `dataset/BENI/beni-v1/`.
  — 1.47M articles with LLM-generated seed labels.

### See Also

- Level 0: [Manual Qualitative Coding](L00_manual_qualitative_coding.md) — Human validation of LLM output
- Level 7: [Causal Narrative Extraction](L07_causal_narrative_extraction.md) — Causal extension for L10 prompts
- Level 9: [RELATIO-Style Extraction](L09_relatio_style_extraction.md) — Triple extraction via LLM
- Level 11: [Agentic Discovery Systems](L11_agentic_discovery_systems.md) — Autonomous LLM-driven pipelines

---

**Up:** [Methodologies Index](INDEX.md) | **Main:** [Narrative Extraction Methodologies](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
