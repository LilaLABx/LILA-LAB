"""LLM annotation orchestration and inter-annotator agreement.

This module provides two annotation workflows:

1. **Pilot annotation** (``run_pilot_annotation``):
   Sample N articles, annotate with multiple LLMs, measure agreement.

2. **Batch annotation** (``run_batch_annotation``):
   Full-corpus annotation with checkpointing and resume support.

Both workflows use ``shared.llm.clients`` for API calls, which reads
credentials from environment variables (``ANTHROPIC_API_KEY``,
``OPENAI_API_KEY``, ``GEMINI_API_KEY``).

Usage::

    from shared.analysis.annotator import run_pilot_annotation, compute_agreement

    # Phase 1: pilot
    results = run_pilot_annotation(
        df=corpus,
        schema_path="pipelines/BENI/annotation/schemas/economic.json",
        sample_size=200,
        providers=["claude", "gpt4o"],
    )
    agreement = compute_agreement(results)

TODO:
    - Implement prompt templating with schema injection
    - Add self-consistency (multiple runs per article per LLM)
    - Add confidence-weighted consensus across LLMs
    - Handle rate limiting with exponential backoff
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# ═════════════════════════════════════════════════════════════════════
#  Phase 1: Pilot Annotation
# ═════════════════════════════════════════════════════════════════════


def run_pilot_annotation(
    df: "pd.DataFrame",  # noqa: F821 — pandas type hint
    schema_path: str | Path,
    output_dir: str | Path,
    sample_size: int = 200,
    providers: list[dict[str, Any]] | None = None,
    seed: int = 42,
    strategy: str = "stratified",
    stratify_by: str | None = "category_harmonised",
) -> dict[str, Any]:
    """Sample articles, run multi-LLM annotation, measure agreement.

    This is the primary entry point for Phase 1 of the annotation pipeline.
    It performs the following steps:

    1. Load the annotation schema from ``schema_path``
    2. Sample ``sample_size`` articles from ``df`` (stratified or random)
    3. For each article, call each LLM provider with the schema prompt
    4. Parse structured JSON responses from each LLM
    5. Compute inter-annotator agreement (Cohen's κ, Fleiss' κ)
    6. Report per-field reliability metrics
    7. Write results to ``output_dir``

    Parameters
    ----------
    df:
        Corpus DataFrame. Must contain columns matching the config's
        fieldnames (``text_clean`` or ``text`` for article content).
    schema_path:
        Path to annotation schema JSON (see ``annotation/schemas/economic.json``
        for the canonical format).
    output_dir:
        Directory to write results (agreement report, annotated sample,
        per-field reliability).
    sample_size:
        Number of articles to sample for the pilot. Start with 50 to
        validate the prompt, then scale to 200-500 for reliable agreement
        estimates.
    providers:
        List of LLM provider configs. Each entry should have:
        ``{"name": str, "model": str, "max_tokens": int, "temperature": float}``.
        Default uses providers from pipeline config if None.
    seed:
        Random seed for reproducible sampling.
    strategy:
        Sampling strategy — ``"random"`` or ``"stratified"``.
    stratify_by:
        Column to stratify by (only used if strategy is ``"stratified"``).

    Returns
    -------
    dict
        Keys:
        - ``"sample_path"`` — path to annotated sample JSON
        - ``"agreement"`` — agreement metrics per field
        - ``"field_reliability"`` — per-field reliability breakdown
        - ``"summary"`` — high-level summary statistics

    TODO
    ----
    - Implement the LLM call loop with ``shared.llm.clients``
    - Parse structured JSON from LLM responses with schema validation
    - Handle partial failures (one LLM fails but others succeed)
    - Compute Cohen's κ per field for each LLM pair
    - Compute Fleiss' κ for multi-LLM agreement
    - Flag fields below ``min_agreement`` threshold
    """
    from pathlib import Path

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # ── 1. Load schema ─────────────────────────────────────────
    schema_path = Path(schema_path)
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    logger.info("Schema: %s v%s (%d fields)", schema["domain"], schema["version"], len(schema["fields"]))

    # ── 2. Sample articles ─────────────────────────────────────
    # TODO: replace with actual sampling logic
    #   if strategy == "stratified":
    #       sample = df.groupby(stratify_by, group_keys=False).apply(
    #           lambda g: g.sample(min(len(g), sample_size // df[stratify_by].nunique()), random_state=seed)
    #       )
    #   else:
    #       sample = df.sample(n=min(sample_size, len(df)), random_state=seed)
    logger.info("Sampling %d articles (strategy=%s, seed=%d)", sample_size, strategy, seed)
    sample = df.sample(n=min(sample_size, len(df)), random_state=seed)

    # ── 3. Run LLM annotation ──────────────────────────────────
    # TODO: for each article, for each provider:
    #   1. Build prompt from schema + article text
    #   2. Call LLM API via shared.llm.clients.call_anthropic / call_openai
    #   3. Parse JSON response
    #   4. Validate against schema (field names, value ranges)
    #   5. Store in annotations list
    #
    # Example:
    #   from shared.llm.clients import call_anthropic, call_openai
    #   system_prompt = f"You are annotating articles for {schema['domain']} narratives..."
    #   user_prompt = f"Article: {row[text_col]}\n\nAnnotate with: {json.dumps(schema)}"
    #   response = call_anthropic(model="claude-3-5-sonnet-20241022", system=system_prompt, messages=[{"role": "user", "content": user_prompt}])
    #   parsed = parse_llm_response(response)
    logger.info("Annotating %d articles with %d provider(s)", len(sample), len(providers) if providers else 2)
    annotations = []  # TODO: populate

    # ── 4. Compute agreement ───────────────────────────────────
    agreement = compute_agreement(annotations)
    field_reliability = field_level_reliability(annotations)

    # ── 5. Write outputs ───────────────────────────────────────
    # TODO: write annotated_sample.json, agreement_report.json, reliability_report.json
    summary = {
        "n_articles": len(sample),
        "n_articles_with_annotations": len(annotations),
        "n_providers": len(providers) if providers else 0,
        "overall_agreement": agreement.get("overall", None),
        "fields_below_threshold": [
            f for f, m in field_reliability.items()
            if m.get("cohens_kappa", 1.0) < 0.6  # TODO: make threshold configurable
        ],
    }
    logger.info("Pilot complete — %d articles annotated", len(sample))
    logger.info("  Overall agreement: %s", summary["overall_agreement"])
    logger.info("  Fields below threshold: %s", summary["fields_below_threshold"])

    return {
        "sample_path": str(out / "annotated_sample.json"),
        "agreement": agreement,
        "field_reliability": field_reliability,
        "summary": summary,
    }


# ═════════════════════════════════════════════════════════════════════
#  Agreement Metrics
# ═════════════════════════════════════════════════════════════════════


def compute_agreement(
    annotations: list[dict[str, Any]],
    methods: list[str] | None = None,
) -> dict[str, Any]:
    """Compute inter-annotator agreement across multiple LLMs.

    Supports the following methods:
    - **Cohen's κ**: pairwise agreement between two annotators (corrected
      for chance). Computed for every LLM pair.
    - **Fleiss' κ**: multi-annotator agreement (generalization of Scott's π).
      Computed across all LLMs simultaneously.
    - **Percentage agreement**: simple observed agreement (not chance-corrected).

    Parameters
    ----------
    annotations:
        List of annotation dicts. Each dict should have at least:
        ``{"article_id": str, "annotator": str, "fields": {field_name: value}}``.
    methods:
        List of agreement methods to compute. Defaults to
        ``["cohens_kappa", "fleiss_kappa"]``.

    Returns
    -------
    dict
        Keys:
        - ``"overall"`` — overall agreement across all fields
        - ``"per_field"`` — dict of ``{field_name: {method: value}}``
        - ``"pairwise"`` — dict of ``{(annotator_a, annotator_b): {field: kappa}}``

    TODO
    ----
    - Implement Cohen's κ using ``sklearn.metrics.cohen_kappa_score``
    - Implement Fleiss' κ (not in sklearn — use ``shared.stats.agreement``)
    - Handle ordinal vs nominal fields differently (linear vs quadratic weights)
    - Compute per-field agreement separately (some fields may be easier than others)
    """
    if methods is None:
        methods = ["cohens_kappa", "fleiss_kappa"]

    if not annotations:
        logger.warning("No annotations to compute agreement on")
        return {"overall": None, "per_field": {}, "pairwise": {}}

    # TODO: implement actual agreement computation
    #   1. Group annotations by article_id
    #   2. For each field, build the annotation matrix (articles × annotators)
    #   3. Compute pairwise Cohen's κ for each annotator pair
    #   4. Compute Fleiss' κ across all annotators
    #   5. Aggregate into per-field and overall metrics
    logger.info("Computing agreement: %s", methods)

    return {
        "overall": None,
        "per_field": {},
        "pairwise": {},
        "methods_used": methods,
    }


def field_level_reliability(
    annotations: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Compute per-field reliability metrics.

    For each field in the schema, computes:
    - **Cohen's κ**: pairwise agreement for that field
    - **Observed agreement**: simple percentage agreement
    - **Base rate**: distribution of values (for assessing class imbalance)
    - **N**: number of non-missing annotations

    Parameters
    ----------
    annotations:
        Same format as ``compute_agreement``.

    Returns
    -------
    dict
        ``{field_name: {"cohens_kappa": float, "observed_agreement": float,
        "base_rate": dict, "n": int}}``

    TODO
    ----
    - Separate reliability by field type (binary fields easier than multiclass)
    - Flag fields where base rate is extremely skewed (>90% one class)
    - Flag fields where N is too small for reliable estimates
    """
    # TODO: implement
    logger.info("Computing field-level reliability")
    return {}


