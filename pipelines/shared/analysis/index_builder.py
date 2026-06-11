"""Monthly narrative index construction and LLM calibration.

Builds a monthly economic narrative index from article-level predictions,
applies calibration factors from a pilot annotation study, and merges
macroeconomic time series for downstream validation.

The core index is the **economic narrative share**: the fraction of articles
in a given month classified as economically relevant. This raw share can be
calibrated using LLM annotation results (base rate adjustment, precision
weighting) and normalized for comparability across time.

Usage::

    from shared.analysis.index_builder import build_monthly_index, apply_calibration

    # Phase 3: build the monthly index
    index = build_monthly_index(
        df=articles_with_predictions,
        date_col="publication_date",
        prob_col="economic_prob",
        pred_col="economic_pred",
    )

    # Apply LLM calibration from pilot study
    calibrated = apply_calibration(index, calibration_factors={"base_rate_ratio": 1.2})

    # Merge with macro data for validation
    merged = merge_macro_data(calibrated, macro_dir="pipelines/BENI/data/raw/macro/")

TODO:
    - Implement the beni_pilot build_index.py aggregation pattern (groupby year_month → mean prob)
    - Implement LLM calibration from indices/eco/build_narrative_index.py (base_rate_ratio, precision)
    - Add optional z-score normalization
    - Add confidence intervals around the index
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def build_monthly_index(
    df: pd.DataFrame,  # noqa: F821
    date_col: str = "publication_date",
    prob_col: str = "economic_prob",
    pred_col: str = "economic_pred",
    output_dir: str | Path | None = None,
    min_articles_per_month: int = 10,
) -> dict[str, Any]:
    """Aggregate article-level predictions into a monthly narrative index.

    Groups articles by ``year_month`` (derived from ``date_col``) and computes:

    - ``n_articles``: total articles published that month
    - ``n_economic``: count of articles with ``pred_col == 1``
    - ``economic_share``: ``n_economic / n_articles`` (the core index)
    - ``mean_prob``: mean of ``prob_col`` (continuous alternative)

    Months with fewer than ``min_articles_per_month`` articles are flagged
    (they may produce unreliable estimates).

    Parameters
    ----------
    df:
        Corpus DataFrame with article-level predictions. Must contain
        ``date_col``, ``prob_col``, and ``pred_col`` columns.
    date_col:
        Column name for publication date (datetime or parseable string).
    prob_col:
        Column name for predicted probability of economic relevance (0-1).
    pred_col:
        Column name for binary prediction (0 or 1).
    output_dir:
        If provided, writes the index and summary to this directory.
    min_articles_per_month:
        Minimum articles required for a month to be included in the index.

    Returns
    -------
    dict
        Keys:
        - ``"index"`` — DataFrame (as dict records) with monthly index values
        - ``"summary"`` — dict with ``n_months``, ``date_range``, ``mean_share``
        - ``"flagged_months"`` — months below ``min_articles_per_month``

    TODO
    ----
    - Implement the aggregation from beni_pilot/build_index.py::
        monthly = (
            df.groupby("year_month")
            .agg(
                n_articles=("article_id", "count"),
                mean_prob=(prob_col, "mean"),
                economic_share=(pred_col, "mean"),
                n_economic=(pred_col, "sum"),
            )
            .sort_index()
        )
    - Add ``year_month`` derivation: ``df[date_col].dt.to_period("M").astype(str)``
    - Filter out months below ``min_articles_per_month``
    - Write to CSV and JSON if output_dir is provided
    """
    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    logger.info("Building monthly index from %s ...", date_col)

    # TODO: implement monthly aggregation
    #   1. Derive year_month: df["year_month"] = df[date_col].dt.to_period("M").astype(str)
    #   2. Group by year_month and aggregate
    #   3. Filter low-count months
    #   4. Sort chronologically

    result = {
        "index": [],
        "summary": {
            "n_months": 0,
            "date_range": {"start": None, "end": None},
            "mean_share": None,
        },
        "flagged_months": [],
    }
    return result


def apply_calibration(
    index_df: pd.DataFrame,  # noqa: F821
    calibration_factors: dict[str, float] | None = None,
    method: str = "base_rate",
) -> pd.DataFrame:  # noqa: F821
    """Apply LLM calibration to a raw narrative index.

    The raw ``economic_share`` from TF-IDF classification may over- or
    under-estimate the true proportion of economically relevant articles.
    Calibration adjusts the index using results from the pilot LLM
    annotation (Phase 1).

    Parameters
    ----------
    index_df:
        Monthly index DataFrame from ``build_monthly_index``.
    calibration_factors:
        Dict of calibration factors. Expected keys depend on ``method``:
        - ``"base_rate"``: ``{"base_rate_ratio": float}``
        - ``"llm_precision"``: ``{"precision": float, "recall": float}``
        - ``"none"``: no factors needed
    method:
        Calibration method:
        - ``"base_rate"``: multiply ``economic_share`` by the ratio of
          LLM-identified economic articles to TF-IDF-identified ones
        - ``"llm_precision"``: use precision/recall from confusion matrix:
          ``calibrated = (share - (1 - precision)) / (precision + recall - 1)``
        - ``"none"``: no calibration

    Returns
    -------
    DataFrame
        ``index_df`` with additional columns:
        ``calibrated_share``, ``calibrated_index``, ``ci_lower``, ``ci_upper``.

    TODO
    ----
    - Implement from indices/eco/build_narrative_index.py::
        calibrated_share = economic_share * base_rate_ratio
        beni_index = zscore(calibrated_share)
        ci_lower = calibrated_share - (1 - kappa) * 0.5
        ci_upper = calibrated_share + (1 - kappa) * 0.5
    - Implement z-score normalization
    - Add confidence intervals based on annotation agreement (Cohen's κ)
    """
    if calibration_factors is None:
        calibration_factors = {}

    logger.info("Applying calibration: method=%s", method)

    # TODO: implement calibration logic
    return index_df


def normalize_index(
    index_df: pd.DataFrame,  # noqa: F821
    method: str = "zscore",
    columns: list[str] | None = None,
) -> pd.DataFrame:  # noqa: F821
    """Normalize index values for comparability.

    Parameters
    ----------
    index_df:
        Monthly index DataFrame.
    method:
        Normalization method:
        - ``"zscore"``: subtract mean, divide by std
        - ``"minmax"``: scale to [0, 1]
        - ``"none"``: no normalization
    columns:
        Columns to normalize. Defaults to ``["economic_share", "calibrated_share"]``.

    Returns
    -------
    DataFrame with normalized columns.
    """
    if columns is None:
        columns = ["economic_share", "calibrated_share"]

    logger.info("Normalizing index: method=%s", method)

    return index_df


def merge_macro_data(
    index_df: pd.DataFrame,  # noqa: F821
    macro_config: list[dict[str, Any]] | None = None,
    macro_dir: str | Path | None = None,
) -> pd.DataFrame:  # noqa: F821
    """Merge macroeconomic time series with the narrative index.

    Loads macro series (CPI, FX, reserves) from CSV files and left-joins
    them to the monthly index on the ``year_month`` column.

    Parameters
    ----------
    index_df:
        Monthly index DataFrame with a ``year_month`` column (string format
        ``"YYYY-MM"``).
    macro_config:
        List of macro series configs. Each entry::
            {"name": str, "path": str, "column": str}
    macro_dir:
        Base directory for macro data paths. If provided, paths in
        ``macro_config`` are resolved relative to this directory.

    Returns
    -------
    DataFrame
        ``index_df`` with additional columns for each macro series.

    TODO
    ----
    - Implement macro loading from beni_pilot/correlate.py patterns:
        - BIS FX: pd.read_csv(fx_path, parse_dates=["date"]), resample to month-end
        - IMF CPI: same pattern
        - WB Reserves: annual, merge on year
    - Handle frequency mismatches (monthly index vs annual reserves)
    - Handle missing values (forward-fill for monthly series)
    """
    if macro_config is None:
        macro_config = []

    logger.info("Merging %d macro series", len(macro_config))

    return index_df


def load_macro_series(
    series_name: str,
    file_path: str | Path,
    column_name: str | None = None,
) -> pd.Series:  # noqa: F821
    """Load a single macroeconomic time series.

    Convenience wrapper for loading individual macro series.
    Supports BIS FX CSV, IMF CPI SDMX exports, and World Bank
    reserves data by detecting the file format.

    Parameters
    ----------
    series_name:
        Identifier for the series (e.g., ``"fx_bis"``, ``"cpi"``).
    file_path:
        Path to the CSV file.
    column_name:
        Name of the value column. If None, inferred from the file.

    Returns
    -------
    pd.Series
        Time series indexed by ``year_month`` (string format ``"YYYY-MM"``).

    TODO
    ----
    - Parse BIS FX format (date, value columns)
    - Parse IMF CPI format (SDMX)
    - Parse World Bank reserves format
    - Resample to monthly frequency
    """
    logger.info("Loading macro series: %s", series_name)
    # TODO: implement
    import pandas as pd  # noqa: F811

    return pd.Series(dtype=float)
