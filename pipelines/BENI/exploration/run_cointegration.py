#!/usr/bin/env python3
"""Cointegration analysis: Johansen test on TF-IDF, BBD, CPI, FX in levels."""
from __future__ import annotations

import json, sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

import numpy as np
import pandas as pd
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.stattools import adfuller

TFIDF_PATH = _HERE/"outputs/07_tfidf_index/beni_tfidf_index.csv"
BBD_PATH = _HERE/"outputs/06_bbd_index/beni_bbd_index.csv"
MACRO_DIR = _PIPELINES/"BENI/data/raw/macro"
OUTPUT_DIR = _HERE/"outputs/07_tfidf_index/econometric"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def _parse_imf_period(p: str) -> str:
    parts = p.split("-M")
    return f"{parts[0]}-{parts[1].zfill(2)}"

# Load
tfidf = pd.read_csv(TFIDF_PATH)
tfidf["month"] = pd.to_datetime(tfidf["year_month"]+"-01")
bbd = pd.read_csv(BBD_PATH)
bbd["month"] = pd.to_datetime(bbd["year_month"]+"-01")
fx = pd.read_csv(MACRO_DIR/"fx_bdt_usd_bis_eop_monthly.csv")
fx["month"] = pd.to_datetime(fx["TIME_PERIOD"]+"-01")
fx = fx[["month","OBS_VALUE"]].rename(columns={"OBS_VALUE":"fx_bis"}).dropna()
cpi = pd.read_csv(MACRO_DIR/"cpi_imf_bgd_index_monthly.csv")
cpi = cpi[cpi["OBS_VALUE"].notna()].copy()
cpi["month"] = pd.to_datetime(cpi["TIME_PERIOD"].map(_parse_imf_period)+"-01")
cpi = cpi[["month","OBS_VALUE"]].rename(columns={"OBS_VALUE":"cpi"})

df = tfidf.merge(bbd, on="month").merge(fx, on="month").merge(cpi, on="month")
df = df.sort_values("month").reset_index(drop=True)
print(f"Data: {len(df)} months ({df['month'].min().date()} – {df['month'].max().date()})")

# Johansen cointegration tests on different variable sets
tests = [
    ("TF-IDF + CPI + FX",     ["tfidf_index", "cpi", "fx_bis"]),
    ("BBD + CPI + FX",         ["beni_index", "cpi", "fx_bis"]),
    ("TF-IDF + BBD + CPI+FX", ["tfidf_index", "beni_index", "cpi", "fx_bis"]),
]

results = {}
for label, cols in tests:
    data = df[cols].dropna().values
    n, k = data.shape
    
    # Johansen test with constant (det_order=0) and lag 1-4
    for lag in [1, 2, 3, 4]:
        try:
            jres = coint_johansen(data, det_order=0, k_ar_diff=lag)
            # Trace statistic
            trace_stat = jres.lr1
            trace_crit = jres.cvt[:, 1]  # 5% critical values
            trace_crit_1 = jres.cvt[:, 0]  # 1%
            
            n_r = k
            n_ce = sum(trace_stat > trace_crit)
            n_ce_1 = sum(trace_stat > trace_crit_1)
            
            key = f"{label} (lag={lag})"
            results[key] = {
                "variables": cols,
                "lag": lag,
                "n": n,
                "n_ce_5pct": int(n_ce),
                "n_ce_1pct": int(n_ce_1),
                "trace_stats": [round(t, 2) for t in trace_stat],
                "crit_5pct": [round(c, 2) for c in trace_crit],
                "crit_1pct": [round(c, 2) for c in trace_crit_1],
            }
            
            # Print
            print(f"\n  {key}")
            print(f"    Sample: {n} obs, {k} variables")
            print(f"    H0: r=0..{k-1} cointegrating vectors")
            for r in range(k):
                sig = "<" if trace_stat[r] < trace_crit[r] else ">"
                print(f"      r<={r}: trace={trace_stat[r]:.2f}  "
                      f"5%={trace_crit[r]:.2f}  ({sig})  "
                      f"1%={trace_crit_1[r]:.2f}")
            print(f"    -> {int(n_ce)} coint vectors (5%), {int(n_ce_1)} (1%)")
            
        except Exception as e:
            print(f"  {label} (lag={lag}): ERROR: {e}")

# Save
Path(OUTPUT_DIR/"cointegration.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False, default=str),
    encoding="utf-8")
print(f"\nResults -> {OUTPUT_DIR/'cointegration.json'}")
