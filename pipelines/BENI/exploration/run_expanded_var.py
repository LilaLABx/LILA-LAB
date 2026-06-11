#!/usr/bin/env python3
"""Expanded VAR with global price controls + GDP nowcasting exercise."""

from __future__ import annotations
import json, sys, warnings
from pathlib import Path
from datetime import datetime

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

# ── config ──────────────────────────────────────────────────────────
EXCLUDE_2014 = True          # exclude low-coverage 2014 months
OUTPUT = _HERE / "outputs/07_tfidf_index/econometric/expanded"
OUTPUT.mkdir(parents=True, exist_ok=True)

TFIDF_PATH = _HERE / "outputs/07_tfidf_index/beni_tfidf_index.csv"
BBD_PATH = _HERE / "outputs/06_bbd_index/beni_bbd_index.csv"
MACRO_DIR = _PIPELINES / "BENI/data/raw/macro"
FAO_PATH = _PIPELINES / "BENI/data/external/fao_food_price_index.csv"

# ── load helpers ────────────────────────────────────────────────────
def _parse_imf_period(p: str) -> str:
    parts = p.split("-M")
    return f"{parts[0]}-{parts[1].zfill(2)}"

def parse_fao_date(d: str) -> datetime:
    """Parse FAO date formats: 1990-01 or Jan-90 or 2014-01."""
    d = d.strip()
    if len(d) == 7 and d[0].isdigit():
        return datetime.strptime(d, "%Y-%m")
    elif len(d) == 6 and d[0].isalpha():
        return datetime.strptime(d, "%b-%y")
    raise ValueError(f"Cannot parse FAO date: {d}")

# ── load data ───────────────────────────────────────────────────────
print("="*60)
print("LOADING DATA")
print("="*60)

# TF-IDF
tfidf = pd.read_csv(TFIDF_PATH)
tfidf["month"] = pd.to_datetime(tfidf["year_month"]+"-01")

# BBD
bbd = pd.read_csv(BBD_PATH)
bbd["month"] = pd.to_datetime(bbd["year_month"]+"-01")

# FX
fx = pd.read_csv(MACRO_DIR / "fx_bdt_usd_bis_eop_monthly.csv")
fx["month"] = pd.to_datetime(fx["TIME_PERIOD"]+"-01")
fx = fx[["month", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "fx_bis"}).dropna()

# CPI
cpi = pd.read_csv(MACRO_DIR / "cpi_imf_bgd_index_monthly.csv")
cpi = cpi[cpi["OBS_VALUE"].notna()].copy()
cpi["month"] = pd.to_datetime(cpi["TIME_PERIOD"].map(_parse_imf_period)+"-01")
cpi = cpi[["month", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "cpi"})

# FAO Food Price Index (2014-2016=100 base)
fao = pd.read_csv(FAO_PATH, header=None, skiprows=4)  # skip title + base annotation + header + NaN row
fao = fao.iloc[:, :7]
fao.columns = ["Date", "Food", "Meat", "Dairy", "Cereals", "Oils", "Sugar"]
fao = fao[fao["Date"].notna()].copy()
fao["month"] = fao["Date"].apply(parse_fao_date)
for c in ["Food", "Meat", "Dairy", "Cereals", "Oils", "Sugar"]:
    fao[c] = pd.to_numeric(fao[c], errors="coerce")
fao = fao.dropna(subset=["Food"])
print(f"FAO data: {len(fao)} months ({fao['month'].min().date()} – {fao['month'].max().date()})")

# Merge
df = tfidf.merge(bbd, on="month").merge(fx, on="month").merge(cpi, on="month")
# merge fao
df = df.merge(fao[["month", "Food", "Meat", "Dairy", "Cereals", "Oils", "Sugar"]], on="month", how="left")
df = df.sort_values("month").reset_index(drop=True)

if EXCLUDE_2014:
    df = df[df["month"] >= "2015-01-01"].copy()

df = df.dropna().reset_index(drop=True)
print(f"Analysis sample: {len(df)} months ({df['month'].iloc[0].date()} – {df['month'].iloc[-1].date()})")
print(f"\nVariables: {list(df.columns)}")
print(df[["month", "tfidf_index", "beni_index", "cpi", "fx_bis", "Food"]].head())

# ── transformations ────────────────────────────────────────────────
print("\n" + "="*60)
print("TRANSFORMATIONS & STATIONARITY")
print("="*60)

