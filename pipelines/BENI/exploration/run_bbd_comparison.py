#!/usr/bin/env python3
"""Compare BBD vs TF-IDF nowcasting performance + robustness checks."""

from __future__ import annotations
import json, sys, warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.api import VAR

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

OUTPUT = _HERE / "outputs/07_tfidf_index/econometric/bbd_comparison"
OUTPUT.mkdir(parents=True, exist_ok=True)

TFIDF_PATH = _HERE / "outputs/07_tfidf_index/beni_tfidf_index.csv"
BBD_PATH = _HERE / "outputs/06_bbd_index/beni_bbd_index.csv"
MACRO_DIR = _PIPELINES / "BENI/data/raw/macro"

# ── load data ────────────────────────────────────────────────────
tfidf = pd.read_csv(TFIDF_PATH)
bbd = pd.read_csv(BBD_PATH)

cpi = pd.read_csv(MACRO_DIR / "cpi_imf_bgd_index_monthly.csv")
cpi["month"] = pd.to_datetime(cpi["TIME_PERIOD"].str.replace("-M", "-"))
cpi = cpi.sort_values("month").reset_index(drop=True)

fx = pd.read_csv(MACRO_DIR / "fx_bdt_usd_bis_eop_monthly.csv")
fx["month"] = pd.to_datetime(fx["TIME_PERIOD"])
fx = fx.sort_values("month").reset_index(drop=True)

# ── merge into analysis dataset ──────────────────────────────────
df = tfidf[["year_month", "tfidf_index"]].copy()
df = df.merge(bbd[["year_month", "beni_index"]], on="year_month", how="inner")
df["month"] = pd.to_datetime(df["year_month"])
df = df.sort_values("month")
df = df.merge(cpi[["month", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "cpi"}), on="month", how="left")
df = df.merge(fx[["month", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "fx"}), on="month", how="left")

# Exclude 2014 (low coverage)
df = df[df["month"] >= "2015-01-01"].copy().reset_index(drop=True)

# Log-differences (stationarity)
for col in ["tfidf_index", "beni_index", "cpi", "fx"]:
    df[f"dl{col[:4]}"] = np.log(df[col]).diff() * 100

df_valid = df.dropna(subset=["dltfid", "dlbeni", "dlcpi", "dlfx"]).reset_index(drop=True)
n_total = len(df_valid)

print(f"Analysis sample: {n_total} months ({df_valid['month'].iloc[0].date()} – {df_valid['month'].iloc[-1].date()})")

# ── nowcasting comparison function ───────────────────────────────
def evaluate_nowcast(vars_list, var_names, label, n_test=24, max_lag=4):
    """Run expanding window nowcast, return metrics dict."""
    results = {"label": label, "vars": var_names}
    for lag in range(1, max_lag + 1):
        y = df_valid[vars_list].values
        y_actual = df_valid["dlcpi"].values
        n = len(y)
        n_train_init = n - n_test

        fcast_var = np.full(n, np.nan)
        fcast_rw = np.full(n, np.nan)

        for i in range(n_test):
            train_end = n_train_init + i
            if train_end < lag + 5:
                continue
            try:
                y_train = y[:train_end]
                v = VAR(y_train)
                vf = v.fit(lag)
                f = vf.forecast(y_train, steps=1)
                cpi_idx = vars_list.index("dlcpi")
                fcast_var[train_end] = f[0, cpi_idx]
            except Exception:
                pass
            fcast_rw[train_end] = y_actual[train_end - 1]

        valid = ~np.isnan(fcast_var) & ~np.isnan(y_actual)
        idx = np.where(valid)[0]

        if len(idx) < 6:
            results[f"lag{lag}"] = {"n": int(len(idx)), "error": "insufficient OOS"}
            continue

        ya = y_actual[idx]
        yv = fcast_var[idx]
        yr = fcast_rw[idx]

        rmse_var = float(np.sqrt(np.mean((ya - yv) ** 2)))
        rmse_rw = float(np.sqrt(np.mean((ya - yr) ** 2)))
        mae_var = float(np.mean(np.abs(ya - yv)))
        mae_rw = float(np.mean(np.abs(ya - yr)))

        e1 = (ya - yv) ** 2
        e2 = (ya - yr) ** 2
        d = e1 - e2
        dm_stat = float(np.mean(d) / (np.std(d, ddof=1) / np.sqrt(len(d))))
        dm_pval = float(2 * (1 - stats.norm.cdf(abs(dm_stat))))

        improvement = (1 - rmse_var / rmse_rw) * 100

        results[f"lag{lag}"] = {
            "n": int(len(idx)),
            "rmse_var": rmse_var,
            "rmse_rw": rmse_rw,
            "mae_var": mae_var,
            "mae_rw": mae_rw,
            "dm_stat": dm_stat,
            "dm_pval": dm_pval,
            "improvement_pct": improvement,
            "var_wins": bool(rmse_var < rmse_rw),
        }

        # Store forecast paths for best lag (lag=1 default)
        if lag == 1:
            results["_fcast_var"] = fcast_var
            results["_fcast_rw"] = fcast_rw
            results["_y_actual"] = y_actual
            results["_idx_oos"] = idx

    return results


