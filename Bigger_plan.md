# BENI Research Program: Synthesised and Refined PhD Roadmap

## 1. Core Identity

**Working program name:** Bangla Economic Narrative Index (BENI)

**Central research question:**  
Can local-language economic narratives in Bangla be measured reliably, and do they contain useful real-time information about macroeconomic conditions in Bangladesh?

This project should be framed as a measurement and applied-economics program, not as a generic NLP exercise. The core scientific object is:

> A reproducible, validated index system that converts Bangla economic news narratives into macroeconomically interpretable time-series indicators.

The strongest version of the PhD is now built around one completed foundation chain and two remaining empirical tests:

1. The completed systematic review establishes the gap in text-as-data research.
2. The completed BENI data/pipeline paper builds the local-language measurement infrastructure for Bangla economic narratives.
3. The next paper validates the index against inflation, exchange-rate pressure, reserves, and other macro indicators.
4. A nowcasting paper tests whether BENI improves real-time macroeconomic monitoring.
5. The full thesis synthesises these outputs into a broader argument about multilingual economic measurement.

## 2. Theoretical Spine

BENI needs a clear economics argument:

Economic agents do not observe the economy directly. They observe prices, employment conditions, policy signals, market stress, and media narratives. In a developing economy with delayed official data, a large informal sector, and thinner financial-market signals, local-language news can act as a high-frequency proxy for expectation pressure and institutional stress.

The project should be anchored in four literatures:

- **Narrative economics:** Shiller and related work on stories, expectations, and economic behaviour.
- **Text-as-data economics:** Tetlock; Baker, Bloom, and Davis; Gentzkow, Kelly, and Taddy.
- **Expectations and information frictions:** agents form beliefs from partial, noisy, mediated information.
- **Low-resource and multilingual NLP:** the methodological gap created by English-dominated models and datasets.

The central claim should be disciplined:

> BENI may improve measurement and nowcasting in Bangladesh because Bangla news captures local economic anxiety and policy narratives that official data and English-language sources miss.

Avoid overclaiming that news sentiment mechanically predicts the economy. The realistic contribution is incremental, interpretable, and policy-relevant measurement.

## 3. Research Outputs

### Foundation Paper: Completed Systematic Review of Economic Text-as-Data

**Status:** complete.  
**Role in program:** establishes the gap and motivates BENI.

**Core question:**  
What does the text-as-data literature show about predictive value, validation standards, publication bias, and language/geography gaps?

**Contribution:**

- Synthesises 66 papers and replication evidence.
- Shows that text-as-data value is real but uneven.
- Documents English and high-income-country dominance.
- Creates the justification for a Bangla-language economic narrative index.

**Program function:**  
This is now a completed foundation paper, not an active future deliverable. Its job is to supply the literature gap, methodological benchmark, and motivation for the BENI papers.

### Paper 1: BENI Data Paper and Local-Language Measurement Pipeline

**Working title:**  
*Building Local-Language Economic Narrative Indices: A Replicable Pipeline from Raw News to Validated Index*

**Status:** complete.  
**Role in program:** documents the dataset, corpus construction, and measurement infrastructure used by the remaining BENI papers.

**Core question:**  
How can a reliable economic narrative index be built in a low-resource language setting, and how much annotation is needed for credible measurement?

**Data:**

- Potrika Bangla news corpus.
- Weak labels from sections, keywords, and economic filters.
- LLM-assisted 300-article reference set with confidence and uncertainty checks.
- Macro indicators from public sources such as IMF, BIS, World Bank, and Bangladesh sources where available.

**Methods:**

- TF-IDF + Logistic Regression baseline.
- BanglaBERT or comparable transformer model.
- LLM-assisted annotation and active-learning/uncertainty review.
- Monthly index construction.
- Validation against CPI, food inflation, exchange rate, reserves, and other macro indicators.

**Main deliverables:**

- BENI v1 data release and documented corpus files.
- Reusable pipeline from raw Bangla news to analysis-ready economic narrative data.
- Dataset card, file schema, processing documentation, release manifest, and reproducibility materials.
- Documentation of uncertainty, source coverage, deduplication, data quality, and reproducibility choices.
- Foundation for the subsequent BENI validation and nowcasting papers.

**Key discipline:**  
Keep the data paper's claims centred on dataset construction, documentation, reproducibility, and measurement readiness. Do not overclaim downstream predictive value until the validation and nowcasting papers are complete.

### Paper 2: BENI as a Macroeconomic Indicator

**Working title:**  
*The Bangla Economic Narrative Index: Local-Language News Sentiment and Real-Time Macroeconomic Monitoring in Bangladesh*

**Role in program:** validates the instrument as an economic object.

