"""
Inter-annotator agreement metrics for Audio Annotation Lab.

Implements from-scratch agreement statistics suitable for evaluating
consistency across LLM and human annotators on categorical data.

Functions
---------
krippendorff_alpha
    Multi-annotator categorical agreement (pure Python).
cohens_kappa
    Pairwise Cohen's kappa for two annotators.
pairwise_agreement_matrix
    Pairwise percent-agreement across all annotator pairs.
agreement_report
    Full agreement summary dictionary.
"""

from __future__ import annotations

import itertools
from collections import defaultdict
from typing import Any

import pandas as pd

# ── Helper ───────────────────────────────────────────────────────────


def _reliability_data(
    annotations: list[dict],
    field: str = "primary_field",
) -> tuple[dict[str, int], dict[str, list[tuple[str, int | None]]]]:
    """Convert annotation records into a reliability-data matrix.

    Returns
    -------
    value_to_code : dict[str, int]
        Mapping from label value to numeric code.
    units : dict[str, list[tuple[str, int | None]]]
        Mapping from segment_id to list of (annotator, code) pairs.
        Missing annotations are represented as ``None`` codes.
    """
    value_to_code: dict[str, int] = {}
    code_counter = 0
    units: dict[str, list[tuple[str, int | None]]] = defaultdict(list)

    for ann in annotations:
        seg_id = ann.get("segment_id", "")
        annotator = ann.get("annotator", "")
        labels: dict = ann.get("labels", {})
        raw_val = labels.get(field)

        if raw_val is None:
            units[seg_id].append((annotator, None))
            continue

        if raw_val not in value_to_code:
            value_to_code[raw_val] = code_counter
            code_counter += 1
        units[seg_id].append((annotator, value_to_code[raw_val]))

    return value_to_code, dict(units)


def _coincidence_matrix(
    units: dict[str, list[tuple[str, int | None]]],
    n_codes: int,
) -> list[list[int]]:
    """Build the coincidence matrix for Krippendorff's alpha.

    ``o_{vu}`` is the number of times code ``v`` is paired with code ``u``
    across all unit-annotator pairs.
    """
    coinc: list[list[int]] = [[0] * n_codes for _ in range(n_codes)]

    for pairs in units.values():
        # Only consider units with at least 2 annotations
        annotators_present = [p for p in pairs if p[1] is not None]
        for (_, v), (_, u) in itertools.permutations(annotators_present, 2):
            coinc[v][u] += 1

    return coinc


# ── Public API ───────────────────────────────────────────────────────


