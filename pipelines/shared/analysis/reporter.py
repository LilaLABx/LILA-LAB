"""Synthesis report generator — combines profile, vocabulary, temporal,
and schema validation results into a single Markdown diagnostic report.

Typical usage::

    from shared.analysis.reporter import generate_report

    report_path = generate_report(
        language="BENI",
        output_dir="pipelines/BENI/exploration/outputs/05_diagnostic",
        phases={
            "profile": "pipelines/BENI/exploration/outputs/01_profile/profile_summary.json",
            "vocabulary": "pipelines/BENI/exploration/outputs/02_vocabulary/vocabulary_summary.json",
            "temporal": "pipelines/BENI/exploration/outputs/03_temporal/temporal_diagnostics.json",
            "schema": "pipelines/BENI/exploration/outputs/04_schema/schema_coverage.json",
        },
    )
"""

from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _load_json(path: str | Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    p = Path(path)
    if not p.exists():
        logger.warning("Report input not found: %s", p)
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _coverage_badge(pct: float | None) -> str:
    if pct is None:
        return "⬜"
    if pct >= 80:
        return "✅"
    if pct >= 50:
        return "🟡"
    return "🔴"


def _status_badge(ok: bool | None) -> str:
    if ok is None:
        return "⬜"
    return "✅" if ok else "🔴"


# ── Report generation ─────────────────────────────────────────────────


def generate_report(
    language: str,
    output_dir: str | Path,
    phases: dict[str, str | Path | None],
    *,
    registry_entry: dict[str, Any] | None = None,
) -> Path:
    """Generate a synthesis diagnostics report.

    Parameters
    ----------
    language:
        Pipeline name (e.g. ``"BENI"``).
    output_dir:
        Directory to write ``diagnostic_report.md``.
    phases:
        Mapping of phase name to JSON output path (or ``None``).
        Expected keys: ``profile``, ``vocabulary``, ``temporal``, ``schema``.
    registry_entry:
        Optional dict from ``registry/languages.json`` for cross-reference.

    Returns
    -------
    Path
        Path to the generated report.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    profile = _load_json(phases.get("profile"))
    vocab = _load_json(phases.get("vocabulary"))
    temporal = _load_json(phases.get("temporal"))
    schema = _load_json(phases.get("schema"))

    lines: list[str] = []

    # ── Header ──────────────────────────────────────────────────────
    lines.append(f"# {language} — Dataset Diagnostic Report")
    lines.append("")
    lines.append(f"**Generated:** {date.today().isoformat()}")
    if registry_entry:
        r = registry_entry
        status_icon = {"active": "✅", "bootstrapped": "🔜", "planned": "📋"}.get(
            r.get("pipeline_status", ""), "⬜"
        )
        lines.append(f"**Pipeline status:** {status_icon} {r.get('pipeline_status', 'unknown')}")
        lines.append(f"**Language:** {r.get('name', '')} ({r.get('native', '')})")
        lines.append(f"**Speakers:** {r.get('speakers_million', '?')}M")
    lines.append("")

    # ── Phase summary table ─────────────────────────────────────────
    lines.append("## Phase Summary")
    lines.append("")
    lines.append("| Phase | Status | Key Metric |")
    lines.append("|-------|--------|------------|")

    phase_labels = {
        "profile": "Corpus Profile",
        "vocabulary": "Vocabulary Analysis",
        "temporal": "Temporal Diagnostics",
        "schema": "Schema Validation",
    }

    for phase_key, label in phase_labels.items():
        data = _load_json(phases.get(phase_key))
        if data is None:
            lines.append(f"| {label} | ⬜ Not run | — |")
        elif "error" in data:
            lines.append(f"| {label} | 🔴 Error | {data['error']} |")
        else:
            metric = _phase_metric(phase_key, data)
            lines.append(f"| {label} | ✅ Complete | {metric} |")

    lines.append("")

    # ── 1. Corpus profile ───────────────────────────────────────────
    if profile:
        lines.append("## 1. Corpus Profile")
        lines.append("")
        lines.append(f"- **Total articles:** {profile.get('n_articles', '?'):,}")
        dr = profile.get("date_range", {})
        if dr:
            lines.append(
                f"- **Date range:** {dr.get('start', '?')} → {dr.get('end', '?')} ({dr.get('n_days', '?')} days)"
            )
        lines.append(f"- **Sources:** {profile.get('n_sources', '?')}")
        lines.append(f"- **Categories:** {profile.get('n_categories', '?')}")

        tl = profile.get("text_length", {})
        if tl:
            lines.append(
                f"- **Words/article:** mean={tl.get('mean_words')}, median={tl.get('median_words')}"
            )

        q = profile.get("quality", {})
        if q:
            lines.append(f"- **Empty texts:** {q.get('empty_texts')} ({q.get('empty_texts_pct')}%)")
            if q.get("missing_dates") is not None:
                lines.append(
                    f"- **Missing dates:** {q.get('missing_dates')} ({q.get('missing_dates_pct')}%)"
                )

        dc = profile.get("date_coverage", {})
        if dc:
            lines.append(
                f"- **Monthly coverage:** {dc.get('n_months', '?')}/{dc.get('n_months', '?') + dc.get('n_gaps', 0)} months"
            )
            if dc.get("n_gaps", 0) > 0:
                lines.append(f"- **Coverage gaps:** {dc['n_gaps']} gaps detected")

        # Source breakdown (top 5)
        sources = profile.get("by_source", [])
        if sources:
            lines.append("")
            lines.append("**Top sources:**")
            for s in sources[:5]:
                lines.append(f"  - {s['source']}: {s['n_articles']:,} articles")

        # Category breakdown (top 5)
        cats = profile.get("by_category", [])
        if cats:
            lines.append("")
            lines.append("**Top categories:**")
            for c in cats[:5]:
                lines.append(f"  - {c['category']}: {c['n_articles']:,} articles")
        lines.append("")

    # ── 2. Vocabulary analysis ──────────────────────────────────────
    if vocab:
        lines.append("## 2. Vocabulary Analysis")
        lines.append("")
        lines.append(f"- **Tokens:** {vocab.get('tokens', '?'):,}")
        lines.append(f"- **Types:** {vocab.get('types', '?'):,}")
        lines.append(f"- **TTR (type-token ratio):** {vocab.get('ttr', '?')}")
        lines.append(
            f"- **Hapax legomena:** {vocab.get('hapax_count', '?')} ({vocab.get('hapax_percentage', '?')}% of types)"
        )

        top_words = vocab.get("top_n_words", [])
        if top_words:
            lines.append("")
            lines.append("**Top words:**")
            for w in top_words[:20]:
                lines.append(f"  - {w['word']}: {w['frequency']:,} ({w['proportion']:.2%})")

        per_cat = vocab.get("per_category", {})
        if per_cat:
            lines.append("")
            lines.append("**Per-category vocabulary richness:**")
            lines.append("")
            lines.append("| Category | Types | TTR | Top word |")
            lines.append("|----------|-------|-----|----------|")
            for cat_name, cdata in sorted(per_cat.items()):
                top = (
                    cdata.get("top_n_words", [{}])[0].get("word", "—")
                    if cdata.get("top_n_words")
                    else "—"
                )
                lines.append(
                    f"| {cat_name} | {cdata.get('types', '?'):,} | {cdata.get('ttr', '?')} | {top} |"
                )
        lines.append("")

    # ── 3. Temporal diagnostics ──────────────────────────────────────
    if temporal:
        lines.append("## 3. Temporal Diagnostics")
        lines.append("")
        cov = temporal.get("coverage", {})
        if cov:
            lines.append(
                f"- **Coverage:** {cov.get('n_months_with_data')}/{cov.get('n_months_total')} months ({cov.get('coverage_pct')}%)"
            )
            if cov.get("n_gaps", 0) > 0:
                lines.append(
                    f"- **Gaps:** {cov['n_gaps']} gap(s), max {cov.get('max_gap_months')} consecutive months"
                )
            ms = cov.get("monthly_statistics", {})
            if ms:
                lines.append(
                    f"- **Articles/month:** mean={ms.get('mean_articles_per_month')}, range={ms.get('min_articles_month')}–{ms.get('max_articles_month')}"
                )

        boundaries = temporal.get("source_boundaries", [])
        if boundaries:
            sig_count = sum(1 for b in boundaries if b["significant"])
            lines.append("")
            lines.append(
                f"**Source transitions:** {len(boundaries)} detected, {sig_count} significant"
            )
            lines.append("")
            lines.append("| Transition | Year | KS | p-value | Significant |")
            lines.append("|------------|------|----|---------|-------------|")
            for b in boundaries[:10]:
                sig = "⚠️" if b["significant"] else "✓"
                lines.append(
                    f"| {b['source_a']}→{b['source_b']} | {b['transition_year']} | {b['ks_statistic']} | {b['p_value']} | {sig} |"
                )
        lines.append("")

    # ── 4. Schema validation ─────────────────────────────────────────
    if schema:
        lines.append("## 4. Schema Validation")
        lines.append("")
        lines.append(f"- **Schema domain:** {schema.get('schema', {}).get('domain', '?')}")
        lines.append(f"- **Sample size:** {schema.get('sample_size', '?'):,} articles")
        status = "✅ Pass" if schema.get("passes_threshold") else "🔴 Needs review"
        lines.append(f"- **Overall coverage:** {schema.get('overall_coverage', '?')}% — {status}")

        if schema.get("dead_fields"):
            lines.append(f"- **Dead fields:** {', '.join(schema['dead_fields'])} ⚠️")

        lines.append("")
        lines.append("**Per-field coverage:**")
        lines.append("")
        lines.append("| Field | Coverage | Status |")
        lines.append("|-------|----------|--------|")
        for fname, fdata in schema.get("per_field", {}).items():
            pct = fdata.get("any_match_pct", 0)
            badge = _coverage_badge(pct)
            lines.append(f"| {fname} | {pct}% | {badge} |")
        lines.append("")

    # ── 5. Recommendations ───────────────────────────────────────────
    lines.append("## 5. Recommendations")
    lines.append("")

    recommendations: list[str] = []

    if profile and profile.get("quality", {}).get("empty_texts", 0) > 0:
        recommendations.append(
            f"- 🔴 **{profile['quality']['empty_texts']} empty texts detected.** "
            "Filter or investigate before running annotation."
        )

    if schema and schema.get("dead_fields"):
        recommendations.append(
            f"- 🔴 **{len(schema['dead_fields'])} dead field(s): {', '.join(schema['dead_fields'])}. "
            "Consider removing or revising these schema fields before annotation."
        )

    if temporal:
        cov = temporal.get("coverage", {})
        if cov.get("n_gaps", 0) > 0:
            recommendations.append(
                f"- 🟡 **{cov['n_gaps']} coverage gap(s).** "
                "Time-series indices will have missing months in these periods."
            )
        boundaries = temporal.get("source_boundaries", [])
        sig_boundaries = [b for b in boundaries if b["significant"]]
        if sig_boundaries:
            for b in sig_boundaries[:3]:
                recommendations.append(
                    f"- 🔴 **Significant source shift at {b['transition_year']}:** "
                    f"{b['source_a']}→{b['source_b']} (KS={b['ks_statistic']}, p={b['p_value']}). "
                    "This may create artifacts in temporal indices."
                )

    if vocab and vocab.get("hapax_percentage", 0) > 60:
        recommendations.append(
            f"- 🟡 **Very high hapax ratio ({vocab['hapax_percentage']}%).** "
            "Corpus has many rare terms — consider whether stopword or frequency filtering is needed."
        )

    if not recommendations:
        recommendations.append(
            "- ✅ No critical issues detected. Corpus is ready for annotation and indexing."
        )

    if profile and schema:
        rec = _annotation_readiness_recommendation(profile, schema)
        if rec:
            recommendations.append(rec)

    for rec in recommendations:
        lines.append(rec)
    lines.append("")

    # ── Footer ───────────────────────────────────────────────────────
    lines.append("---")
    lines.append(
        f"*Report auto-generated by LILA Lab Data Observatory on {date.today().isoformat()}*"
    )
    lines.append("")

    report = out / "diagnostic_report.md"
    report.write_text("\n".join(lines) + "\n")
    logger.info("Diagnostic report written to %s", report)
    return report


# ── Helpers ───────────────────────────────────────────────────────────


def _phase_metric(phase: str, data: dict[str, Any]) -> str:
    if phase == "profile":
        return f"{data.get('n_articles', '?'):,} articles, {data.get('n_sources', '?')} sources"
    elif phase == "vocabulary":
        return f"TTR={data.get('ttr', '?')}, {data.get('types', '?'):,} types"
    elif phase == "temporal":
        cov = data.get("coverage", {})
        return f"{cov.get('n_months_with_data', '?')}/{cov.get('n_months_total', '?')} months"
    elif phase == "schema":
        return f"{data.get('overall_coverage', '?')}% coverage, {data.get('n_dead_fields', 0)} dead fields"
    return ""


def _annotation_readiness_recommendation(
    profile: dict[str, Any],
    schema: dict[str, Any],
) -> str | None:
    """Return a go/no-go recommendation for annotation."""
    issues: list[str] = []

    if profile.get("quality", {}).get("empty_texts_pct", 0) > 5:
        issues.append("empty texts")
    if schema.get("n_dead_fields", 0) > 0:
        dead = ", ".join(schema["dead_fields"])
        issues.append(f"dead schema fields ({dead})")
    if not schema.get("passes_threshold", True):
        issues.append("low schema coverage")

    if not issues:
        return "- ✅ **Annotation readiness:** Corpus passes all checks. Ready for annotation pipeline."
    return f"- 🟡 **Annotation readiness:** Issues found — {'; '.join(issues)}. Resolve before full annotation run."


def generate_registry_update(
    report_dir: str | Path,
    phases: dict[str, str | Path | None],
) -> dict[str, str]:
    """Generate the ``exploration`` status dict for registry update.

    Returns a dict mapping phase names to status strings (``"complete"``,
    ``"not_run"``, ``"error"``).
    """
    statuses: dict[str, str] = {}
    for key, path in phases.items():
        if path is None:
            statuses[key] = "not_run"
        else:
            data = _load_json(path)
            if data is None:
                statuses[key] = "not_run"
            elif "error" in data:
                statuses[key] = "error"
            else:
                statuses[key] = "complete"
    return statuses
