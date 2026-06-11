"""Annotation schema coverage validator.

Before running expensive LLM annotation, validate that your annotation
schema's categories actually appear in the corpus.  Uses keyword matching
to estimate whether each schema field has sufficient coverage.

This is the gate that prevents the single most expensive mistake in the
XENI pipeline: annotating thousands of articles with a schema that has
dead fields.

Typical usage::

    from shared.analysis.schema_validator import validate_schema_coverage

    result = validate_schema_coverage(
        df, text_column="content",
        schema_path="pipelines/BENI/annotation/schemas/economic.json",
    )
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

import pandas as pd

from ..io import write_json

logger = logging.getLogger(__name__)

# ── Default keyword mappings per schema field ─────────────────────────

# Fallback keywords when a schema field has no explicit keyword hints.
# These are deliberately generic — per-language overrides go in config.
DEFAULT_FIELD_KEYWORDS: dict[str, list[str]] = {
    "economic_relevance": [
        "economy", "economic", "market", "price", "inflation", "trade",
        "bank", "finance", "budget", "tax", "revenue", "currency",
        "economy", "money", "business", "investment", "loan",
    ],
    "economic_topic:inflation": ["inflation", "price", "cpi", "cost of living", "inflation rate"],
    "economic_topic:exchange_rate": ["exchange rate", "forex", "currency", "dollar", "taka", "fx"],
    "economic_topic:reserves": ["reserve", "foreign reserve", "forex reserve"],
    "economic_topic:banking": ["bank", "banking", "loan", "interest rate", "credit"],
    "economic_topic:fiscal_policy": ["budget", "fiscal", "tax", "revenue", "spending", "deficit"],
    "economic_topic:trade": ["trade", "export", "import", "tariff", "customs"],
    "economic_topic:employment": ["employment", "unemployment", "job", "labour", "labor"],
    "economic_topic:growth_investment": ["growth", "gdp", "investment", "development", "infrastructure"],
    "narrative_force:crisis": ["crisis", "crash", "collapse", "emergency", "turmoil"],
    "narrative_force:burden": ["burden", "pressure", "strain", "struggle", "hardship"],
    "narrative_force:blame": ["blame", "failure", "mismanagement", "corruption", "scandal"],
    "narrative_force:reform": ["reform", "policy change", "new law", "regulation", "initiative"],
    "narrative_force:stability": ["stable", "stability", "steady", "balanced", "sustainable"],
    "narrative_force:uncertainty": ["uncertainty", "unpredictable", "volatile", "risk", "instability"],
    "narrative_force:resilience": ["resilient", "resilience", "recovery", "rebound", "rebuilding"],
    "valuation_target:government": ["government", "ministry", "authority", "official"],
    "valuation_target:central_bank": ["central bank", "bangladesh bank", "monetary authority", "fed", "reserve bank"],
    "valuation_target:businesses": ["business", "company", "corporation", "industry", "sector", "firm"],
    "valuation_target:market_actors": ["investor", "trader", "market", "shareholder", "speculator"],
    "valuation_target:households": ["household", "family", "consumer", "citizen", "people", "public"],
    "sentiment:negative": ["crisis", "decline", "loss", "damage", "threat", "risk", "worry"],
    "sentiment:positive": ["growth", "recovery", "improvement", "gain", "success", "opportunity"],
    "health_relevance": ["health", "hospital", "disease", "patient", "medical", "treatment", "vaccine"],
    "health_topic:public_health": ["public health", "outbreak", "epidemic", "pandemic", "hygiene", "sanitation"],
    "health_topic:healthcare_system": ["healthcare", "hospital", "clinic", "health service", "health insurance"],
}


# ── Core validation ───────────────────────────────────────────────────


def validate_schema_coverage(
    df: pd.DataFrame,
    schema_path: str | Path,
    text_column: str = "text",
    *,
    sample_size: int = 5_000,
    min_coverage: float = 0.05,
    keyword_overrides: dict[str, list[str]] | None = None,
    case_insensitive: bool = True,
) -> dict[str, Any]:
    """Test annotation schema coverage against actual corpus text.

    For each field/option in the schema, searches for indicative keywords
    in a random sample of articles and reports the match rate.

    Parameters
    ----------
    df:
        Corpus DataFrame.
    schema_path:
        Path to annotation schema JSON.
    text_column:
        Column containing article text.
    sample_size:
        Number of articles to sample (default 5,000).
    min_coverage:
        Minimum fraction of articles that should match a field
        before a warning is raised (default 0.05 = 5%).
    keyword_overrides:
        Per-field keyword lists to override defaults.  Key format:
        ``field_name:option_value`` or just ``field_name``.
    case_insensitive:
        Whether keyword matching is case-insensitive.

    Returns
    -------
    dict
        Keys: ``schema``, ``per_field``, ``overall_coverage``,
        ``dead_fields``, ``passes_threshold``.
    """
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    fields = schema.get("fields", [])
    domain = schema.get("domain", "unknown")

    # Sample
    if len(df) > sample_size:
        df_sample = df.sample(n=sample_size, random_state=42)
    else:
        df_sample = df

    flags = re.IGNORECASE if case_insensitive else 0
    kw_overrides = keyword_overrides or {}

    per_field: dict[str, Any] = {}
    dead_fields: list[str] = []
    all_matched: set[int] = set()

    for field in fields:
        field_name = field["name"]
        field_type = field.get("type", "binary")
        values = field.get("values", [])
        conditional = field.get("conditional_on", "")

        field_result: dict[str, Any] = {
            "type": field_type,
            "conditional_on": conditional,
            "n_values": len(values),
        }

        # Collect keywords for this field
        field_kw = kw_overrides.get(field_name) or DEFAULT_FIELD_KEYWORDS.get(field_name, [])

        # Per-value keywords
        per_value: dict[str, dict] = {}
        total_matches_field = 0

        for val in values:
            val_key = f"{field_name}:{val}"
            kw = kw_overrides.get(val_key) or DEFAULT_FIELD_KEYWORDS.get(val_key, [])

            if not kw:
                # Auto-generate from value name
                kw = [val.lower().replace("_", " ")]

            if not kw or kw == [val.lower().replace("_", " ")]:
                per_value[val] = {"match_count": 0, "match_pct": 0.0, "keywords_used": kw}
                continue

            pattern = re.compile("|".join(re.escape(k) for k in kw), flags)
            matches = df_sample[text_column].apply(
                lambda t: bool(isinstance(t, str) and pattern.search(t))
            )
            match_count = int(matches.sum())
            match_pct = round(match_count / len(df_sample) * 100, 2)
            total_matches_field += match_count

            per_value[val] = {
                "match_count": match_count,
                "match_pct": match_pct,
                "keywords_used": kw[:5],
            }

        field_result["per_value"] = per_value
        field_result["any_match_pct"] = round(
            min(total_matches_field / len(df_sample) * 100, 100.0), 2
        )
        field_result["passes_min_coverage"] = field_result["any_match_pct"] >= (min_coverage * 100)

        if not field_result["passes_min_coverage"] and field_type not in ("flag",):
            dead_fields.append(field_name)

        # Track which rows matched ANY field
        if field_result["any_match_pct"] > 0:
            pattern_all = re.compile(
                "|".join(
                    re.escape(k)
                    for val_d in per_value.values()
                    for k in val_d.get("keywords_used", [])
                ),
                flags,
            )
            matched_idx = df_sample[text_column].apply(
                lambda t: bool(isinstance(t, str) and pattern_all.search(t))
            )
            all_matched.update(df_sample.index[matched_idx])

        per_field[field_name] = field_result

    n_matched_any = len(all_matched)
    overall_coverage = round(n_matched_any / len(df_sample) * 100, 2) if len(df_sample) else 0.0

    result: dict[str, Any] = {
        "schema": {"domain": domain, "version": schema.get("version"), "path": str(schema_path)},
        "n_fields": len(fields),
        "sample_size": len(df_sample),
        "overall_coverage": overall_coverage,
        "passes_threshold": overall_coverage >= (min_coverage * 100),
        "dead_fields": dead_fields,
        "n_dead_fields": len(dead_fields),
        "per_field": per_field,
        "min_coverage_threshold": min_coverage,
    }

    if dead_fields:
        logger.warning("DEAD FIELDS: %d fields below %.0f%% coverage — %s",
                       len(dead_fields), min_coverage * 100, dead_fields)
    logger.info("Schema coverage: %.1f%% overall, %d/%d fields pass",
                overall_coverage, sum(1 for f in per_field.values()
                                      if f.get("passes_min_coverage")), len(fields))
    return result


def run_schema_validation(
    df: pd.DataFrame,
    output_dir: str | Path,
    schema_path: str | Path,
    text_column: str = "text",
    **kwargs: Any,
) -> dict[str, Any]:
    """Run schema validation and write results to *output_dir*.

    Returns the validation result dict.
    """
    from pathlib import Path

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    result = validate_schema_coverage(df, schema_path, text_column=text_column, **kwargs)
    write_json(out / "schema_coverage.json", result)

    # Report
    domain = result["schema"]["domain"]
    lines = [
        "═" * 60,
        f"SCHEMA VALIDATION: {domain.upper()}",
        "═" * 60,
        f"  Schema:       {result['schema']['path']}",
        f"  Fields:       {result['n_fields']}",
        f"  Sample:       {result['sample_size']} articles",
        f"  Coverage:     {result['overall_coverage']}% {'✅' if result['passes_threshold'] else '⚠️'}",
    ]
    if result["dead_fields"]:
        lines.append(f"  Dead fields:  {', '.join(result['dead_fields'])} ⚠️")
    lines.append("")
    for field_name, fdata in result["per_field"].items():
        status = "✅" if fdata.get("passes_min_coverage") else "⚠️"
        lines.append(f"  {field_name:<30} {status} {fdata.get('any_match_pct', 0)}%")
        for val, vdata in fdata.get("per_value", {}).items():
            if vdata.get("match_count", 0) > 0:
                lines.append(f"    {val:<28} {vdata['match_pct']}%  (n={vdata['match_count']})")
    lines.append("═" * 60)
    out.joinpath("schema_coverage_report.md").write_text("\n".join(lines) + "\n")

    logger.info("Schema validation written to %s", out)
    return result