def krippendorff_alpha(
    annotations: list[dict],
    field: str = "primary_field",
    level: str = "nominal",
) -> float:
    """Compute Krippendorff's alpha for multi-annotator categorical data.

    This is a pure-Python implementation (no external dependency) based on
    Krippendorff (2004, 2011).  It handles missing annotations and
    unbalanced annotator sets gracefully.

    Parameters
    ----------
    annotations : list[dict]
        Each dict must contain ``segment_id``, ``annotator``, and ``labels``
        (a dict mapping field -> value).
    field : str
        The label field within ``labels`` to compare (default ``"primary_field"``).
    level : str
        Measurement level: ``"nominal"`` (default), ``"ordinal"``, ``"interval"``,
        or ``"ratio"``.

    Returns
    -------
    float
        Krippendorff's alpha in [-1, 1]; 1 = perfect agreement,
        0 = chance-level, < 0 = systematic disagreement.

    Raises
    ------
    ValueError
        If there are fewer than 2 usable units or codes.

    References
    ----------
    Krippendorff, K. (2004). Content analysis: An introduction to its
    methodology (2nd ed.). Sage.
    """
    value_to_code, units = _reliability_data(annotations, field)
    n_codes = len(value_to_code)

    if n_codes < 2:
        msg = f"Need at least 2 distinct values for field '{field}', got {n_codes}"
        raise ValueError(msg)

    coinc = _coincidence_matrix(units, n_codes)

    # Total paired observations
    total_paired = sum(sum(row) for row in coinc)
    if total_paired == 0:
        msg = "No paired observations found; at least 2 annotators per item needed"
        raise ValueError(msg)

    # Row / column sums (same, symmetric)
    totals = [sum(row) for row in coinc]

    if level == "nominal":
        # Observed disagreement
        observed = sum(coinc[c][k] for c in range(n_codes) for k in range(n_codes) if c != k)

        # Expected disagreement (chance)
        expected = (
            sum(totals[c] * totals[k] for c in range(n_codes) for k in range(n_codes) if c != k)
            / total_paired
        )

    elif level == "ordinal":
        observed = 0.0
        expected = 0.0
        for c in range(n_codes):
            for k in range(n_codes):
                if c == k:
                    continue
                # Guttman's metric: (sum_{g=c}^{k} n_g - (n_c+n_k)/2)^2
                n_g = sum(totals[c : k + 1]) if c <= k else sum(totals[k : c + 1])
                metric = (n_g - (totals[c] + totals[k]) / 2) ** 2
                observed += coinc[c][k] * metric
                expected += totals[c] * totals[k] * metric / total_paired
    elif level in ("interval", "ratio"):
        observed = 0.0
        expected = 0.0
        for c in range(n_codes):
            for k in range(n_codes):
                if c == k:
                    continue
                metric = (c - k) ** 2
                observed += coinc[c][k] * metric
                expected += totals[c] * totals[k] * metric / total_paired
    else:
        msg = f"Unknown level '{level}'; use nominal, ordinal, interval, or ratio"
        raise ValueError(msg)

    if expected == 0:
        return 1.0  # Perfect agreement trivially

    return 1.0 - observed / expected


def cohens_kappa(
    annotations_a: list[str],
    annotations_b: list[str],
    labels: list[str] | None = None,
) -> float:
    """Compute Cohen's kappa for two annotators.

    Parameters
    ----------
    annotations_a : list[str]
        Labels from annotator A (one per item).
    annotations_b : list[str]
        Labels from annotator B (one per item).
    labels : list[str] | None
        Explicit label set.  If ``None``, the union of observed labels is used.

    Returns
    -------
    float
        Cohen's kappa in [-1, 1].

    Raises
    ------
    ValueError
        If the two annotation lists differ in length or fewer than 2 items.
    """
    if len(annotations_a) != len(annotations_b):
        msg = f"Annotation list length mismatch: {len(annotations_a)} vs {len(annotations_b)}"
        raise ValueError(msg)
    n = len(annotations_a)
    if n < 2:
        msg = f"Need at least 2 items, got {n}"
        raise ValueError(msg)

    if labels is None:
        labels = sorted(set(annotations_a) | set(annotations_b))

    label_idx = {lbl: i for i, lbl in enumerate(labels)}
    m = len(labels)

    # Contingency matrix
    obs: list[list[int]] = [[0] * m for _ in range(m)]
    for a, b in zip(annotations_a, annotations_b):
        ia = label_idx.get(a)
        ib = label_idx.get(b)
        if ia is not None and ib is not None:
            obs[ia][ib] += 1

    # Observed agreement proportion
    po = sum(obs[i][i] for i in range(m)) / n

    # Expected agreement proportion
    row_sums = [sum(row) for row in obs]
    col_sums = [sum(obs[i][j] for i in range(m)) for j in range(m)]
    pe = sum(row_sums[i] * col_sums[i] for i in range(m)) / (n * n)

    if pe == 1.0:
        return 1.0  # Trivial perfect agreement

    return (po - pe) / (1.0 - pe)


