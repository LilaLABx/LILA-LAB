#!/usr/bin/env python3
"""Econometric validation: stationarity, Granger causality, VAR, impulse responses.

Transforms:
  CPI -> inflation acceleration (D²log CPI x 100) — stationary
  FX  -> monthly depreciation (Dlog FX x 100)      — stationary
  Indices -> first difference                       — stationary

Usage::

    python econometric_validation.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import adfuller, grangercausalitytests
from statsmodels.tsa.api import VAR
from statsmodels.stats.diagnostic import acorr_ljungbox


TFIDF_PATH = _HERE / "outputs/07_tfidf_index/beni_tfidf_index.csv"
BBD_PATH = _HERE / "outputs/06_bbd_index/beni_bbd_index.csv"
MACRO_DIR = _PIPELINES / "BENI/data/raw/macro"
OUTPUT_DIR = _HERE / "outputs/07_tfidf_index" / "econometric"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _parse_imf_period(period: str) -> str:
    parts = period.split("-M")
    return f"{parts[0]}-{parts[1].zfill(2)}"


def load_data() -> pd.DataFrame:
    tfidf = pd.read_csv(TFIDF_PATH)
    tfidf["month"] = pd.to_datetime(tfidf["year_month"] + "-01")
    tfidf = tfidf[tfidf["month"] >= "2015-01-01"].copy()
    mu, sigma = tfidf["economic_share"].mean(), tfidf["economic_share"].std()
    tfidf["tfidf_index"] = 100.0 + (tfidf["economic_share"] - mu) / sigma * 10.0

    bbd = pd.read_csv(BBD_PATH)
    bbd["month"] = pd.to_datetime(bbd["year_month"] + "-01")
    bbd = bbd[bbd["month"] >= "2015-01-01"].copy()

    fx = pd.read_csv(MACRO_DIR / "fx_bdt_usd_bis_eop_monthly.csv")
    fx["month"] = pd.to_datetime(fx["TIME_PERIOD"] + "-01")
    fx = fx[["month", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "fx_bis"}).dropna()

    cpi = pd.read_csv(MACRO_DIR / "cpi_imf_bgd_index_monthly.csv")
    cpi = cpi[cpi["OBS_VALUE"].notna()].copy()
    cpi["month"] = pd.to_datetime(cpi["TIME_PERIOD"].map(_parse_imf_period) + "-01")
    cpi = cpi[["month", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "cpi"})

    df = tfidf[["month", "tfidf_index", "economic_share"]].merge(
        bbd[["month", "beni_index", "triple_share", "sentiment_balance"]],
        on="month", how="inner"
    ).merge(fx, on="month", how="inner").merge(cpi, on="month", how="inner")
    df = df.sort_values("month").reset_index(drop=True)

    log_cpi = np.log(df["cpi"])
    log_fx = np.log(df["fx_bis"])

    df["d2cpi"] = log_cpi.diff().diff() * 100    # inflation acceleration
    df["dfx"] = log_fx.diff() * 100               # depreciation rate
    df["dtfidf"] = df["tfidf_index"].diff()
    df["dbbd"] = df["beni_index"].diff()

    return df


def _adf_report(series: pd.Series, name: str, maxlag: int = 12) -> dict:
    result = adfuller(series.dropna(), maxlag=maxlag, autolag="AIC")
    return {
        "series": name,
        "adf_stat": round(result[0], 4),
        "p_value": round(result[1], 4),
        "stationary": result[1] < 0.05,
    }


def _r_sq(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    ss_res = ((y_true - y_pred) ** 2).sum()
    ss_tot = ((y_true - y_true.mean()) ** 2).sum()
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0


def plot_impulse_responses(irf, names: list[str], n_p: int = 12) -> str:
    n = len(names)
    fig, axes = plt.subplots(nrows=n, ncols=n, figsize=(3 * n + 1, 3 * n + 1))
    fig.suptitle("Orthogonalized Impulse Response Functions (1 SD shock)",
                 fontsize=14, y=1.02)
    stderr = irf.stderr()  # (steps+1, n, n)
    for i in range(n):
        for j in range(n):
            ax = axes[i, j]
            resp = irf.orth_irfs[:, i, j]
            se = stderr[:, i, j]
            lo = resp - 1.96 * se
            hi = resp + 1.96 * se
            ax.plot(range(n_p + 1), resp, "b-", lw=1.5)
            ax.fill_between(range(n_p + 1), lo, hi, alpha=0.2, color="blue")
            ax.axhline(y=0, color="k", ls="--", lw=0.5)
            if i == n - 1:
                ax.set_xlabel(f"Shock {names[j]}", fontsize=9)
            if j == 0:
                ax.set_ylabel(names[i], fontsize=9)
            ax.tick_params(labelsize=7)
    plt.tight_layout()
    path = OUTPUT_DIR / "impulse_responses.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return str(path)


def main():
    df = load_data()
    df_s = df.dropna().reset_index(drop=True)
    print(f"Period: {df_s['month'].min().date()} - {df_s['month'].max().date()}  "
          f"({len(df_s)} months)\n")

    results: dict = {"stationarity": [], "granger": [], "var": {}}

    # ── 1. UNIT ROOT TESTS ──────────────────────────────────────
    print("=" * 66)
    print("1. ADF Unit Root Tests")
    print("=" * 66)

    for col, label in [
        ("tfidf_index", "TF-IDF Index (level)"),
        ("beni_index", "BBD Index (level)"),
        ("cpi", "CPI Index (level)"),
        ("fx_bis", "FX BDT/USD (level)"),
        ("dtfidf", "D TF-IDF Index"),
        ("dbbd", "D BBD Index"),
        ("d2cpi", "D2 log CPI (inflation accel.)"),
        ("dfx", "D log FX (depreciation)"),
    ]:
        series = df[col].dropna() if col.startswith("d") else df[col]
        r = _adf_report(series, label)
        results["stationarity"].append(r)
        sym = "+" if r["stationary"] else "x"
        print(f"  {r['series']:42s}  ADF={r['adf_stat']:7.4f}  p={r['p_value']:.4f}  {sym}")

    # ── 2. GRANGER CAUSALITY ───────────────────────────────────
    print("\n" + "=" * 66)
    print("2. Granger Causality (maxlag=4, on stationary data)")
    print("=" * 66)

    pairs = [
        ("dtfidf", "d2cpi", "DTF-IDF -> Inflation"),
        ("d2cpi", "dtfidf", "Inflation -> DTF-IDF"),
        ("dtfidf", "dfx", "DTF-IDF -> Depreciation"),
        ("dfx", "dtfidf", "Depreciation -> DTF-IDF"),
        ("dbbd", "d2cpi", "DBBD -> Inflation"),
        ("d2cpi", "dbbd", "Inflation -> DBBD"),
        ("dbbd", "dfx", "DBBD -> Depreciation"),
        ("dfx", "dbbd", "Depreciation -> DBBD"),
        ("dtfidf", "dbbd", "DTF-IDF -> DBBD"),
        ("dbbd", "dtfidf", "DBBD -> DTF-IDF"),
    ]

    for cause, effect, label in pairs:
        gd = df_s[[cause, effect]].dropna()
        try:
            tr = grangercausalitytests(gd, maxlag=4, verbose=False)
            bp, bl = 1.0, None
            for lag in range(1, 5):
                p = tr[lag][0]["ssr_chi2test"][1]
                if p < bp:
                    bp, bl = p, lag
            results["granger"].append({
                "cause": cause, "effect": effect, "label": label,
                "best_lag": bl, "best_p": round(bp, 4),
                "significant_5pct": bp < 0.05})
            stars = "***" if bp < 0.01 else ("**" if bp < 0.05 else (
                "*" if bp < 0.10 else ""))
            print(f"  {label:35s}  lag={bl}  p={bp:.4f}  {stars}")
        except Exception as e:
            print(f"  {label:35s}  ERROR: {e}")

    # ── 3. VAR ──────────────────────────────────────────────────
    print("\n" + "=" * 66)
    print("3. VAR Models (stationary data)")
    print("=" * 66)

    specs = [
        ("VAR: TF-IDF + Inflation + Depreciation",
         ["dtfidf", "d2cpi", "dfx"],
         ["DTF-IDF", "Inflation", "Depreciation"]),
        ("VAR: BBD + Inflation + Depreciation",
         ["dbbd", "d2cpi", "dfx"],
         ["DBBD", "Inflation", "Depreciation"]),
    ]

    for label, cols, names in specs:
        print(f"\n  -- {label} --")
        vd = df_s[cols].copy()

        vm = VAR(vd)
        lo = vm.select_order(maxlags=8)
        bl = max(lo.aic, 1)
        print(f"  Optimal lag (AIC) = {lo.aic}  ->  using {bl}")

        vf = vm.fit(maxlags=bl, ic="aic")
        print(f"  Lags={vf.k_ar}  nobs={vf.nobs}  AIC={vf.aic:.2f}  BIC={vf.bic:.2f}")

        fitted = vf.fittedvalues
        r2s = {}
        for ei, en in enumerate(names):
            actual = vd.values[bl:, ei]
            pred = fitted.values[:, ei]
            r2 = _r_sq(actual, pred)
            r2s[en] = round(r2, 4)
            print(f"    R2({en}) = {r2:.4f}")

        resid_ok = True
        for ei, en in enumerate(names):
            lb = acorr_ljungbox(vf.resid.values[:, ei], lags=[12], return_df=True)
            p = lb["lb_pvalue"].iloc[0]
            ok = p > 0.05
            if not ok:
                resid_ok = False
            print(f"    LB({en}, l=12) p={p:.4f}  {'OK' if ok else 'AUTOCORR'}")

        results["var"][label] = {
            "lag": vf.k_ar, "nobs": vf.nobs,
            "aic": round(vf.aic, 2), "bic": round(vf.bic, 2),
            "residuals_ok": resid_ok, "r_squared": r2s}

        n_p = 12
        irf = vf.irf(n_p)
        pp = plot_impulse_responses(irf, names, n_p)
        results["var"][label]["impulse_response_plot"] = pp
        print(f"  IRF -> {pp}")

        fevd = vf.fevd(n_p)
        print(f"\n  FEVD at {n_p}-month horizon (prop. of variance explained by each shock):")
        for vi, vn in enumerate(names):
            parts = []
            for si, sn in enumerate(names):
                val = fevd.decomp[si, -1, vi]
                parts.append(f"{sn}: {val:.1%}")
            print(f"    {vn}:  {'  '.join(parts)}")

        cum = irf.cum_effects
        print(f"\n  Cumulative {n_p}m response to 1 SD shock:")
        for si, sn in enumerate(names):
            r = cum[-1, :, si]
            ls = "  ".join(f"{names[j]}: {r[j]:.4f}" for j in range(len(names)))
            print(f"    Shock {sn}:  {ls}")

    # ── 4. SAVE ─────────────────────────────────────────────────
    pd.DataFrame(results["stationarity"]).to_csv(
        OUTPUT_DIR / "stationarity_tests.csv", index=False)
    pd.DataFrame(results["granger"]).to_csv(
        OUTPUT_DIR / "granger_causality.csv", index=False)

    jp = OUTPUT_DIR / "econometric_results.json"
    jp.write_text(
        json.dumps(results, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8")

    print(f"\n{'=' * 66}")
    print(f"All results -> {OUTPUT_DIR}")
    print("=" * 66)


if __name__ == "__main__":
    main()