df["dlcpi"] = df["cpi"].pct_change() * 100  # monthly inflation %
df["d2lcpi"] = df["dlcpi"].diff()           # acceleration
df["dlfx"] = df["fx_bis"].pct_change() * 100
df["dltfidf"] = df["tfidf_index"].pct_change() * 100
df["dlbbd"] = df["beni_index"].pct_change() * 100
df["dlfood"] = df["Food"].pct_change() * 100
df["dlcereals"] = df["Cereals"].pct_change() * 100
df["dloils"] = df["Oils"].pct_change() * 100

df_valid = df.dropna().reset_index(drop=True)
print(f"Full sample (after differencing): {len(df_valid)} obs")

# ── EXPANDED VAR GRANGER CAUSALITY ─────────────────────────────────
print("\n" + "="*60)
print("EXPANDED VAR WITH GLOBAL FOOD PRICE CONTROLS")
print("="*60)

from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.stats.stattools import durbin_watson

# We estimate VAR on [dltfidf, dlcpi, dlfx, dlfood]
# This adds global food price changes as an endogenous variable
endog_vars = ["dltfidf", "dlcpi", "dlfx", "dlfood"]
endog = df_valid[endog_vars].values

# Find optimal lag
maxlags = 6
results_aic = []
for lag in range(1, maxlags+1):
    try:
        mod = VAR(endog)
        res = mod.fit(lag)
        results_aic.append((lag, res.aic))
    except:
        pass

best_lag = min(results_aic, key=lambda x: x[1])[0] if results_aic else 2
print(f"\nOptimal lag (AIC): {best_lag}")
for lag, aic in results_aic:
    print(f"  Lag {lag}: AIC={aic:.2f}")

# Estimate VAR with best lag
var_expanded = VAR(endog)
var_res = var_expanded.fit(best_lag)
print(f"\nVAR({best_lag}) summary:")
print(var_res.summary())

# Granger tests in expanded system
print(f"\n── Granger Causality (expanded VAR({best_lag})) ──")
granger_results = {}
for cause_idx, cause_name in enumerate(endog_vars):
    for effect_idx, effect_name in enumerate(endog_vars):
        if cause_idx == effect_idx:
            continue
        try:
            # H0: cause does NOT Granger-cause effect
            test = var_res.test_causality(caused=effect_idx, causing=cause_idx, kind="wald")
            pval = test.pvalue
            stat = test.test_statistic
            granger_results[f"{cause_name} → {effect_name}"] = {
                "stat": float(stat),
                "pvalue": float(pval),
                "sig_5pct": bool(pval < 0.05),
                "sig_10pct": bool(pval < 0.10),
            }
            sig = "***" if pval < 0.01 else "**" if pval < 0.05 else "*" if pval < 0.10 else ""
            print(f"  {cause_name:>10s} → {effect_name:<10s}  χ²={float(stat):.3f}, p={float(pval):.4f} {sig}")
        except Exception as e:
            print(f"  {cause_name:>10s} → {effect_name:<10s}  ERROR: {e}")

# ── FEVD for expanded VAR ──────────────────────────────────────────
print(f"\n── FEVD (forecast error variance decomposition) ──")
fevd_horizons = [1, 3, 6, 12]
fevd_results = {}
for h in fevd_horizons:
    try:
        fevd = var_res.fevd(h)
        # fevd.decomp has shape (neqs, periods, neqs): decomp[var_idx, period, shock_idx]
        for var_idx, var_name in enumerate(endog_vars):
            fevd_results[f"h={h},{var_name}"] = {}
            for shock_idx, shock_name in enumerate(endog_vars):
                val = fevd.decomp[var_idx, h-1, shock_idx]  # h-1 because 0-indexed
                fevd_results[f"h={h},{var_name}"][f"from_{shock_name}"] = float(val)
    except Exception as e:
        print(f"  FEVD error: {e}")

# Print key FEVD findings
print("  - Variance Decomposition of dltfidf (narrative index):")
for h in fevd_horizons:
    key12m = f"h={h},dltfidf"
    if key12m in fevd_results:
        own = fevd_results[key12m]["from_dltfidf"]
        food = fevd_results[key12m]["from_dlfood"]
        print(f"    h={h}: own={own:.1%}, from_global_food={food:.1%}")

# ── Impulse Response for expanded VAR ──────────────────────────────
print(f"\n── Generating IRF plots ──")
irf = var_res.irf(20)
irf_fig, irf_axes = plt.subplots(4, 4, figsize=(14, 10))
irf_fig.suptitle(f"Expanded VAR({best_lag}) Impulse Responses\nwith Global Food Price Controls", fontsize=13, y=1.01)

