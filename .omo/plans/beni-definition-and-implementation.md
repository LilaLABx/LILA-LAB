# BENI Definition & Implementation Plan

**Project**: Bangla Economic Narrative Index  
**Covers**: Phase 5 (BENI Integration) + Phase 6 (Real Data Validation)  
**Status**: 📋 Planned  
**Date**: June 6, 2026  
**Author**: Sisyphus (from systematic exploration)

---

## Table of Contents
1. [BENI Definition](#1-beni-definition)
2. [Architecture Overview](#2-architecture-overview)
3. [Phase 5: BENI Integration Dashboard](#3-phase-5-beni-integration-dashboard)
4. [Phase 6: Real Bengali News Data Validation](#4-phase-6-real-bengali-news-data-validation)
5. [Implementation Work Breakdown](#5-implementation-work-breakdown)
6. [Validation Protocol](#6-validation-protocol)
7. [Success Criteria](#7-success-criteria)
8. [Files to Create / Modify](#8-files-to-create--modify)

---

## 1. BENI Definition

### What BENI Is

A **native Bangla economic narrative index** that measures how macroeconomic meaning is constructed, spread, and intensified across Bangla newspaper sections. It is:

- **Not** a translation of English sentiment methods into Bangla
- **Not** another generic Bangla news classifier
- A **section-aware narrative index** that tracks how economic topics migrate from technical reporting (Economy section) into political blame (Politics), household burden (National), external shock (International), and moral interpretation (Editorial)

### Novel Contributions (from JER systematic review gap analysis)

1. **First Bangla Economic Narrative Index** — fills 265M speaker gap (0% non-English coverage in literature)
2. **Sectional Migration Score** (novel) — tracks when/if economic topics leave the Economy section and enter other frames
3. **Narrative Regime Detection** — identifies shifts in dominant narrative frames (e.g., monetary → trade → growth)
4. **Cross-Source Convergence** — measures when multiple outlets converge on similar framing of the same macro issue
5. **Geographic gap validation** — first South Asian economic sentiment index using native-language text

### Core Hypotheses

| # | Hypothesis | Test |
|---|-----------|------|
| H1 | **Sectional Migration** — Economic narratives become socially salient when they migrate from Economy pages into National/Politics/Editorial | Entropy of topic distribution across sections over time |
| H2 | **Blame Intensification** — Same economic topic carries stronger blame/crisis language in Politics/Editorial than in Economy | Narrative force lexicon scores × section |
| H3 | **Household Burden** — Inflation/food-price narratives are more negative in National sections than in Economy | Sentiment polarity × section |
| H4 | **External Dependence** — Exchange-rate/reserves narratives are framed through external-shock language rather than domestic policy | Topic-source coupling analysis |
| H5 | **Narrative Lead** — BENI narrative pressure leads official macro indicators (CPI, exchange rate, reserves) by 2-8 weeks | Granger causality, cross-correlation |

---

## 2. Architecture Overview

### 6-Layer Pipeline

```
┌─────────────────────────────────────┐
│ L1: CORPUS                          │
│ Potrika (2014-2020, 6 newspapers)    │
│ + Prothom Alo / Daily Star (scrape) │
│ → article_id, date, source,          │
│   section, headline, body            │
└────────────┬────────────────────────┘
             ▼
┌─────────────────────────────────────┐
│ L2: ECONOMIC FILTER                 │
│ BanglaBERT fine-tuned for           │
│ economic relevance classification    │
│ (trained on 300-500 human labels)   │
│ + keyword fallback                   │
└────────────┬────────────────────────┘
             ▼
┌─────────────────────────────────────┐
│ L3: MULTI-ATTRIBUTE EXTRACTION      │
│ ┌─────────────────────────────┐     │
│ │ (a) Economic Topic          │     │
│ │ inflation, exchange_rate,   │     │
│ │ reserves, banking, fiscal,  │     │
│ │ trade, employment, growth   │     │
│ └─────────────────────────────┘     │
│ ┌─────────────────────────────┐     │
│ │ (b) Narrative Force         │     │
│ │ crisis, burden, blame,      │     │
│ │ reform, stability,          │     │
│ │ uncertainty, resilience     │     │
│ └─────────────────────────────┘     │
│ ┌─────────────────────────────┐     │
│ │ (c) Valuation Target        │     │
│ │ government, central_bank,   │     │
│ │ banks, businesses,          │     │
│ │ market_actors, households,  │     │
│ │ global_economy              │     │
│ └─────────────────────────────┘     │
│ ┌─────────────────────────────┐     │
│ │ (d) Sentiment Polarity      │     │
│ │ negative, neutral, positive │     │
│ │ (SentiBangla + BanglaBERT)  │     │
│ └─────────────────────────────┘     │
└────────────┬────────────────────────┘
             ▼
┌─────────────────────────────────────┐
│ L4: TIME-SERIES AGGREGATION         │
│ Bi-weekly periods (80-100 arts/     │
│ period — optimal for Bangladesh)    │
│ ├── Domain activation vectors        │
│ ├── Narrative shift detection        │
│ ├── Cross-period similarity          │
│ └── Sentiment × domain pressure      │
└────────────┬────────────────────────┘
             ▼
┌─────────────────────────────────────┐
│ L5: INDEX CONSTRUCTION (NOVEL)      │
│ Sub-indices:                         │
│ ├─ BENI-Inflation Pressure          │
│ ├─ BENI-Exchange Rate Pressure      │
│ ├─ BENI-Banking/Financial Stress    │
│ ├─ BENI-External Sector             │
│ ├─ BENI-Uncertainty                 │
│ └─ BENI-Aggregate (dynamic factor)  │
│                                      │
│ Novel metrics:                       │
│ ├─ Sectional Migration Score         │
│ ├─ Narrative Regime Indicator        │
│ └─ Cross-Source Convergence Index   │
└────────────┬────────────────────────┘
             ▼
┌─────────────────────────────────────┐
│ L6: VALIDATION                      │
│ Against: CPI, exchange rate,        │
│ reserves, remittances, policy rate  │
│ ├─ AR(1) baseline                   │
│ ├─ AR(1) + BENI                     │
│ ├─ MIDAS regression                  │
│ ├─ Diebold-Mariano test             │
│ └─ Granger causality analysis       │
└─────────────────────────────────────┘
```

### Model Selection Rationale

| Layer | Primary Model | Alternative | Rationale |
|-------|--------------|-------------|-----------|
| Economic relevance | **BanglaBERT** | XLM-R, MuRIL | Best RMSE in replications (+31.5%), native Bangla pretraining |
| Topic extraction | BanglaBERT multi-label | TF-IDF + LR (baseline) | Replication-proven, interpretable baseline available |
| Narrative force | **Bangla lexicon + embedding** | BERTopic (exploratory) | Lexicon provides interpretability; BERT adds semantic depth |
| Sentiment | SentiBangla + BanglaBERT | VADER-Bangla adaptation | Dictionary baseline + transformer refinement |
| Time-series | **Bi-weekly aggregation** | Weekly (if >100 arts/wk) | MODEL 2 from comparison — optimal for 40-50 arts/wk |
| Index construction | Dynamic factor model | Simple average | Accounts for correlated sub-indices |

---

## 3. Phase 5: BENI Integration Dashboard

### Goal
Integrate the existing BENI pilot (TF-IDF + lexicons) with the replications framework (BERT/RoBERTa benchmarks) into a unified comparison dashboard.

### Current State
- `_prep/beni_experiment/beni_pilot/` — working TF-IDF + lexicon pipeline
- `replications/` — 8 replicated models with meta-analysis
- `replications/results/meta_analysis_synthesis.json` — benchmark numbers
- Streamlit dashboard exists but only shows BENI pilot

### Deliverables

#### D5.1: Unified Benchmark Table
| Method | RMSE Impr. | Accuracy | F1 | Interpretability | Speed | Data Need |
|--------|-----------|----------|-----|-----------------|-------|-----------|
| Tetlock (dictionary) | +7.52% | 67.5% | — | High | Fast | Low |
| Gentzkow (EPU) | -6.68% | 100% | — | High | Fast | Low |
| SVM | 0% | 100% | 100% | Medium | Medium | Moderate |
| Random Forest | 0% | 100% | 100% | Medium | Medium | Moderate |
| XGBoost | 0% | 100% | 100% | Low | Medium | Moderate |
| LSTM | +28.5% | 71.5% | 67.1% | Low | Slow | High |
| **BERT** | **+31.5%** | **68.5%** | **62.3%** | **Low** | **Slow** | **High** |
| RoBERTa | +30.5% | 69.5% | 65.9% | Low | Slow | High |
| **BENI (TF-IDF)** | baseline | 89.4% | 0.86 | **High** | **Fast** | Low |
| **BENI (BanglaBERT)** | TBD | TBD | TBD | Medium | Medium | High |

#### D5.2: Interactive Dashboard
- Tab 1: Model comparison (all 8 replications + BENI)
- Tab 2: Time-series view of domain activation
- Tab 3: Sectional migration visualization (when data available)
- Tab 4: Narrative shift timeline
- Export: publication-ready tables + figures

#### D5.3: Reproducibility Extension
- Add BENI to the reproducibility checklist
- Document BENI assumptions alongside replication assumptions
- Seed control, deterministic preprocessing, walk-forward validation

### Tasks

| # | Task | File(s) | Effort |
|---|------|---------|--------|
| 5.1 | Create `beni_benchmark.py` — run all 8 replicas + BENI on common test set | `replications/beni_benchmark.py` | 1 day |
| 5.2 | Create unified results table with BENI row | `replications/results/beni_comparison.json` | 0.5 day |
| 5.3 | Enhance dashboard with comparison tab | `_prep/beni_experiment/beni_pilot/dashboard.py` | 1 day |
| 5.4 | Add reproducibility docs for BENI | `replications/era4_validation_framework.py` | 0.5 day |
| 5.5 | Write `BENI_INTEGRATION_REPORT.md` | `replications/BENI_INTEGRATION_REPORT.md` | 0.5 day |

---

## 4. Phase 6: Real Bengali News Data Validation

### Goal
Replace synthetic data with real Bengali news, build ground-truth labels, fine-tune BanglaBERT, construct sub-indices, and validate against Bangladesh macroeconomic indicators.

### Current State
- Synthetic data only for replications
- Weak keyword labels for BENI pilot (4.4% positive, 45% precision)
- BanglaNLP news categorization dataset (no Economy class)
- Potrika identified but **not yet downloaded** (#1 blocker)
- Manual Bangla lexicons written (8 topics, 7 forces, 7 targets)

### Deliverables

#### D6.1: Real Bengali News Corpus
- **Potrika dataset** (664K articles, 8 categories, 2014-2020, 6 newspapers)
- Fallback: BARD (2,500 articles, 5 categories)
- Target: 10,000+ date-stamped articles across Economy, Politics, National, International sections

#### D6.2: Ground-Truth Labels
- 300-500 manually annotated articles
- Columns: article_id, source, date, section, headline, text, economic_relevance, topic, narrative_force, valuation_target, sentiment, notes
- Inter-annotator agreement check (Cohen's κ ≥ 0.7)

#### D6.3: BanglaBERT Fine-tuned Models
- `beni_economic_relevance_bert/` — binary classifier
- `beni_topic_bert/` — 8-class topic classifier (multi-label)
- `beni_narrative_bert/` — narrative force classifier (7-class)
- Evaluation: macro-F1, calibration curves, temporal robustness

#### D6.4: BENI Sub-Indices
- Time series (bi-weekly, 2014-2020+)
- BENI-Inflation Pressure Index
- BENI-Exchange Rate Pressure Index
- BENI-Banking Stress Index
- BENI-External Sector Index
- BENI-Uncertainty Index
- BENI-Aggregate Index (dynamic factor)

#### D6.5: Sectional Migration Analysis
- Cross-section entropy over time
- Narrative force × section interaction
- Source convergence metrics

#### D6.6: Macroeconomic Validation
- Against Bangladesh CPI, exchange rate, reserves, remittances, policy rate
- AR(1) vs. AR(1) + BENI comparison
- MIDAS regression for mixed-frequency nowcasting
- Diebold-Mariano significance tests
- Granger causality (supporting evidence)
- Narrative lead quantification (weeks)

### Tasks

| # | Task | File(s) | Effort |
|---|------|---------|--------|
| 6.1 | Download Potrika from Mendeley (manual: 10.17632/v362rp78dc.4) | `_prep/beni_experiment/data/raw/potrika/` | 0.5 day |
| 6.2 | Run potrika.py export for all sections | `_prep/beni_experiment/beni_pilot/potrika.py` | 0.5 day |
| 6.3 | Create 300-500 article annotation sheet | `_prep/beni_experiment/data/annotations/beni_annotation_sheet.csv` | 2 days |
| 6.4 | Fine-tune BanglaBERT for relevance, topic, narrative | `_prep/beni_experiment/beni_pilot/train_bert.py` (new) | 3 days |
| 6.5 | Build time-series aggregation pipeline | `_prep/beni_experiment/beni_pilot/time_series_index.py` (new) | 2 days |
| 6.6 | Implement sectional migration score | `_prep/beni_experiment/beni_pilot/sectional_migration.py` (new) | 1.5 days |
| 6.7 | Construct BENI sub-indices | `_prep/beni_experiment/beni_pilot/beni_indices.py` (new) | 1.5 days |
| 6.8 | Download Bangladesh macro data (CPI, FX, reserves) | `_prep/beni_experiment/data/macro/` | 0.5 day |
| 6.9 | Build validation pipeline | `_prep/beni_experiment/beni_pilot/validate.py` (new) | 2 days |
| 6.10 | Write validation report | `_prep/beni_experiment/REAL_DATA_VALIDATION_REPORT.md` | 1 day |

---

## 5. Implementation Work Breakdown

### Phase 5 (Week 1)

```
Week 1, Day 1:
  [ ] Download Potrika manually from Mendeley
  [ ] Place under data/raw/potrika/
  [ ] Export sections via potrika.py (Economy, Politics, National, International)

Week 1, Day 2:
  [ ] Train BanglaBERT economic relevance classifier on Potrika
  [ ] Create annotation sheet (first 100 articles for pilot)

Week 1, Day 3:
  [ ] Build time-series aggregation pipeline
  [ ] Build bi-weekly domain vectors

Week 1, Day 4:
  [ ] Implement sectional migration score
  [ ] Compute cross-section entropy

Week 1, Day 5:
  [ ] Construct BENI sub-indices
  [ ] Write first index to CSV/json
```

### Phase 6 (Week 2-3)

```
Week 2, Day 1-2:
  [ ] Annotate 300-500 articles (manual + review)
  [ ] Check inter-annotator agreement

Week 2, Day 3-4:
  [ ] Fine-tune BanglaBERT (economic relevance, topic, narrative force)
  [ ] Evaluate: macro-F1, calibration, temporal robustness

Week 2, Day 5:
  [ ] Integrate BanglaBERT into prediction pipeline
  [ ] Run full corpus through fine-tuned models

Week 3, Day 1-2:
  [ ] Download Bangladesh macro data (CPI, exchange rate, reserves)
  [ ] Build validation pipeline: AR vs AR+BENI, MIDAS, Diebold-Mariano

Week 3, Day 3-4:
  [ ] Sectional migration analysis
  [ ] Narrative lead quantification
  [ ] Granger causality tests

Week 3, Day 5:
  [ ] Compare BENI vs all 8 replications in unified dashboard
  [ ] Write comprehensive validation report
  [ ] Update PROJECT_STATUS.md
```

### Parallel Work Streams

Where possible, these streams run in parallel:

```
Stream A (Data):  6.1 → 6.2 → 6.3 (blocking — sequential)
Stream B (Model): 5.1 → 5.2 → 6.4 → 6.5 (can start after Potrika available)
Stream C (Index): 5.3 → 6.6 → 6.7 (can start after topics available)
Stream D (Validation): 6.8 → 6.9 → 6.10 (can start after indices available)
```

---

## 6. Validation Protocol

### Text Validation

| Criterion | Standard | Method |
|-----------|----------|--------|
| Train/test split | **By time, not random** | Train: 2014-2018, Test: 2019-2020 |
| Economic relevance F1 | Macro-F1 ≥ 0.80 | BanglaBERT vs. human labels |
| Topic accuracy | Macro-F1 ≥ 0.75 | 8-class topic classification |
| Narrative force | Macro-F1 ≥ 0.60 | 7-class (harder: subjective) |
| Calibration | Expected Calibration Error ≤ 0.05 | Reliability diagrams |
| Temporal robustness | ΔF1 ≤ 0.10 | Train early, test late |

### Economic Validation

| Test | BENI Target | Macro Comparator | Expected |
|------|------------|-----------------|----------|
| AR(1) vs AR(1)+BENI-Inflation | BENI-Inflation sub-index | CPI inflation (monthly) | +5-15% RMSE improvement |
| AR(1) vs AR(1)+BENI-Exchange | BENI-Exchange sub-index | USD/BDT exchange rate | +5-15% |
| AR(1) vs AR(1)+BENI-Reserves | BENI-External sub-index | Foreign reserves (USD) | +3-10% |
| MIDAS nowcasting | BENI-Aggregate | CPI (monthly on weekly news) | RMSE improvement |
| Diebold-Mariano | All sub-indices vs AR | — | p < 0.10 |
| Granger causality | Narrative force → macro | CPI, FX, reserves | p < 0.10 |
| Narrative lead | Shift detection → policy | Policy rate changes | 2-8 week lead |

### Publication Bias Mitigation

- Report ALL null results explicitly
- Pre-register validation protocol before running tests
- Report both with/without BENI, not just relative improvement
- Use Diebold-Mariano (not just RMSE comparisons)
- Compare against strong baselines (ARIMA, not just AR(1))
- Document data preprocessing decisions before seeing results

---

## 7. Success Criteria

### Must-Have (Phase 5)

- [ ] Unified comparison table: 8 replications + BENI in one view
- [ ] BENI dashboard enhanced with comparison tab
- [ ] At least 2 sub-indices constructed on real data
- [ ] Reproducibility checklist extended for BENI

### Must-Have (Phase 6)

- [ ] Potrika dataset downloaded and processed
- [ ] 300+ human annotations with inter-annotator agreement ≥ 0.7
- [ ] BanglaBERT fine-tuned for economic relevance
- [ ] At least 3 BENI sub-indices with bi-weekly time series
- [ ] Sectional migration score implemented
- [ ] Validation against CPI and exchange rate
- [ ] At least 1 statistically significant narrative lead finding

### Nice-to-Have

- [ ] Real-time scraping pipeline for Prothom Alo / Daily Star
- [ ] Cross-source convergence metric
- [ ] Interactive dashboard with time-series controls
- [ ] BENI as predictor for policy rate changes
- [ ] Comparison against English-language Bangladesh news sentiment

---

## 8. Files to Create / Modify

### New Files

| File | Purpose |
|------|---------|
| `replications/beni_benchmark.py` | Run all replicas + BENI on common test set |
| `_prep/beni_experiment/beni_pilot/train_bert.py` | Fine-tune BanglaBERT for BENI tasks |
| `_prep/beni_experiment/beni_pilot/time_series_index.py` | Bi-weekly aggregation + index construction |
| `_prep/beni_experiment/beni_pilot/sectional_migration.py` | Cross-section entropy + migration metrics |
| `_prep/beni_experiment/beni_pilot/beni_indices.py` | Sub-index construction + dynamic factor model |
| `_prep/beni_experiment/beni_pilot/validate.py` | Macroeconomic validation pipeline |
| `_prep/beni_experiment/data/annotations/beni_annotation_sheet.csv` | Human annotation template |
| `replications/BENI_INTEGRATION_REPORT.md` | Phase 5 deliverable |
| `_prep/beni_experiment/REAL_DATA_VALIDATION_REPORT.md` | Phase 6 deliverable |

### Modified Files

| File | Change |
|------|--------|
| `_prep/beni_experiment/beni_pilot/dashboard.py` | Add comparison tab + sub-index visualization |
| `replications/era4_validation_framework.py` | Extend reproducibility checklist for BENI |
| `PROJECT_STATUS.md` | Update with Phase 5-6 progress |
| `_prep/beni_experiment/beni_pilot/predict.py` | Add BanglaBERT as optional model backend |
| `_prep/beni_experiment/beni_pilot/config.py` | Add Potrika paths + BanglaBERT model config |
| `_prep/beni_experiment/beni_pilot/narrative.py` | Extend lexicons with validated terms |

---

## Decision Points (Require User Input)

1. **Potrika download** — Requires manual download from Mendeley (10.17632/v362rp78dc.4). No anonymous API access available. Need to download and place in `_prep/beni_experiment/data/raw/potrika/`.

2. **BanglaBERT vs. XLM-R vs. MuRIL** — BanglaBERT is the primary candidate from replications. If GPU constraints limit fine-tuning, fall back to XLM-R (requires less compute).

3. **Annotation scope** — 300 vs. 500 articles. 300 is minimum for reasonable fine-tuning. 500 is stronger. Annotator availability?

4. **Macro data source** — Bangladesh Bank publishes CPI, exchange rate, reserves monthly. Need to determine if API access or manual collection.

5. **Dashboard priority** — Streamlit (existing) vs. new framework. Keeping Streamlit is pragmatic.

6. **Sectional migration aggregation** — Per-article entropy vs. period-level distribution comparison. Period-level is more stable.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Potrika download fails | Medium | High (blocks data) | Fallback: BARD dataset (2.5K articles) or manual scrape |
| BanglaBERT fine-tuning requires GPU | Medium | Medium | Use XLM-R (smaller); or cloud GPU |
| Weak annotation quality | Medium | Medium | Inter-annotator agreement check; clear guidelines |
| Macro data unavailable at high frequency | High | Medium | Monthly data sufficient for MIDAS; report limitations |
| Synthetic-to-real performance drop | High | Medium | Report honestly; document distribution shift |
| No significant narrative lead found | Medium | Low | Still publishable (null result = important for field) |