# ═════════════════════════════════════════════════════════════════════
#  Phase 2: Batch Annotation
# ═════════════════════════════════════════════════════════════════════


def run_batch_annotation(
    df: "pd.DataFrame",  # noqa: F821
    schema_path: str | Path,
    output_dir: str | Path,
    llm_config: dict[str, Any] | None = None,
    checkpoint_path: str | Path | None = None,
    checkpoint_every: int = 500,
    batch_size: int = 100,
    max_articles: int | None = None,
    n_workers: int = 1,
    consensus: str = "majority_vote",
) -> dict[str, Any]:
    """Annotate the full corpus in batches with checkpoint resume.

    Processes articles in batches, calling the LLM ensemble on each batch.
    Supports resuming from a checkpoint if the process is interrupted.

    Parameters
    ----------
    df:
        Full corpus DataFrame.
    schema_path:
        Path to annotation schema JSON.
    output_dir:
        Directory for output files (predictions, consensus, logs).
    llm_config:
        LLM configuration dict. If None, reads from pipeline config.
        Expected keys: ``providers``, ``n_runs``, ``max_retries``.
    checkpoint_path:
        Path to Parquet checkpoint file. If it exists, resumes from it.
    checkpoint_every:
        Save checkpoint every N articles.
    batch_size:
        Number of articles per batch (per API call).
    max_articles:
        Maximum articles to annotate. ``None`` means full corpus.
    n_workers:
        Number of parallel workers. Use 1 to avoid rate limits.
    consensus:
        Strategy to combine multiple LLM predictions.
        - ``"majority_vote"``: most common value wins
        - ``"confidence_weighted"``: weight by LLM confidence
        - ``"llm_only"``: use only the best-performing LLM from Phase 1

    Returns
    -------
    dict
        Keys:
        - ``"n_annotated"`` — total articles annotated
        - ``"predictions_path"`` — path to full predictions Parquet
        - ``"consensus_path"`` — path to consensus labels Parquet
        - ``"checkpoint_path"`` — path to checkpoint (for resume)

    TODO
    ----
    - Implement batched API calls with ``concurrent.futures.ThreadPoolExecutor``
    - Add checkpoint save/load with ``pd.DataFrame.to_parquet``
    - Handle API errors gracefully (retry, skip, log)
    - Implement consensus strategies
    - Track cost per article per provider
    """
    from pathlib import Path

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    total = min(max_articles, len(df)) if max_articles else len(df)
    logger.info("Batch annotating %d articles (batch_size=%d, n_workers=%d)", total, batch_size, n_workers)

    # TODO: implement batch annotation loop
    #   1. Load checkpoint if exists (skip already-annotated articles)
    #   2. Iterate through articles in batches
    #   3. For each batch, call LLM ensemble
    #   4. Save checkpoint every checkpoint_every articles
    #   5. On completion, save full predictions and consensus labels
    #   6. Log summary statistics (cost, throughput, error rate)

    logger.info("Batch annotation — not yet implemented")
    return {
        "n_annotated": 0,
        "predictions_path": str(out / "full_predictions.parquet"),
        "consensus_path": str(out / "consensus_labels.parquet"),
        "checkpoint_path": str(out / "checkpoint.parquet") if not checkpoint_path else str(checkpoint_path),
    }
