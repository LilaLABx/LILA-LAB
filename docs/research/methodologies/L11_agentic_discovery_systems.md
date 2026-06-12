# Level 11: Agentic Narrative Discovery Systems

> **Hierarchy:** The emerging frontier — autonomous, continuous narrative discovery through multi-agent LLM pipelines.
> **BENI Status:** ⬜ Not Yet Implemented (currently batch-process, not continuous)
> **Core Idea:** Deploy autonomous AI agents that continuously ingest text, extract narratives, build graphs, detect emerging stories, and flag novel narrative patterns — all without human intervention.

---

## Table of Contents

1. [Overview](#overview)
2. [Agentic Systems for Narrative Discovery](#agentic-systems-for-narrative-discovery)
3. [Multi-Agent Architecture](#multi-agent-architecture)
4. [Continuous Ingestion and Processing](#continuous-ingestion-and-processing)
5. [Narrative Emergence Detection](#narrative-emergence-detection)
6. [Autonomous Narrative Observatory](#autonomous-narrative-observatory)
7. [Worked Example](#worked-example)
8. [Strengths & Weaknesses](#strengths--weaknesses)
9. [When to Use Level 11](#when-to-use-level-11)
10. [BENI Implementation Guide](#beni-implementation-guide)
11. [Research Frontier](#research-frontier)
12. [References](#references)

---

## Overview

Agentic narrative discovery systems represent the most advanced level of narrative extraction — where the process becomes **autonomous, continuous, and self-improving**. Rather than running a batch pipeline on a static corpus, a Level 11 system continuously ingests new text, extracts narratives, updates graphs, detects emerging patterns, and alerts researchers to novel narrative developments.

### Key Principle

**Narrative extraction should be continuous, not episodic.** Economic narratives don't follow research workflows — they emerge, spread, compete, and fade in real time. Level 11 systems mirror this dynamism.

### From Batch to Continuous

```
Batch Pipeline (BENI current):
Collect 2014–2020 data → Annotate → Classify → Index → Publish
                                (months per cycle)

Agentic System (Level 11):
Ingest daily → Extract → Update Graph → Detect Emergence → Alert
                                (hours per cycle)
```

---

## Agentic Systems for Narrative Discovery

### What Makes a System "Agentic"

| Feature | Batch Pipeline | Agentic System |
|---------|---------------|----------------|
| **Processing mode** | Periodic batch | Continuous stream |
| **Decision-making** | Fixed pipeline logic | Autonomous routing decisions |
| **Adaptation** | Manual retraining | Self-improving via feedback |
| **Scope** | Fixed corpus | Open-ended ingestion |
| **Alerting** | None (produces reports) | Proactive emergence detection |
| **Multi-LLM** | Ensemble for accuracy | Specialized agent roles |
| **Memory** | Database | Graph + vector + episodic memory |

### The Narrative Agent Stack

```
                         ┌──────────────────────────┐
                         │   Orchestrator Agent      │
                         │  Routes work, manages     │
                         │  agent communication      │
                         └──────────┬───────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│  Collection Agent     │ │  Extraction Agent     │ │  Analysis Agent      │
│  - RSS/API ingestion  │ │  - LLM narrative ext. │ │  - Graph update      │
│  - Source monitoring  │ │  - Causal detection   │ │  - Community detect   │
│  - Deduplication      │ │  - Entity extraction  │ │  - Trend analysis    │
└───────────────────────┘ └───────────────────────┘ └───────────────────────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────────┐
                         │   Verification Agent     │
                         │  - Cross-validate        │
                         │  - Anomaly detection     │
                         │  - Human escalation      │
                         └──────────────────────────┘
```

---

## Multi-Agent Architecture

### Agent Roles and Responsibilities

```python
class NarrativeAgent:
    """Base class for narrative discovery agents."""

    def __init__(self, name: str, llm_client, tools: list):
        self.name = name
        self.llm = llm_client
        self.tools = {t.name: t for t in tools}
        self.memory = []

    def act(self, task: dict) -> dict:
        """Perceive, reason, act, observe."""
        observation = self._perceive(task)
        reasoning = self._reason(observation)
        action = self._execute(reasoning)
        result = self._observe(action)
        self.memory.append({"task": task, "result": result})
        return result

    def _perceive(self, task): ...
    def _reason(self, observation): ...
    def _execute(self, plan): ...
    def _observe(self, action): ...
```

### Orchestrator Agent

```python
class NarrativeOrchestrator:
    """Routes articles to appropriate agents and synthesizes results."""

    def __init__(self):
        self.collector = CollectionAgent()
        self.extractor = ExtractionAgent()
        self.analyzer = AnalysisAgent()
        self.verifier = VerificationAgent()
        self.graph_db = NarrativeGraphDB()
        self.vector_store = VectorStore()

    def process_article(self, article: dict) -> dict:
        """End-to-end processing of a single article."""

        # Step 1: Collect and normalize
        normalized = self.collector.clean(article)

        # Step 2: Extract narrative components
        extraction = self.extractor.extract(normalized)

        # Step 3: Update knowledge base
        self.graph_db.add_article(
            normalized["id"],
            extraction["entities"],
            extraction["causal_claims"],
            extraction["timestamp"],
        )
        self.vector_store.add_embedding(
            normalized["id"],
            extraction["embedding"],
        )

        # Step 4: Analyze for emergence
        insights = self.analyzer.detect_emergence(
            extraction,
            self.graph_db,
            self.vector_store,
        )

        # Step 5: Verify and escalate
        if insights.get("novelty_score", 0) > 0.8:
            self.verifier.escalate_for_review(normalized, extraction, insights)

        return {
            "article_id": normalized["id"],
            "extraction": extraction,
            "insights": insights,
            "processed_at": datetime.now().isoformat(),
        }
```

### Specialized Extraction Agent

```python
class ExtractionAgent(NarrativeAgent):
    """Specialized agent for narrative extraction from text."""

    def __init__(self, llm_client):
        super().__init__("extractor", llm_client, tools=[extract_narratives_tool])
        self.schema = self._load_current_schema()

    def extract(self, article: dict) -> dict:
        """Extract all narrative components from an article."""
        prompt = self._build_extraction_prompt(article)

        response = self.llm(prompt)

        result = {
            "id": article["id"],
            "timestamp": article["date"],
            "narratives": response.get("narratives", []),
            "entities": response.get("entities", []),
            "causal_claims": response.get("causal_claims", []),
            "embedding": response.get("embedding", None),
            "summary": response.get("summary", ""),
            "confidence": response.get("confidence", 0.0),
            "extraction_time": datetime.now().isoformat(),
        }

        # Self-consistency check
        if result["confidence"] < 0.5:
            result["needs_review"] = True
            result["review_reason"] = "low_confidence"

        return result

    def _build_extraction_prompt(self, article):
        return f"""
        Extract all economic narratives from this Bangla news article.
        Identify actors, actions, causal claims, entities, and stance.

        Current schema version: {self.schema['version']}

        Article: {article['text'][:4000]}
        """
```

---

## Continuous Ingestion and Processing

### Stream Pipeline

```python
import asyncio
from datetime import datetime, timedelta

class ContinuousIngestionPipeline:
    """Stream-based narrative ingestion and processing."""

    def __init__(self, sources: list, orchestrator: NarrativeOrchestrator):
        self.sources = sources
        self.orchestrator = orchestrator
        self.queue = asyncio.Queue(maxsize=1000)
        self.processing_rate = 0  # articles/minute

    async def run(self):
        """Main loop: collect → process → update."""
        # Start collection and processing concurrently
        collector_task = asyncio.create_task(self._collect_loop())
        processor_task = asyncio.create_task(self._process_loop())
        reporter_task = asyncio.create_task(self._report_loop())

        await asyncio.gather(collector_task, processor_task, reporter_task)

    async def _collect_loop(self):
        """Continuously collect from all sources."""
        while True:
            for source in self.sources:
                articles = await source.fetch_new()
                for article in articles:
                    await self.queue.put(article)
            await asyncio.sleep(300)  # Poll every 5 minutes

    async def _process_loop(self):
        """Process articles from the queue."""
        while True:
            article = await self.queue.get()
            try:
                result = await asyncio.to_thread(
                    self.orchestrator.process_article, article
                )
                self._update_metrics(result)
            except Exception as e:
                self._log_error(article["id"], str(e))
            finally:
                self.queue.task_done()

    async def _report_loop(self):
        """Periodic reporting of processing status."""
        while True:
            await asyncio.sleep(3600)  # Report hourly
            metrics = self._get_metrics()
            print(f"[{datetime.now()}] Processed {metrics['processed_today']} "
                  f"articles. Queue: {self.queue.qsize()}. "
                  f"Rate: {metrics['rate']}/min")
```

### Adaptive Scheduling

```python
class AdaptiveScheduler:
    """Adjusts processing frequency based on narrative velocity."""

    def __init__(self, base_interval=300):
        self.base_interval = base_interval
        self.narrative_velocity = 0.0

    def update_velocity(self, new_articles, existing_graph):
        """Measure narrative change velocity."""
        # If many new narratives are emerging, process more frequently
        if len(new_articles) > 100:
            self.narrative_velocity = min(1.0, self.narrative_velocity + 0.1)
        else:
            self.narrative_velocity = max(0.0, self.narrative_velocity - 0.05)

        # Dynamic interval: 5 min (calm) to 30 sec (active)
        interval = self.base_interval * (1 - self.narrative_velocity * 0.9)
        return max(30, interval)
```

---

## Narrative Emergence Detection

### Detecting Novel Narratives

```python
class EmergenceDetector:
    """Detect when new narratives emerge in the stream."""

    def __init__(self, vector_store, graph_db, threshold=0.85):
        self.vector_store = vector_store
        self.graph_db = graph_db
        self.threshold = threshold
        self.known_narratives = set()

    def detect(self, extraction: dict) -> dict:
        """Check if extracted content represents a novel narrative."""
        # 1. Embedding similarity to known narratives
        narrative_emb = extraction.get("embedding")
        if narrative_emb is None:
            return {"is_novel": False, "reason": "no_embedding"}

        similar = self.vector_store.search(narrative_emb, k=5)
        max_similarity = similar[0]["score"] if similar else 0

        # 2. Graph structure novelty
        causal_claims = extraction.get("causal_claims", [])
        graph_novelty = self._measure_graph_novelty(causal_claims)

        # 3. Combined novelty score
        novelty_score = 1 - (0.7 * max_similarity + 0.3 * (1 - graph_novelty))

        return {
            "is_novel": novelty_score > self.threshold,
            "novelty_score": novelty_score,
            "most_similar_narrative": similar[0]["id"] if similar else None,
            "similarity": max_similarity,
            "graph_novelty": graph_novelty,
        }

    def _measure_graph_novelty(self, causal_claims):
        """Measure how novel causal claims are relative to existing graph."""
        if not causal_claims or not self.graph_db:
            return 1.0

        novel_edges = 0
        for claim in causal_claims:
            if not self.graph_db.has_edge(claim.get("cause"), claim.get("effect")):
                novel_edges += 1

        return novel_edges / len(causal_claims)
```

### Narrative Lifecycle Tracking

```python
class NarrativeLifecycleTracker:
    """Track narratives through emergence → diffusion → peak → decay."""

    STAGES = ["emerging", "growing", "peaking", "declining", "fading"]

    def __init__(self, window_days=30):
        self.window = timedelta(days=window_days)
        self.history = []  # (timestamp, narrative_id, prevalence)

    def update(self, narrative_id: str, prevalence: float, timestamp: datetime):
        """Update narrative lifecycle stage."""
        self.history.append((timestamp, narrative_id, prevalence))
        self._prune_old()

        trajectory = self._get_trajectory(narrative_id)

        if len(trajectory) < 3:
            return "insufficient_data"

        recent = trajectory[-3:]
        prev_avg = sum(recent[:-1]) / len(recent[:-1])
        curr_val = recent[-1]

        if curr_val > prev_avg * 1.5 and prev_avg < 0.1:
            return "emerging"
        elif curr_val > prev_avg * 1.2:
            return "growing"
        elif curr_val > prev_avg * 0.8:
            return "peaking"
        elif curr_val < prev_avg * 0.7:
            return "declining"
        else:
            return "fading"

    def _get_trajectory(self, narrative_id: str) -> list[float]:
        return [
            p for t, n, p in self.history
            if n == narrative_id
            and t > datetime.now() - self.window
        ]
```

### Alerting System

```python
class NarrativeAlertingSystem:
    """Proactive alerts when notable narrative events occur."""

    def __init__(self, notifiers: list):
        self.notifiers = notifiers  # Email, Slack, Discord, etc.

    def check_alerts(self, emergence_results: list, lifecycle_updates: list):
        alerts = []

        for result in emergence_results:
            if result["novelty_score"] > 0.95:
                alerts.append(Alert(
                    level="critical",
                    type="novel_narrative",
                    message=f"Highly novel narrative detected "
                            f"(score: {result['novelty_score']:.2f})",
                    data=result,
                ))

        for update in lifecycle_updates:
            if update["stage"] == "emerging":
                alerts.append(Alert(
                    level="info",
                    type="narrative_emergence",
                    message=f"Narrative '{update['narrative_id']}' is emerging",
                    data=update,
                ))
            elif update["stage"] == "peaking" and update["prevalence"] > 0.5:
                alerts.append(Alert(
                    level="warning",
                    type="narrative_dominance",
                    message=f"Narrative '{update['narrative_id']}' "
                            f"now dominates discourse ({update['prevalence']:.1%})",
                    data=update,
                ))

        # Dispatch alerts
        for alert in alerts:
            for notifier in self.notifiers:
                notifier.send(alert)

        return alerts
```

---

## Autonomous Narrative Observatory

The highest ambition of Level 11: a fully autonomous system that discovers, tracks, and explains economic narratives without human operation.

### Observatory Architecture

```text
                      ┌─────────────────────────────────┐
                      │   NARRATIVE OBSERVATORY         │
                      │   Dashboard + API + Alerts      │
                      └──────────────┬──────────────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            │                        │                        │
            ▼                        ▼                        ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│   Ingestion Layer   │  │   Analysis Layer    │  │   Storage Layer     │
│                      │  │                      │  │                      │
│  - RSS feeds (50+)  │  │  - LLM extraction    │  │  - Neo4j graph DB   │
│  - News APIs        │  │  - Causal detection  │  │  - Qdrant vectors   │
│  - Social media     │  │  - Emergence detect  │  │  - PostgreSQL meta  │
│  - Policy speeches  │  │  - Graph analysis    │  │  - S3 raw storage   │
│  - Academic papers  │  │  - Trend forecasting  │  │                     │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

### Key Observatory Features

| Feature | Description | BENI Value |
|---------|-------------|------------|
| **Real-time dashboard** | Narrative prevalence, emergence, velocity | Monitor economic discourse as it evolves |
| **Automated weekly brief** | LLM-generated narrative landscape summary | Reduce manual analysis effort |
| **Anomaly detection** | Flag sudden narrative shifts | Early warning for economic sentiment changes |
| **Cross-platform tracking** | News vs. social vs. policy narratives | Understand narrative amplification |
| **Multi-language coordination** | Same narrative across XENI languages | Cross-linguistic narrative comparison |

### Weekly Brief Generation

```python
class AutomatedNarrativeBrief:
    """Generate weekly narrative landscape summaries."""

    def __init__(self, llm_client, graph_db):
        self.llm = llm_client
        self.graph = graph_db

    def generate_weekly_brief(self) -> str:
        """Produce human-readable weekly narrative summary."""
        # Collect weekly metrics
        metrics = {
            "emerging_narratives": self.graph.get_emerging(7),
            "dominant_narratives": self.graph.get_most_prevalent(7),
            "narrative_shifts": self.graph.get_largest_shifts(7),
            "actor_changes": self.graph.get_actor_centrality_changes(7),
        }

        # LLM synthesis
        prompt = f"""
        You are an economic narrative analyst. Based on this week's
        narrative landscape data, produce a concise brief covering:

        1. Top 3 emerging narratives
        2. How dominant narratives are changing
        3. Notable actor centrality shifts
        4. Cross-narrative connections to watch

        Data:
        {json.dumps(metrics, indent=2)}

        Format as a brief markdown report.
        """

        response = self.llm(prompt)
        return response
```

---

## Worked Example

### Scenario

An agentic narrative discovery system monitoring Bangla economic news for one week.

### Day 1: Setup

System begins monitoring 10 Bangla news sources. Ingests 500 articles/day.

### Day 2: Baseline

Extraction agent processes articles, builds initial narrative graph with 12 narrative clusters. The graph database contains 1,200 causal claims across 5 months of backfill data.

### Day 3: Novel Narrative Detected

```python
emergence_result = emergence_detector.detect(new_article_extraction)
# → {"is_novel": True, "novelty_score": 0.92,
#     "narrative": "Gas price hike is causing factory shutdowns",
#     "cause": "gas price increase",
#     "effect": "factory closures and job losses"}
```

**Alert:** "Highly novel narrative detected: 'Gas price hike causing factory shutdowns' (score: 0.92)"

The system escalates to human reviewer for validation.

### Day 4: Narrative Spreading

```python
lifecycle = lifecycle_tracker.update(
    "gas_hike_factory_shutdowns", prevalence=0.15, timestamp=now
)
# → "growing"

tracker = narrative_tracker.track_spread("gas_hike_factory_shutdowns")
# → Sources: Prothom Alo (started), now detected in:
#   - Daily Star (business section)
#   - Bangladesh Today (editorial)
#   - Social media amplification (2.5x)
```

### Day 5: Dominant Narrative

```python
lifecycle = lifecycle_tracker.update(
    "gas_hike_factory_shutdowns", prevalence=0.42, timestamp=now
)
# → "peaking"

alert_system.check_alerts(...)
# → Warning: "Narrative 'gas_hike_factory_shutdowns' dominates
#    discourse at 42% prevalence"
```

### Day 7: Weekly Brief Generated

```markdown
## Weekly Economic Narrative Brief (June 10–16, 2026)

### Emerging
1. **Gas price hike → factory shutdowns** (new, 42% prevalence by week's end)
   - Started in Prothom Alo business, spread to 4 other sources
   - Key actors: Govt (blamed), Factory owners (affected), Workers (victims)

### Dominant (Top 3)
1. **Inflation driven by energy costs** (58% prevalence, declining)
2. **Gas crisis impacting industry** (42%, rapidly growing) ⬆️
3. **Remittance growth slowing** (31%, stable)

### Actor Centrality Shift
- "Bangladesh Bank" centrality dropped from #2 to #5
- "Government" centrality rose from #3 to #1 (blame for gas crisis)
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Description |
|----------|-------------|
| **Continuous monitoring** | Real-time narrative tracking, not retrospective reports |
| **Emergence detection** | Catches new narratives as they form, not months later |
| **Autonomous operation** | Minimal human oversight needed after setup |
| **Multi-source integration** | News + social + policy in unified system |
| **Self-improving** | Feedback loops improve extraction over time |
| **Scalable** | Can monitor 10+ languages simultaneously (XENI target) |

### Weaknesses

| Weakness | Description | Mitigation |
|----------|-------------|------------|
| **Complexity** | Multi-agent systems are hard to build and debug | Start with simple 2-agent system |
| **Cost** | Continuous LLM usage at scale | Distillation, selective extraction |
| **Error propagation** | Early errors compound through the pipeline | Verification agent, human escalation |
| **Evaluation** | How to evaluate an autonomous discovery system | Regular human audit rounds |
| **Over-alerting** | System may flag noise as novelty | Adaptive thresholds, feedback |

---

## When to Use Level 11

| Scenario | Recommended | Alternative |
|----------|-------------|-------------|
| Real-time narrative monitoring | ✅ **Level 11** | — |
| Cross-platform narrative tracking | ✅ **Level 11** | — |
| Multi-language narrative observatory | ✅ **Level 11** | — |
| Historical research (static corpus) | ❌ Overkill | L3, L4, or L10 |
| Single-pipeline production deployment | ⚠️ Premature | L10 + L2 distillation first |
| Resource-constrained research | ❌ Too expensive | L10 on sample, L2 at scale |

---

## BENI Implementation Guide

### Phase 1: Simple Continuous Collection (4 weeks)

Extend BENI from batch to continuous:

```python
class BeniContinuousCollector:
    """Extend BENI with continuous news collection."""

    def __init__(self):
        self.sources = self._load_beni_sources()
        self.existing_ids = self._load_processed_ids()

    def _load_beni_sources(self):
        """Load BENI's existing news sources."""
        return [
            RSSSource("https://www.prothomalo.com/feed"),
            RSSSource("https://www.thedailystar.net/rss"),
            # Add remaining BENI sources
        ]

    def collect_new(self) -> list[dict]:
        """Fetch articles published since last check."""
        new_articles = []
        for source in self.sources:
            articles = source.fetch_since(self.last_check)
            for article in articles:
                if article["id"] not in self.existing_ids:
                    new_articles.append(article)
                    self.existing_ids.add(article["id"])
        return new_articles

    def run_daily(self):
        """Daily collection and processing."""
        articles = self.collect_new()
        print(f"Collected {len(articles)} new articles")

        # Process through existing BENI pipeline
        for batch in chunks(articles, 50):
            beni_pipeline.process_batch(batch)

        # Update indices
        beni_index_builder.update(articles)
```

### Phase 2: Narrative Graph from LLM Output (2 weeks)

Build on existing infrastructure:

```python
class BeniAgenticExtension:
    """Extend BENI with agentic discovery capabilities."""

    def __init__(self, llm_annotator, graph_db):
        self.annotator = llm_annotator  # Reuse existing BENI annotator
        self.graph = graph_db
        self.detector = EmergenceDetector(...)

    def process_article(self, article: dict) -> dict:
        # Step 1: Use existing BENI annotation
        annotation = self.annotator.annotate(
            article["text"], article["id"]
        )

        # Step 2: Add to narrative graph
        self.graph.add_annotation(
            article["id"],
            annotation["economic_topic"],
            annotation["narrative_force"],
            annotation["valuation_target"],
        )

        # Step 3: Detect emergence
        emergence = self.detector.detect({
            "topic": annotation["economic_topic"],
            "force": annotation["narrative_force"],
            "target": annotation["valuation_target"],
        })

        return {
            "article_id": article["id"],
            "annotation": annotation,
            "emergence": emergence,
        }
```

### Phase 3: Full Observatory (Q3 2027)

```text
BENI 2.0 → BENI 3.0 (Agentic) Roadmap:

Phase 1 (Q3 2026): Continuous collection + daily processing
Phase 2 (Q4 2026): Narrative graph with emergence detection
Phase 3 (Q1 2027): Cross-platform integration (social media)
Phase 4 (Q2 2027): Multi-language coordination (XENI agents)
Phase 5 (H2 2027): Autonomous narrative observatory
```

### Infrastructure Requirements

```python
# Core dependencies
pip install asyncio aiohttp feedparser  # Continuous ingestion
pip install networkx neo4j py2neo       # Graph storage
pip install qdrant-client               # Vector storage
pip install fastapi uvicorn             # Observatory API
pip install celery redis                # Task queue
```

### XENI Multi-Language Coordination

```python
class XeniNarrativeCoordinator:
    """Coordinate narrative discovery across XENI pipelines."""

    def __init__(self):
        self.pipelines = {
            "BENI": BeniAgenticExtension(...),
            # Future: AENI, NENI, HENI, ...
        }

    def cross_language_narrative_detection(self):
        """Detect same narrative across multiple languages."""
        narratives = {}
        for lang, pipeline in self.pipelines.items():
            narratives[lang] = pipeline.get_dominant_narratives(7)

        # Cross-language comparison
        for narrative_en in narratives.get("BENI", []):
            # Check for similar narratives in other languages
            for lang, lang_narratives in narratives.items():
                if lang == "BENI":
                    continue
                similar = self._find_similar(
                    narrative_en, lang_narratives
                )
                if similar:
                    print(f"Narrative '{narrative_en['id']}' "
                          f"also found in {lang}: {similar['id']}")

    def _find_similar(self, narrative_a, narratives_b):
        """Find similar narratives across languages using embeddings."""
        emb_a = narrative_a["embedding"]
        for nb in narratives_b:
            similarity = cosine_similarity(emb_a, nb["embedding"])
            if similarity > 0.85:
                return nb
        return None
```

---

## Research Frontier

### Current Challenges (2026)

1. **Evaluation** — How do we evaluate an autonomous system that discovers things we don't know?
2. **Cost sustainability** — Continuous LLM usage at multi-language scale
3. **Feedback loops** — System discovers its own biases, which amplify
4. **Human-in-the-loop design** — When and how to escalate to humans
5. **Cross-language coordination** — Same narrative, different language, different framing

### Open Questions for BENI

1. **Lead time** — How much earlier does an agentic system detect narrative shifts compared to batch processing?
2. **Novelty calibration** — What fraction of "novel narratives" are actually meaningful vs. noise?
3. **Cost-benefit** — Does continuous monitoring provide enough additional value over monthly batch indices?
4. **Social media integration** — Can BENI's newspaper-trained system handle social media noise?

### Future Directions

- **Narrative forecasting** — Agentic systems that predict narrative trajectories using temporal graph neural networks
- **Causal intervention simulation** — "What would happen to narrative X if event Y occurred?"
- **Self-improving schemas** — Agents that autonomously update their extraction schema as new narrative patterns emerge
- **Federated narrative observatories** — Independent per-language observatories that share cross-language insights

---

## References

### Agentic Systems and Multi-Agent AI

- Tian, Q. et al. (2026). "Narrative Knowledge Weaver." *ICLR 2026*.
  — Multi-agent framework for narrative extraction: adaptive schema induction, reflection-augmented extraction, normalization-before-merge.

- Park, J. S. et al. (2023). "Generative Agents: Interactive Simulacra of Human Behavior." *UIST 2023*. arXiv: `2304.03442`.
  — Foundational paper on autonomous LLM agents with memory, reflection, and planning.

- Xi, Z. et al. (2025). "The Rise and Potential of LLM-Based Agents: A Survey." *ACM Computing Surveys*.
  — Comprehensive survey of LLM agent architectures relevant to narrative discovery.

### Narrative Discovery and Tracking

- Salloum, C. et al. (2025). "Modeling cross-platform narrative templates: a temporal knowledge graph approach." *Social Network Analysis and Mining*, 15: 14.
  — Temporal KG approach fundamental to cross-platform narrative tracking.

- Norambuena, B. K., Mitra, T., & North, C. (2023). "A Survey on Event-based News Narrative Extraction." *ACM Computing Surveys*, 55(14s): 1–39.
  — Three resolution levels for narrative tracking systems.

### Continuous Systems

- Lazer, D. et al. (2009). "Computational Social Science." *Science*, 323(5915): 721–723.
  — The paradigm that motivates continuous social science measurement.

### BENI-Specific

- Nabil, A. N. (2026). "BENI Roadmap." `pipelines/BENI/management/BENI_ROADMAP.md`.
  — Current plans for BENI 2.0 (L3, L4, L7) and 3.0 (agentic extensions).

- Nabil, A. N. (2026). "BENI Global 10: A Multilingual Economic News Dataset for Narrative Measurement." arXiv: `2606.10225`.
  — Multi-language dataset enabling cross-lingual agentic discovery.

### See Also

- Level 4: [Embedding-Based Discovery](L04_embedding_based_discovery.md) — Foundation for narrative clustering
- Level 8: [Narrative Networks and Graphs](L08_narrative_networks_graphs.md) — Graph infrastructure for observatory
- Level 9: [RELATIO-Style Extraction](L09_relatio_style_extraction.md) — Triple extraction at scale
- Level 10: [LLM-Based Extraction](L10_llm_based_extraction.md) — LLM extraction engine for agents

---

**Up:** [Methodologies Index](INDEX.md) | **Main:** [Narrative Extraction Methodologies](../NARRATIVE_EXTRACTION_METHODOLOGIES.md)