# Manually plot IRF using irf values
irf_vals = irf.irfs  # shape (periods+1, neqs, neqs) — impulse[shock, response, t]
n_periods = irf_vals.shape[0]
for i, cause in enumerate(endog_vars):
    for j, effect in enumerate(endog_vars):
        ax = irf_axes[i, j]
        ax.plot(range(n_periods), irf_vals[:, j, i], color="steelblue", linewidth=1.0)
        ax.set_title(f"{cause} → {effect}", fontsize=8)
        ax.axhline(y=0, color="grey", linestyle="--", linewidth=0.5)
        ax.tick_params(labelsize=6)

plt.tight_layout()
plt.savefig(OUTPUT / "expanded_var_irf.png", dpi=150, bbox_inches="tight")
plt.close(irf_fig)
print(f"  -> {OUTPUT/'expanded_var_irf.png'}")

# ── COMPARE: VAR with vs without global food prices ────────────────
print(f"\n── Comparing VAR fit: with vs without global food ──")
# Baseline VAR: [dltfidf, dlcpi, dlfx]  (no food)
endog_base = df_valid[["dltfidf", "dlcpi", "dlfx"]].values
var_base = VAR(endog_base)
var_base_res = var_base.fit(best_lag)
base_aic = var_base_res.aic
expanded_aic = var_res.aic
print(f"  VAR without global food: AIC={base_aic:.2f}")
print(f"  VAR with global food:    AIC={expanded_aic:.2f}")
aic_diff = expanded_aic - base_aic
if aic_diff < 0:
    print(f"  Expanded VAR (with food) improved fit: ΔAIC={aic_diff:.2f}")
else:
    print(f"  Base VAR (without food) has better fit: ΔAIC=+{aic_diff:.2f} (lower is better)")

# ── OUT-OF-SAMPLE NOWCASTING (VAR-based) ───────────────────────────
print(f"\n" + "="*60)
print("OUT-OF-SAMPLE NOWCASTING EVALUATION")
print("="*60)
print("\n  Method: Recursive 1-step-ahead VAR forecasts")
print("  Target: Dlog CPI (monthly inflation rate)")
print("  Evaluation: RMSE of VAR vs. RW benchmark\n")

# Walk-forward 1-step-ahead forecasts
nw_lag = min(best_lag, 4)
n_total = len(df_valid)
n_test = 24  # last 24 months for out-of-sample
n_train_init = n_total - n_test  # initial training window size

var_fcast_vars = ["dltfidf", "dlcpi", "dlfx", "dlfood"]
y_actual = df_valid["dlcpi"].values
fcast_var = np.full(n_total, np.nan)
fcast_rw = np.full(n_total, np.nan)  # random walk = last observation

# Expanding window: start with n_train_init, predict 1 step, expand, repeat
for i in range(n_test):
    train_end = n_train_init + i  # train on 0..train_end-1, predict train_end
    if train_end < nw_lag + 5:
        continue

    try:
        y_train = df_valid.iloc[:train_end][var_fcast_vars].values
        v = VAR(y_train)
        vf = v.fit(nw_lag)
        f = vf.forecast(y_train, steps=1)
        fcast_var[train_end] = f[0, 1]  # dlcpi index=1
    except:
        pass

    # RW forecast (last observed dlcpi)
    fcast_rw[train_end] = y_actual[train_end - 1]

# Evaluate — use all non-NaN predictions
valid_oos = ~np.isnan(fcast_var) & ~np.isnan(y_actual)
idx_oos = np.where(valid_oos)[0]

