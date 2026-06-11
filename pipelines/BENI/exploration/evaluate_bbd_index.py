#!/usr/bin/env python3
"""Evaluate BBD index against macroeconomic indicators.

Loads the BBD index from 06_bbd_index, merges with CPI, FX, and
reserves, then computes:

- Contemporaneous level correlations (Pearson, Spearman)
- First-differenced (detrended) correlations
- Narrative-leads-macro correlations (1, 3, 6 month leads)
- Annual-level correlation with foreign reserves
- Diagnostic plots

Usage::

    python evaluate_bbd_index.py
    python evaluate_bbd_index.py --output outputs/06_bbd_index
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr


def _parse_imf_period(period: str) -> str:
    """Convert IMF TIME_PERIOD like '2020-M01' → '2020-01'."""
    parts = period.split("-M")
    return f"{parts[0]}-{parts[1].zfill(2)}"


def load_bbd_index(path: Path) -> pd.DataFrame:
    idx = pd.read_csv(path)
    idx["month"] = pd.to_datetime(idx["year_month"] + "-01")
    return idx.sort_values("month").reset_index(drop=True)


def load_bis_fx(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["month"] = pd.to_datetime(df["TIME_PERIOD"] + "-01")
    df = df[["month", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "fx_bis"})
    return df.dropna()


def load_imf_cpi(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[df["OBS_VALUE"].notna()].copy()
    df["month"] = pd.to_datetime(df["TIME_PERIOD"].map(_parse_imf_period) + "-01")
    df = df[["month", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "cpi"})
    return df


def load_reserves(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df[["year", "reserves_usd"]]


def make_annual(monthly: pd.DataFrame) -> pd.DataFrame:
    monthly = monthly.copy()
    monthly["year"] = monthly["month"].dt.year
    return monthly.groupby("year").mean(numeric_only=True).reset_index()


def compute_correlations(
    merged: pd.DataFrame, x_col: str, y_cols: list[str], label: str
) -> list[dict]:
    rows = []
    for y in y_cols:
        pair = merged[[x_col, y]].dropna()
        n = len(pair)
        if n < 5:
            continue
        r_p, p_p = pearsonr(pair[x_col], pair[y])
        r_s, p_s = spearmanr(pair[x_col], pair[y])
        rows.append({
            "frequency": label,
            "x": x_col,
            "y": y,
            "n": n,
            "pearson_r": round(r_p, 4),
            "pearson_p": round(p_p, 4),
            "spearman_r": round(r_s, 4),
            "spearman_p": round(p_s, 4),
        })
    return rows


def correlation_report(
    results: list[dict], monthly: pd.DataFrame, diffed: pd.DataFrame
) -> str:
    lines = []
    lines.append("# BBD Index — Macroeconomic Correlation Report\n")
    lines.append(
        f"**Period:** {monthly['month'].min().strftime('%Y-%m')} — "
        f"{monthly['month'].max().strftime('%Y-%m')}  "
        f"({len(monthly)} months)\n"
    )

    sig_0 = [r for r in results if r["pearson_p"] < 0.05]
    sig_1 = [r for r in results if r["pearson_p"] < 0.01]

    lines.append(
        f"**Significant at p<0.01:** {len(sig_1)} / {len(results)}  "
        f"|  **p<0.05:** {len(sig_0)} / {len(results)}\n"
    )

    # Group by frequency
    from itertools import groupby
    results_sorted = sorted(results, key=lambda r: r["frequency"])
    for freq, group in groupby(results_sorted, key=lambda r: r["frequency"]):
        rows = list(group)
        lines.append(f"\n## {freq}\n")
        lines.append("| x | y | n | Pearson r | p | Spearman r | p | Sig |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for r in rows:
            sig = ""
            if r["pearson_p"] < 0.01:
                sig = "**"
            elif r["pearson_p"] < 0.05:
                sig = "*"
            lines.append(
                f"| {r['x']} | {r['y']} | {r['n']} | {r['pearson_r']:.4f} | "
                f"{r['pearson_p']:.4f} | {r['spearman_r']:.4f} | "
                f"{r['spearman_p']:.4f} | {sig} |"
            )

    # Summary statistics
    lines.append("\n## Summary Statistics\n")
    lines.append(f"- **Mean triple_share:** {monthly['triple_share'].mean():.1%} "
                 f"(range: {monthly['triple_share'].min():.1%} – {monthly['triple_share'].max():.1%})")
    lines.append(f"- **Mean CPI (2021=100):** {monthly['cpi'].mean():.1f}")
    lines.append(f"- **Mean FX (BDT/USD):** {monthly['fx_bis'].mean():.2f}")
    lines.append(f"- **triple_share std:** {monthly['triple_share'].std():.3f}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Evaluate BBD index vs macro")
    parser.add_argument("--bbd-index", type=Path,
                        default=_HERE / "outputs/06_bbd_index/beni_bbd_index.csv")
    parser.add_argument("--macro-dir", type=Path,
                        default=_PIPELINES / "BENI/data/raw/macro")
    parser.add_argument("--output", type=Path,
                        default=_HERE / "outputs/06_bbd_index")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    macro_dir = Path(args.macro_dir)

    # 1. Load BBD index
    idx = load_bbd_index(args.bbd_index)
    print(f"BBD index: {len(idx)} months "
          f"({idx['month'].min().date()} to {idx['month'].max().date()})")

    # 2. Load macro series
    bis_fx = load_bis_fx(macro_dir / "fx_bdt_usd_bis_eop_monthly.csv")
    imf_cpi = load_imf_cpi(macro_dir / "cpi_imf_bgd_index_monthly.csv")
    imf_fx = load_bis_fx(macro_dir / "fx_bdt_usd_imf_eop_monthly.csv")
    reserves = load_reserves(macro_dir / "reserves_wb_annual.csv")

    print(f"BIS FX:   {len(bis_fx)} months ({bis_fx['month'].min().date()} – {bis_fx['month'].max().date()})")
    print(f"IMF CPI:  {len(imf_cpi)} months ({imf_cpi['month'].min().date()} – {imf_cpi['month'].max().date()})")
    print(f"Reserves: {len(reserves)} years")

    # 3. Merge monthly
    monthly = idx.merge(bis_fx, on="month", how="inner")
    monthly = monthly.merge(imf_cpi, on="month", how="inner")
    monthly = monthly.sort_values("month").reset_index(drop=True)
    print(f"\nMerged monthly: {len(monthly)} months "
          f"({monthly['month'].min().date()} – {monthly['month'].max().date()})")

    # 4. Correlations
    results = []
    macro_cols = ["fx_bis", "cpi"]

    # Contemporaneous level
    results += compute_correlations(monthly, "triple_share", macro_cols, "monthly_level")
    results += compute_correlations(monthly, "beni_index", macro_cols, "monthly_level")
    results += compute_correlations(monthly, "sentiment_balance", macro_cols, "monthly_level")

    # 5. First-differenced
    diffed = monthly.copy()
    diff_cols = ["triple_share", "beni_index", "sentiment_balance"] + macro_cols
    for c in diff_cols:
        diffed[f"{c}_d1"] = diffed[c].diff()
    diffed = diffed.dropna().reset_index(drop=True)
    diff_macro = [f"{c}_d1" for c in macro_cols]
    results += compute_correlations(diffed, "triple_share_d1", diff_macro, "monthly_diff")
    results += compute_correlations(diffed, "beni_index_d1", diff_macro, "monthly_diff")

    # 6. Narrative leads macro by 1, 3, 6 months
    for lag in [1, 3, 6]:
        shifted = monthly.copy()
        for mc in macro_cols:
            shifted[f"{mc}_lead{lag}"] = shifted[mc].shift(-lag)
        lead_cols = [f"{c}_lead{lag}" for c in macro_cols]
        results += compute_correlations(shifted, "triple_share", lead_cols,
                                        f"narrative_leads_{lag}m")
        results += compute_correlations(shifted, "beni_index", lead_cols,
                                        f"narrative_leads_{lag}m")

    # 7. Annual level with reserves
    annual_idx = make_annual(monthly)
    annual = annual_idx.merge(reserves, on="year", how="inner")
    print(f"Annual merge: {len(annual)} years ({annual['year'].min()} – {annual['year'].max()})")
    results += compute_correlations(annual, "triple_share", ["reserves_usd"], "annual")
    results += compute_correlations(annual, "beni_index", ["reserves_usd"], "annual")

    # 8. Save results
    res_df = pd.DataFrame(results)
    res_path = output_dir / "bbd_macro_correlations.csv"
    res_df.to_csv(res_path, index=False)
    print(f"\nCorrelations → {res_path}")

    # 9. Print summary
    print("\n=== Correlation Results ===")
    for r in results:
        sig = ""
        if r["pearson_p"] < 0.01:
            sig = "**"
        elif r["pearson_p"] < 0.05:
            sig = "*"
        print(f"  [{r['frequency']:20s}] {r['x']:15s} vs {r['y']:12s}  "
              f"r={r['pearson_r']:7.4f}{sig}  (p={r['pearson_p']:.4f})  n={r['n']}")

    # 10. Generate report
    report = correlation_report(results, monthly, diffed)
    report_path = output_dir / "bbd_macro_correlation_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport → {report_path}")


if __name__ == "__main__":
    main()