**Core question:**  
Do Bangla economic narratives contain interpretable macroeconomic information?

**Index families:**

- Aggregate BENI sentiment or narrative pressure index.
- Inflation Pressure Index.
- Exchange-Rate and Reserves Pressure Index.
- Banking/Financial Stress Index.
- External Sector Index.
- Policy Uncertainty Index.

**Validation tests:**

- Lead-lag correlations.
- Level and first-difference correlations.
- Granger causality.
- Robustness across source-weighting schemes.
- Subperiod checks, especially pre-COVID versus COVID-period dynamics.
- Comparison against simple baselines and, where feasible, English-language indicators.

**Expected contribution:**  
The paper should show whether BENI captures long-run macro narrative regimes, short-run shocks, or both. A null result in first-differenced prediction is still useful if it is clearly interpreted.

### Paper 3: Inflation Nowcasting with BENI

**Working title:**  
*Nowcasting Inflation with the Bangla Economic Narrative Index: Local-Language News as a High-Frequency Economic Indicator*

**Role in program:** tests practical policy value.

**Core question:**  
Does BENI improve inflation nowcasting in Bangladesh compared with autoregressive and official-statistics-only benchmarks?

**Methods:**

- AR/ARIMA baseline.
- ARIMAX or dynamic regression with BENI.
- MIDAS regression if mixed-frequency data are used.
- Recursive pseudo-real-time forecasting.
- Diebold-Mariano or Clark-West tests where sample size permits.
- Asymmetry test for inflation accelerations versus decelerations.

**Primary test:**  
Compare forecast performance with and without BENI for:

- same-month nowcast,
- one-month-ahead forecast,
- three-month-ahead forecast.

**Important constraint:**  
Final results should use the frozen BENI index from the pipeline paper. TF-IDF BENI can be used for drafting and prototyping, but the published paper should rerun results after the improved index is locked.

### Optional Synthesis Chapter or Later Review Paper

**Working title:**  
*Multilingual Text-as-Data for Economic Measurement: Lessons from BENI*

**Role in program:** optional synthesis, not a required next paper.

**Core question:**  
What does the BENI project imply for multilingual text-as-data, low-resource economic measurement, and LLM-assisted social-science pipelines?

**Contribution:**

- Connects the completed systematic review with the empirical BENI papers.
- Positions BENI as a concrete response to the language and geography gaps found in the review.
- Extracts general design principles for future local-language economic indices.
- Can become a thesis synthesis chapter, policy/methods essay, or later standalone review only if there is enough new material.

**Program function:**  
This should not distract from the BENI empirical papers. It is useful only if it strengthens the thesis narrative after the pipeline, validation, and nowcasting work are substantially complete.

## 4. Data Architecture

Each document in the BENI corpus should preserve:

- `article_id`
- `source`
- `publication_date`
- `title`
- `body_text`
- `url`
- `language`
- `section`
- `scrape_timestamp`
- `duplicate_group_id`
- `economic_relevance_score`
- `topic_or_narrative_label`
- `sentiment_or_pressure_score`
- `model_version`

The immediate source universe should prioritise:

- Prothom Alo
- The Daily Star
- Dhaka Tribune
- Financial Express
- New Age
- Business Standard Bangladesh, if archive quality is usable
- Bangladesh Bank statements and press releases
- Ministry of Finance budget and policy documents

The design should explicitly handle:

- Bangla-English code mixing.
- Duplicate and syndicated articles.
- Section labels that are noisy proxies for economic relevance.
- Political stories with direct economic consequences.
- Source imbalance, where high-volume outlets dominate raw article counts.

## 5. Index Design

BENI should not be only a sentiment index. It should be a narrative measurement system.

Recommended index layers:

1. **Economic attention:** share of news classified as economically relevant.
2. **Narrative prevalence:** share of economic news in each theme.
3. **Narrative pressure:** sentiment or stress score within each theme.
4. **Composite BENI:** source-balanced aggregate of attention, prevalence, and pressure.

Candidate sub-indices:

- Inflation and price pressure.
- Exchange-rate and reserve pressure.
- Banking and financial stress.
- Employment and wage anxiety.
- Energy and import pressure.
- Export, garments, and external demand.
- Fiscal and policy uncertainty.

Aggregation should compare at least three specifications:

- article-weighted monthly index,
- source-balanced monthly index,
- topic-weighted or factor-model index.

The source-balanced version should be treated as the default unless testing shows that raw article weighting is more stable and interpretable.

## 6. Validation Standard

The project should be judged by whether it creates a credible economic measurement tool. Minimum validation standards:

