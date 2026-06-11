# Paper 3: Nowcasting Inflation with a TF-IDF Narrative Index

**Full Title:** Nowcasting Inflation in Bangladesh Using a TF-IDF Narrative Index from Bangla News

**Status:** Active

---

This paper evaluates whether a simple TF-IDF-based narrative index from Bangla-language news contains predictive content for inflation (CPI) beyond traditional econometric models.

### Completed analysis

- **TF-IDF index**: 111 months (2015–2024), built from 933K Bangla news articles
- **Cointegration (Johansen)**: 1 cointegrating vector in 4-variable system (TF-IDF + BBD + CPI + FX) at all lags — long-run equilibrium
- **Granger causality**: CPI → narrative index (p=0.01), not reverse
- **Expanded VAR**: Global food prices add no explanatory power (ΔAIC = +1.62)
- **Nowcasting**: VAR beats random walk by 20.9% RMSE (DM p=0.0004) — 24-month out-of-sample

### Scripts & outputs

- `pipelines/BENI/exploration/run_cointegration.py` — Johansen tests
- `pipelines/BENI/exploration/run_expanded_var.py` — VAR, Granger, FEVD, nowcasting
- `pipelines/BENI/exploration/outputs/07_tfidf_index/econometric/` — all results

### Dependencies

- BENI v1 dataset (`dataset/BENI/beni-v1/`)
- Macro data: CPI, FX (Bangladesh Bank, BBS)
- FAO Food Price Index (exogenous control)