if len(idx_oos) >= 6:
    y_act = y_actual[idx_oos]
    y_var = fcast_var[idx_oos]
    y_rw = fcast_rw[idx_oos]

    rmse_var = np.sqrt(np.mean((y_act - y_var)**2))
    rmse_rw = np.sqrt(np.mean((y_act - y_rw)**2))
    mae_var = np.mean(np.abs(y_act - y_var))
    mae_rw = np.mean(np.abs(y_act - y_rw))

    # Diebold-Mariano test
    e1 = (y_act - y_var)**2
    e2 = (y_act - y_rw)**2
    d = e1 - e2
    dm_stat = np.mean(d) / (np.std(d, ddof=1) / np.sqrt(len(d)))
    dm_pval = 2 * (1 - stats.norm.cdf(abs(dm_stat)))

    print(f"  Out-of-sample period: {len(idx_oos)} months")
    print(f"  ┌─────────────────────┬──────────┬──────────┐")
    print(f"  │ Metric              │ VAR      │ RW       │")
    print(f"  ├─────────────────────┼──────────┼──────────┤")
    print(f"  │ RMSE                │ {rmse_var:.4f}  │ {rmse_rw:.4f}  │")
    print(f"  │ MAE                 │ {mae_var:.4f}  │ {mae_rw:.4f}  │")
    print(f"  │ DM statistic        │ {dm_stat:.3f}  │ (ref)    │")
    print(f"  │ DM p-value          │ {dm_pval:.4f}  │ (ref)    │")
    print(f"  └─────────────────────┴──────────┴──────────┘")

    if rmse_var < rmse_rw:
        print(f"  ✅ VAR nowcast beats random walk by {(1-rmse_var/rmse_rw)*100:.1f}%")
    else:
        print(f"  ❌ RW beats VAR nowcast by {(1-rmse_rw/rmse_var)*100:.1f}%")

    # Plot
    fig, ax = plt.subplots(figsize=(12, 5))
    months = df_valid["month"].iloc[idx_oos]
    ax.plot(months, y_act, "k-", label="Actual Dlog CPI", linewidth=1.5)
    ax.plot(months, y_var, "b--", label=f"VAR({nw_lag}) nowcast", linewidth=1)
    ax.plot(months, y_rw, "r:", label="Random walk", linewidth=1)
    ax.set_title("Out-of-sample nowcasting: Monthly inflation rate", fontsize=12)
    ax.set_ylabel("Dlog CPI (%)")
    ax.legend(fontsize=9)
    ax.axhline(y=0, color="grey", linestyle="-", linewidth=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT / "nowcasting_oos_plot.png", dpi=150)
    plt.close()
    print(f"  -> {OUTPUT/'nowcasting_oos_plot.png'}")

else:
    print(f"  Insufficient OOS data ({len(idx_oos)} obs)")

# ── CUMULATIVE IMPULSE RESPONSE COMPARISON ─────────────────────────
print(f"\n── Cumulative IRF: Shock to narrative → inflation path ──")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for ax_i, (label, color, varying) in enumerate([
    ("Without global food (Base VAR)", "steelblue", ["dltfidf", "dlcpi", "dlfx"]),
    ("With global food (Expanded VAR)", "darkorange", ["dltfidf", "dlcpi", "dlfx", "dlfood"]),
]):
    ax = axes[ax_i]
    if label.startswith("Without"):
        y = df_valid[varying].values
        vv = VAR(y)
        vr = vv.fit(best_lag)
    else:
        y = df_valid[varying].values
        vv = VAR(y)
        vr = vv.fit(best_lag)

    irf_obj = vr.irf(20)
    cum = np.cumsum(irf_obj.irfs[:, 0, 1])  # cumulative response of dlcpi to dltfidf shock
    ax.plot(range(len(cum)), cum, color=color, linewidth=1.5)
    ax.axhline(y=0, color="grey", linestyle="--", linewidth=0.5)
    ax.set_title(label, fontsize=9)
    ax.set_xlabel("Months after shock")
    ax.set_ylabel("Cumulative Δ in Dlog CPI (%)")

plt.suptitle("Cumulative Response of Inflation to TF-IDF Narrative Shock", fontsize=11)
plt.tight_layout()
plt.savefig(OUTPUT / "cumulative_irf_comparison.png", dpi=150)
plt.close()
print(f"  -> {OUTPUT/'cumulative_irf_comparison.png'}")

# ── Save results ───────────────────────────────────────────────────
print(f"\n── Saving results ──")
results = {
    "sample": {
        "n_months": len(df_valid),
        "start": str(df_valid["month"].iloc[0].date()),
        "end": str(df_valid["month"].iloc[-1].date()),
    },
    "var_expanded": {
        "best_lag": int(best_lag),
        "aic": float(var_res.aic),
        "base_aic": float(base_aic) if 'base_aic' in dir() else None,
        "variables": endog_vars,
    },
    "granger_causality": granger_results,
    "fevd": fevd_results,
}

if len(idx_oos) >= 6:
    results["nowcasting"] = {
        "n_test": len(idx_oos),
        "rmse_var": float(rmse_var) if 'rmse_var' in dir() else None,
        "rmse_rw": float(rmse_rw) if 'rmse_rw' in dir() else None,
        "mae_var": float(mae_var) if 'mae_var' in dir() else None,
        "mae_rw": float(mae_rw) if 'mae_rw' in dir() else None,
        "dm_stat": float(dm_stat) if 'dm_stat' in dir() else None,
        "dm_pval": float(dm_pval) if 'dm_pval' in dir() else None,
    }

with open(OUTPUT / "expanded_var_results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)

print(f"  -> {OUTPUT/'expanded_var_results.json'}")
print("\n✅ DONE")