- Baseline comparison against simple keyword/dictionary methods.
- Model comparison between TF-IDF and transformer approaches.
- Clear train/test separation.
- No look-ahead bias in index construction.
- Frozen model versions for final validation.
- External validation against macro indicators.
- Rolling or pseudo-real-time tests for forecasting papers.
- Explicit reporting of null or weak results.

Target macro variables:

- CPI inflation.
- Food inflation.
- BDT/USD exchange rate.
- Foreign-exchange reserves.
- Import payments.
- Export receipts.
- Remittances.
- Policy rate or monetary-policy stance.
- Industrial production proxy, if usable.

## 7. Timeline and Dependencies

### Phase A: Consolidation and Corpus Freeze

**Target:** June 2026  
**Status:** complete.  
**Deliverables:**

- Freeze source list and corpus version.
- Document data cleaning, deduplication, and filtering.
- Produce the frozen BENI v1 corpus and index-ready monthly data.
- Confirm macro data sources and date ranges.

### Phase B: BENI Pipeline Paper

**Target:** June-July 2026  
**Status:** complete as the BENI v1 data/pipeline paper.  
**Deliverables:**

- Freeze and document the BENI v1 corpus.
- Package data, documentation, schema, release materials, and reproducibility files.
- Complete the data/pipeline paper as the methodological foundation for the empirical BENI papers.

### Phase C: BENI Economic Validation Paper

**Target:** July-August 2026  
**Deliverables:**

- Finalise BENI sub-indices.
- Run macro validation tests.
- Write the BENI index paper around measurement and interpretability.

### Phase D: BENI Inflation Nowcasting Paper

**Target:** August-September 2026  
**Deliverables:**

- Build pseudo-real-time forecasting protocol.
- Compare AR/ARIMA benchmarks with BENI-augmented models.
- Test horizons h = 0, 1, and 3.
- Run asymmetry and domain-decomposition analyses.

### Phase E: Thesis Synthesis

**Target:** October-December 2026  
**Deliverables:**

- Integrate the completed systematic review with the BENI empirical papers.
- Write the thesis-level argument around multilingual economic measurement.
- Add a short synthesis chapter or later standalone essay only if it does not delay the BENI papers.

## 8. Contribution Hierarchy

The thesis should make five layered contributions:

1. **Gap contribution:** shows that economic text-as-data is still heavily English- and high-income-country biased.
2. **Data contribution:** creates a documented Bangla economic news corpus and annotation protocol.
3. **Measurement contribution:** builds BENI as a reproducible local-language narrative index.
4. **Economic contribution:** tests whether Bangla narratives contain macroeconomic information.
5. **Policy contribution:** evaluates BENI as a real-time nowcasting input for inflation and macro stress.

The safest claim is not that BENI will always beat official models. The stronger and more defensible claim is:

> BENI provides an interpretable, reproducible, local-language measurement layer that can be tested against macroeconomic outcomes and deployed for real-time monitoring.

## 9. Risks and Mitigations

| Risk | Why it matters | Mitigation |
|---|---|---|
| LLM labels are challenged | They are not independent human gold labels | Call them reference labels, report confidence and disagreement, add human adjudication if possible |
| Transformer models do not beat TF-IDF meaningfully | BanglaBERT gains may be small on short/news text | Treat the result as evidence about cost-effective low-resource pipelines |
| BENI correlates in levels but not differences | It may capture regimes rather than monthly shocks | Separate measurement, monitoring, and forecasting claims |
| Short macro sample weakens inference | Monthly Bangladesh data may be limited | Use conservative tests, bootstrap intervals, and report uncertainty |
| Source imbalance distorts the index | Large outlets can dominate raw counts | Use source-balanced aggregation as a main specification |
| COVID period drives results | 2020 may dominate correlations | Report pre-COVID and COVID-period checks separately |

## 10. Immediate Next Actions

1. Treat the completed systematic review and completed BENI v1 data/pipeline paper as fixed foundations.
2. Construct source-balanced monthly BENI and sub-indices from the frozen BENI v1 corpus.
3. Run validation against CPI, food inflation, exchange rate, reserves, and other available macro indicators.
4. Compare level, first-difference, lead-lag, and subperiod results.
5. Draft the BENI economic validation paper around measurement, interpretability, and external validity.
6. After the validation paper is stable, build the inflation nowcasting protocol using the frozen BENI index.
7. Compare AR/ARIMA benchmarks with BENI-augmented models for h = 0, 1, and 3.
8. Reserve the thesis synthesis chapter for integrating the completed review, completed data paper, validation paper, and nowcasting paper.

## 11. One-Sentence Thesis

This PhD builds and validates the first Bangla-language economic narrative index, showing how local-language news can be transformed into a reproducible measurement system for macroeconomic monitoring in a low-resource, developing-economy setting.