# ── Run all models ───────────────────────────────────────────────
print("\n" + "=" * 60)
print("NOWCASTING COMPARISON: BBD vs TF-IDF")
print("=" * 60)

models = [
    evaluate_nowcast(["dltfid", "dlcpi", "dlfx"], ["dltfid", "dlcpi", "dlfx"],
                     "TF-IDF VAR"),
    evaluate_nowcast(["dlbeni", "dlcpi", "dlfx"], ["dlbeni", "dlcpi", "dlfx"],
                     "BBD VAR"),
    evaluate_nowcast(["dltfid", "dlbeni", "dlcpi", "dlfx"],
                     ["dltfid", "dlbeni", "dlcpi", "dlfx"],
                     "TF-IDF + BBD VAR"),
    evaluate_nowcast(["dlcpi", "dlfx"], ["dlcpi", "dlfx"],
                     "Macro-only VAR (no narrative)"),
]

# ── Print comparison table (lag=1) ───────────────────────────────
print(f"\nOut-of-sample nowcasting results (24-month expanding window, VAR(1)):\n")
print(f"  {'Model':<30s} {'RMSE':>8s} {'MAE':>8s} {'vs RW':>8s} {'DM p':>8s}")
print(f"  " + "-" * 62)
for m in models:
    r = m.get("lag1", {})
    if "rmse_var" in r:
        imp = f"{r['improvement_pct']:+.1f}%"
        sig = "***" if r["dm_pval"] < 0.01 else "**" if r["dm_pval"] < 0.05 else "*" if r["dm_pval"] < 0.10 else ""
        print(f"  {m['label']:<30s} {r['rmse_var']:>8.4f} {r['mae_var']:>8.4f} {imp:>8s} {r['dm_pval']:>7.4f}{sig}")
    else:
        print(f"  {m['label']:<30s} {'N/A':>8s} {'N/A':>8s} {'N/A':>8s} {'N/A':>8s}")

print(f"\n  Random walk benchmark: RMSE={models[0].get('lag1', {}).get('rmse_rw', 0):.4f}")

# ── Comparison plot ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
best_model = models[0]  # TF-IDF as reference
if "_idx_oos" in best_model:
    idx = best_model["_idx_oos"]
    months = df_valid["month"].iloc[idx]
    actual = best_model["_y_actual"][idx]

    ax.plot(months, actual, "k-", label="Actual Dlog CPI", linewidth=1.5)

    colors = ["steelblue", "darkorange", "forestgreen", "crimson"]
    for mi, m in enumerate(models):
        if "_idx_oos" in m and np.array_equal(m["_idx_oos"], idx):
            ax.plot(months, m["_fcast_var"][idx], "--", color=colors[mi],
                    label=f"{m['label']}", linewidth=1, alpha=0.8)

    ax.plot(months, best_model["_fcast_rw"][idx], "r:", label="Random walk", linewidth=1, alpha=0.6)

ax.set_title("Out-of-sample nowcasting: BBD vs TF-IDF vs Macro-only", fontsize=12)
ax.set_ylabel("Dlog CPI (%)")
ax.legend(fontsize=8, ncol=2)
ax.axhline(y=0, color="grey", linestyle="-", linewidth=0.3)
plt.tight_layout()
plt.savefig(OUTPUT / "bbd_comparison_nowcast.png", dpi=150)
plt.close()
print(f"\n  -> {OUTPUT / 'bbd_comparison_nowcast.png'}")

# ── Robustness: all lags comparison ──────────────────────────────
print(f"\n" + "=" * 60)
print("ROBUSTNESS: RMSE across VAR lags")
print("=" * 60)
print(f"\n  {'Model':<30s} {'Lag=1':>8s} {'Lag=2':>8s} {'Lag=3':>8s} {'Lag=4':>8s}")
print(f"  " + "-" * 62)
for m in models:
    row = [m["label"]]
    for lag in range(1, 5):
        r = m.get(f"lag{lag}", {})
        if "rmse_var" in r:
            row.append(f"{r['rmse_var']:.4f}")
        else:
            row.append("  N/A  ")
    print(f"  {row[0]:<30s} {row[1]:>8s} {row[2]:>8s} {row[3]:>8s} {row[4]:>8s}")

# Best lag per model
print(f"\n  Best lag per model:")
for m in models:
    best_lag = None
    best_rmse = float("inf")
    for lag in range(1, 5):
        r = m.get(f"lag{lag}", {})
        if "rmse_var" in r and r["rmse_var"] < best_rmse:
            best_rmse = r["rmse_var"]
            best_lag = lag
    if best_lag:
        print(f"    {m['label']:<30s} lag={best_lag}, RMSE={best_rmse:.4f}")

# ── Robustness: sub-period stability ─────────────────────────────
print(f"\n" + "=" * 60)
print("ROBUSTNESS: Sub-period stability")
print("=" * 60)