def pairwise_agreement_matrix(
    annotations: list[dict],
    annotators: list[str],
    field: str = "primary_field",
) -> pd.DataFrame:
    """Compute pairwise percent-agreement between all annotator pairs.

    Parameters
    ----------
    annotations : list[dict]
        Annotation records (see :func:`krippendorff_alpha`).
    annotators : list[str]
        List of annotator IDs to include.
    field : str
        Label field to compare.

    Returns
    -------
    pd.DataFrame
        Symmetric matrix with annotators as both index and columns.
    """
    # Build per-segment, per-annotator lookup
    seg_annots: dict[str, dict[str, str | None]] = defaultdict(dict)
    for ann in annotations:
        seg_id = ann.get("segment_id", "")
        annotator = ann.get("annotator", "")
        if annotator not in annotators:
            continue
        labels: dict = ann.get("labels", {})
        val = labels.get(field)
        seg_annots[seg_id][annotator] = val

    matrix = pd.DataFrame(0.0, index=annotators, columns=annotators)

    for a, b in itertools.combinations(annotators, 2):
        agreements = 0
        comparisons = 0
        for seg_pairs in seg_annots.values():
            va = seg_pairs.get(a)
            vb = seg_pairs.get(b)
            if va is not None and vb is not None:
                comparisons += 1
                if va == vb:
                    agreements += 1
        pct = agreements / comparisons if comparisons > 0 else 0.0
        matrix.loc[a, b] = pct
        matrix.loc[b, a] = pct

    # Diagonal is 1.0 (self-agreement)
    for a in annotators:
        matrix.loc[a, a] = 1.0

    return matrix


def agreement_report(
    annotations: list[dict],
    field: str = "primary_field",
) -> dict[str, Any]:
    """Produce a full inter-annotator agreement report.

    Parameters
    ----------
    annotations : list[dict]
        Annotation records (see :func:`krippendorff_alpha`).
    field : str
        Label field to analyse.

    Returns
    -------
    dict
        Report containing:

        - ``krippendorff_alpha`` — overall alpha
        - ``n_annotators`` — unique annotator count
        - ``n_items`` — unique segment/item count
        - ``pairwise_kappa`` — dict of ``(a, b) → κ``
        - ``percent_agreement`` — overall proportion of agreeing pairs
        - ``field`` — the field analysed
    """
    value_to_code, units = _reliability_data(annotations, field)
    n_codes = len(value_to_code)
    n_codes = max(n_codes, 2)  # avoids zero-division edge cases

    # Annotator set
    all_annotators = sorted({ann.get("annotator", "") for ann in annotations})
    n_annotators = len(all_annotators)
    n_items = len(units)

    # Krippendorff's alpha
    try:
        alpha = krippendorff_alpha(annotations, field)
    except ValueError:
        alpha = float("nan")

    # Pairwise Cohen's kappa
    seg_annots: dict[str, dict[str, str | None]] = defaultdict(dict)
    for ann in annotations:
        seg_id = ann.get("segment_id", "")
        annotator = ann.get("annotator", "")
        labels: dict = ann.get("labels", {})
        val = labels.get(field)
        seg_annots[seg_id][annotator] = val

    pairwise_kappa: dict[str, float] = {}
    total_pairs = 0
    total_agree = 0

    for a, b in itertools.combinations(all_annotators, 2):
        list_a: list[str] = []
        list_b: list[str] = []
        for seg_pairs in seg_annots.values():
            va = seg_pairs.get(a)
            vb = seg_pairs.get(b)
            if va is not None and vb is not None:
                list_a.append(va)
                list_b.append(vb)

        if len(list_a) < 2:
            continue

        try:
            k = cohens_kappa(list_a, list_b)
        except ValueError:
            k = float("nan")

        key = f"{a} vs {b}"
        pairwise_kappa[key] = round(k, 4)

        # Percent agreement
        agree_count = sum(1 for va, vb in zip(list_a, list_b) if va == vb)
        total_agree += agree_count
        total_pairs += len(list_a)

    percent_agreement = total_agree / total_pairs if total_pairs > 0 else float("nan")

    return {
        "krippendorff_alpha": round(alpha, 4),
        "n_annotators": n_annotators,
        "n_items": n_items,
        "field": field,
        "pairwise_kappa": pairwise_kappa,
        "percent_agreement": round(percent_agreement, 4),
    }
