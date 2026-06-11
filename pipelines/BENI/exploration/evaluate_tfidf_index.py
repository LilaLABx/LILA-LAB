#!/usr/bin/env python3
"""Evaluate TF-IDF narrative index against macroeconomic indicators.

Usage::

    python evaluate_tfidf_index.py
    python evaluate_tfidf_index.py --output outputs/07_tfidf_index
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import groupby
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr


# ── helpers ──────────────────────────────────────────────────────────

def _parse_imf_period(period: str) -> str:
    parts = period.split("-M")
    return f"{parts[0]}-{parts[1].zfill(2)}"


def load_index(path: Path) -> pd.DataFrame:
    idx = pd.read_csv(path)
    idx["month"] = pd.to_datetime(idx["year_month"] + "-01")
    return idx.sort_values("month").reset_index(drop=True)


def load_bis_fx(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["month"] = pd.to_datetime(df["TIME_PERIOD"] + "-01")
    return df[["month", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "fx_bis"}).dropna()


def load_imf_cpi(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[df["OBS_VALUE"].notna()].copy()
    df["month"] = pd.to_datetime(df["TIME_PERIOD"].map(_parse_imf_period) + "-01")
    return df[["month", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "cpi"})


def load_reserves(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)[["year", "reserves_usd"]]


def make_annual(monthly: pd.DataFrame) -> pd.DataFrame:
    m = monthly.copy()
    m["year"] = m["month"].dt.year
    return m.groupby("year").mean(numeric_only=True).reset_index()


def compute_corr(
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


def make_report(results: list[dict], monthly: pd.DataFrame) -> str:
    lines = []
    lines.append("# TF-IDF Narrative Index — Macroeconomic Correlation Report\n")
    lines.append(
        f"**Period:** {monthly['month'].min().strftime('%Y-%m')} — "
        f"{monthly['month'].max().strftime('%Y-%m')}  "
        f"({len(monthly)} months, 2015+)\n"
    )

    sig_05 = [r for r in results if r["pearson_p"] < 0.05]
    sig_01 = [r for r in results if r["pearson_p"] < 0.01]
    lines.append(
        f"**Significant at p<0.01:** {len(sig_01)} / {len(results)}  "
        f"|  **p<0.05:** {len(sig_05)} / {len(results)}\n"
    )

    results_sorted = sorted(results, key=lambda r: r["frequency"])
    for freq, group in groupby(results_sorted, key=lambda r: r["frequency"]):
        rows = list(group)
        lines.append(f"\n## {freq}\n")
        lines.append("| x | y | n | Pearson r | p | Spearman r | p | Sig |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for r in rows:
            sig = "**" if r["pearson_p"] < 0.01 else ("*" if r["pearson_p"] < 0.05 else "")
            lines.append(
                f"| {r['x']} | {r['y']} | {r['n']} | {r['pearson_r']:.4f} | "
                f"{r['pearson_p']:.4f} | {r['spearman_r']:.4f} | "
                f"{r['spearman_p']:.4f} | {sig} |"
            )

    lines.append("\n## Summary Statistics\n")
    lines.append(f"- **Mean TF-IDF economic_share:** {monthly['economic_share'].mean():.1%} "
                 f"(range: {monthly['economic_share'].min():.1%} – {monthly['economic_share'].max():.1%})")
    lines.append(f"- **Mean TF-IDF index:** {monthly['tfidf_index'].mean():.1f} "
                 f"(range: {monthly['tfidf_index'].min():.1f} – {monthly['tfidf_index'].max():.1f})")
    lines.append(f"- **Mean CPI (2021=100):** {monthly['cpi'].mean():.1f}")
    lines.append(f"- **Mean FX (BDT/USD):** {monthly['fx_bis'].mean():.2f}")

    return "\n".join(lines)


# ── main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Evaluate TF-IDF index vs macro")
    parser.add_argument("--tfidf-index", type=Path,
                        default=_HERE / "outputs/07_tfidf_index/beni_tfidf_index.csv")
    parser.add_argument("--bbd-index", type=Path,
                        default=_HERE / "outputs/06_bbd_index/beni_bbd_index.csv")
    parser.add_argument("--macro-dir", type=Path,
                        default=_PIPELINES / "BENI/data/raw/macro")
    parser.add_argument("--output", type=Path,
                        default=_HERE / "outputs/07_tfidf_index")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    macro_dir = Path(args.macro_dir)

    # 1. Load indices
    tfidf = load_index(args.tfidf_index)
    bbd = load_index(args.bbd_index)

    # Exclude 2014 low-coverage artifact
    tfidf = tfidf[tfidf["month"] >= "2015-01-01"].copy()
    bbd_2015 = bbd[bbd["month"] >= "2015-01-01"].copy()

    # Re-normalize TF-IDF to 2015+ mean/std
    mu, sigma = tfidf["economic_share"].mean(), tfidf["economic_share"].std()
    tfidf["tfidf_index"] = 100.0 + (tfidf["economic_share"] - mu) / sigma * 10.0

    print(f"TF-IDF index (2015+): {len(tfidf)} months "
          f"({tfidf['month'].min().date()} to {tfidf['month'].max().date()})")

    # 2. Load macro series
    bis_fx = load_bis_fx(macro_dir / "fx_bdt_usd_bis_eop_monthly.csv")
    imf_cpi = load_imf_cpi(macro_dir / "cpi_imf_bgd_index_monthly.csv")
    reserves = load_reserves(macro_dir / "reserves_wb_annual.csv")

    # 3. Merge monthly (TF-IDF + BBD + macro)
    monthly = tfidf.merge(bbd_2015[["month", "beni_index", "triple_share",
                                     "sentiment_balance"]],
                          on="month", how="inner")
    monthly = monthly.merge(bis_fx, on="month", how="inner")
    monthly = monthly.merge(imf_cpi, on="month", how="inner")
    monthly = monthly.sort_values("month").reset_index(drop=True)

    print(f"Merged monthly: {len(monthly)} months "
          f"({monthly['month'].min().date()} – {monthly['month'].max().date()})")

    # ── 4. Correlations ──────────────────────────────────────────────
    results = []
    macro_cols = ["fx_bis", "cpi"]
    narrative_cols = ["economic_share", "tfidf_index"]

    # 4a. Contemporaneous level (TF-IDF vs macro)
    for nc in narrative_cols:
        results += compute_corr(monthly, nc, macro_cols, "monthly_level")

    # 4b. BBD vs macro (for side-by-side comparison)
    for bc in ["triple_share", "beni_index"]:
        results += compute_corr(monthly, bc, macro_cols, "monthly_level_bbd")

    # 4c. TF-IDF vs BBD (contemporaneous)
    results += compute_corr(monthly, "tfidf_index", ["beni_index", "triple_share"],
                            "tfidf_vs_bbd")

    # 4d. First-differenced (remove trend)
    diffed = monthly.copy()
    diff_cols = ["economic_share", "tfidf_index", "beni_index",
                 "triple_share", "sentiment_balance"] + macro_cols
    for c in diff_cols:
        diffed[f"{c}_d1"] = diffed[c].diff()
    diffed = diffed.dropna().reset_index(drop=True)
    diff_macro = [f"{c}_d1" for c in macro_cols]
    for nc in ["economic_share_d1", "tfidf_index_d1"]:
        results += compute_corr(diffed, nc, diff_macro, "monthly_diff")

    # 4e. Narrative leads macro (1, 3, 6 months) — TF-IDF
    for lag in [1, 3, 6]:
        shifted = monthly.copy()
        for mc in macro_cols:
            shifted[f"{mc}_lead{lag}"] = shifted[mc].shift(-lag)
        lead_cols = [f"{c}_lead{lag}" for c in macro_cols]
        for nc in narrative_cols:
            results += compute_corr(shifted, nc, lead_cols,
                                    f"narrative_leads_{lag}m")

    # 4f. Macro leads narrative (1, 3, 6 months) — macro can predict TF-IDF?
    for lag in [1, 3, 6]:
        shifted = monthly.copy()
        for nc in narrative_cols:
            shifted[f"{nc}_lead{lag}"] = shifted[nc].shift(-lag)
        # narrative ~ macro (before) = macro leads narrative
        for nc in narrative_cols:
            tgt = f"{nc}_lead{lag}"
            results += compute_corr(shifted, tgt, macro_cols,
                                    f"macro_leads_narrative_{lag}m")

    # 4g. Annual level with reserves
    annual_idx = make_annual(monthly)
    annual = annual_idx.merge(reserves, on="year", how="inner")
    print(f"Annual merge: {len(annual)} years ({annual['year'].min()} – {annual['year'].max()})")
    results += compute_corr(annual, "economic_share", ["reserves_usd"], "annual")
    results += compute_corr(annual, "tfidf_index", ["reserves_usd"], "annual")

    # ── 5. Save ──────────────────────────────────────────────────────
    res_df = pd.DataFrame(results)
    res_path = output_dir / "tfidf_macro_correlations.csv"
    res_df.to_csv(res_path, index=False)
    print(f"\nCorrelations → {res_path}")

    # 6. Print summary
    print("\n=== Key Correlation Results ===\n")
    highlights = [
        r for r in results
        if r["frequency"] in ("monthly_level", "monthly_level_bbd", "tfidf_vs_bbd")
    ]
    for r in highlights:
        sig = "**" if r["pearson_p"] < 0.01 else ("*" if r["pearson_p"] < 0.05 else "")
        print(f"  [{r['frequency']:20s}] {r['x']:15s} vs {r['y']:15s}  "
              f"r={r['pearson_r']:7.4f}{sig}  (p={r['pearson_p']:.4f})  n={r['n']}")

    print("\n=== Narrative Leads Macro (TF-IDF) ===\n")
    for r in results:
        if r["frequency"].startswith("narrative_leads"):
            sig = "**" if r["pearson_p"] < 0.01 else ("*" if r["pearson_p"] < 0.05 else "")
            if "tfidf" in r["x"].lower():
                print(f"  [{r['frequency']:22s}] {r['x']:15s} vs {r['y']:15s}  "
                      f"r={r['pearson_r']:7.4f}{sig}  (p={r['pearson_p']:.4f})")

    print("\n=== Macro Leads Narrative (TF-IDF) ===\n")
    for r in results:
        if r["frequency"].startswith("macro_leads"):
            sig = "**" if r["pearson_p"] < 0.01 else ("*" if r["pearson_p"] < 0.05 else "")
            if "tfidf" in r["x"].lower() or "tfidf" in r["y"].lower():
                print(f"  [{r['frequency']:28s}] {r['x']:15s} vs {r['y']:15s}  "
                      f"r={r['pearson_r']:7.4f}{sig}  (p={r['pearson_p']:.4f})")

    print("\n=== Annual (Reserves) ===\n")
    for r in results:
        if r["frequency"] == "annual":
            sig = "**" if r["pearson_p"] < 0.01 else ("*" if r["pearson_p"] < 0.05 else "")
            print(f"  {r['x']:15s} vs {r['y']:15s}  "
                  f"r={r['pearson_r']:7.4f}{sig}  (p={r['pearson_p']:.4f})")

    print("\n=== First-Differenced (Detrended) ===\n")
    for r in results:
        if r["frequency"] == "monthly_diff":
            sig = "**" if r["pearson_p"] < 0.01 else ("*" if r["pearson_p"] < 0.05 else "")
            if "tfidf" in r["x"].lower():
                print(f"  {r['x']:20s} vs {r['y']:12s}  "
                      f"r={r['pearson_r']:7.4f}{sig}  (p={r['pearson_p']:.4f})")

    # 7. Generate report
    report = make_report(results, monthly)
    report_path = output_dir / "tfidf_macro_correlation_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport → {report_path}")

    # 8. Summary JSON
    summary = {
        "period": {
            "start": monthly["month"].min().strftime("%Y-%m"),
            "end": monthly["month"].max().strftime("%Y-%m"),
            "n_months": len(monthly),
        },
        "mean_economic_share": round(float(monthly["economic_share"].mean()), 4),
        "mean_tfidf_index": round(float(monthly["tfidf_index"].mean()), 1),
        "mean_cpi": round(float(monthly["cpi"].mean()), 1),
        "mean_fx": round(float(monthly["fx_bis"].mean()), 2),
        "significant_at_0_01": len(sig_01 := [r for r in results if r["pearson_p"] < 0.01]),
        "significant_at_0_05": len(sig_05 := [r for r in results if r["pearson_p"] < 0.05]),
        "total_tests": len(results),
    }

    # Extract key correlations for quick reference
    for r in results:
        if r["x"] == "tfidf_index" and r["y"] == "cpi" and r["frequency"] == "monthly_level":
            summary["corr_tfidf_cpi_level"] = {
                "pearson_r": r["pearson_r"], "pearson_p": r["pearson_p"],
                "spearman_r": r["spearman_r"], "spearman_p": r["spearman_p"]}
        if r["x"] == "tfidf_index" and r["y"] == "fx_bis" and r["frequency"] == "monthly_level":
            summary["corr_tfidf_fx_level"] = {
                "pearson_r": r["pearson_r"], "pearson_p": r["pearson_p"],
                "spearman_r": r["spearman_r"], "spearman_p": r["spearman_p"]}
        if r["x"] == "tfidf_index" and r["y"] == "beni_index" and r["frequency"] == "tfidf_vs_bbd":
            summary["corr_tfidf_bbd"] = {
                "pearson_r": r["pearson_r"], "pearson_p": r["pearson_p"],
                "spearman_r": r["spearman_r"], "spearman_p": r["spearman_p"]}

    json_path = output_dir / "tfidf_macro_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Summary → {json_path}")


if __name__ == "__main__":
    main()