def subperiod_eval(vars_list, label, start_year, end_year, lag=1):
    sub = df_valid[(df_valid["month"] >= f"{start_year}-01-01") &
                   (df_valid["month"] < f"{end_year}-01-01")].copy().reset_index(drop=True)
    if len(sub) < 24:
        return None
    y = sub[vars_list].values
    y_actual = sub["dlcpi"].values
    n = len(y)
    n_test = min(12, n // 3)
    n_train = n - n_test

    fcast = np.full(n, np.nan)
    for i in range(n_test):
        train_end = n_train + i
        if train_end < lag + 5:
            continue
        try:
            yt = y[:train_end]
            v = VAR(yt).fit(lag)
            f = v.forecast(yt, steps=1)
            cpi_idx = vars_list.index("dlcpi")
            fcast[train_end] = f[0, cpi_idx]
        except:
            pass

    valid = ~np.isnan(fcast) & ~np.isnan(y_actual)
    idx = np.where(valid)[0]
    if len(idx) < 6:
        return None

    ya = y_actual[idx]
    yv = fcast[idx]

    # RW benchmark within subperiod
    yr = np.full_like(yv, np.nan)
    for t in range(len(idx)):
        if idx[t] > 0:
            yr[t] = y_actual[idx[t] - 1]

    yr_valid = ~np.isnan(yr)
    if sum(yr_valid) < 6:
        return None

    rmse_var = np.sqrt(np.mean((ya[yr_valid] - yv[yr_valid]) ** 2))
    rmse_rw = np.sqrt(np.mean((ya[yr_valid] - yr[yr_valid]) ** 2))

    return {
        "n": len(sub), "n_test": len(idx),
        "rmse_var": float(rmse_var), "rmse_rw": float(rmse_rw),
        "improvement": float((1 - rmse_var / rmse_rw) * 100),
    }

subperiods = [
    ("2015", "2020", "Pre-COVID (2015-2019)"),
    ("2019", "2024", "Full later period (2019-2024)"),
    ("2017", "2024", "Second half (2017-2024)"),
]

for label_only, vars_list in [("TF-IDF", ["dltfid", "dlcpi", "dlfx"]),
                               ("BBD", ["dlbeni", "dlcpi", "dlfx"]),
                               ("Macro-only", ["dlcpi", "dlfx"])]:
    print(f"\n  {label_only}:")
    for sy, ey, period_label in subperiods:
        r = subperiod_eval(vars_list, label_only, sy, ey)
        if r:
            print(f"    {period_label:<30s} VAR RMSE={r['rmse_var']:.4f}, RW={r['rmse_rw']:.4f}, "
                  f"Δ={r['improvement']:+.1f}% (n_test={r['n_test']})")
        else:
            print(f"    {period_label:<30s} insufficient data")

# ── Diebold-Mariano pairwise comparison ──────────────────────────
print(f"\n" + "=" * 60)
print("PAIRWISE COMPARISON (Diebold-Mariano, VAR(1))")
print("=" * 60)

pairs = [("TF-IDF", "BBD"), ("TF-IDF", "Macro-only"),
         ("BBD", "TF-IDF"), ("BBD", "Macro-only"),
         ("Macro-only", "TF-IDF"), ("Macro-only", "BBD")]

# Get forecasts from each model
fcasts = {}
for m in models:
    if "lag1" in m and "rmse_var" in m["lag1"] and "_idx_oos" in m:
        fcasts[m["label"]] = m["_fcast_var"][m["_idx_oos"]]

if len(fcasts) >= 2:
    print()
    for m1, m2 in pairs:
        if m1 in fcasts and m2 in fcasts and len(fcasts[m1]) == len(fcasts[m2]):
            d = (fcasts[m1] - models[0]["_y_actual"][models[0]["_idx_oos"]]) ** 2 - \
                (fcasts[m2] - models[0]["_y_actual"][models[0]["_idx_oos"]]) ** 2
            dm = np.mean(d) / (np.std(d, ddof=1) / np.sqrt(len(d)))
            pv = 2 * (1 - stats.norm.cdf(abs(dm)))
            sig = "***" if pv < 0.01 else "**" if pv < 0.05 else "*" if pv < 0.10 else ""
            better = m1 if np.mean(d) < 0 else m2
            print(f"  {m1} vs {m2}: DM={dm:.3f}, p={pv:.4f}{sig} → {better} wins")
    print()

# ── Save all results ─────────────────────────────────────────────
output_results = {}
for m in models:
    label = m["label"]
    output_results[label] = {}
    for lag in range(1, 5):
        r = m.get(f"lag{lag}", {})
        if "rmse_var" in r:
            output_results[label][f"lag{lag}"] = {k: v for k, v in r.items()
                                                   if not k.startswith("_")}

with open(OUTPUT / "bbd_comparison_results.json", "w") as f:
    json.dump(output_results, f, indent=2)

print(f"  -> {OUTPUT / 'bbd_comparison_results.json'}")
print("\n✅ DONE")
