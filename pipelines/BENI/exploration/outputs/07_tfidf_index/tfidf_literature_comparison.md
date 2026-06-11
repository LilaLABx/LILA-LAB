# TF-IDF Narrative Index: Comparison with Existing Research

## 1. Overview

This document compares the **BENI TF-IDF Narrative Index** — a monthly index of economic
narrative attention constructed via supervised TF-IDF + Logistic Regression classification of
933,588 Bangla newspaper articles (2014–2024) — against the established literature on
text-based economic measurement.

---

## 2. Methodology Comparison

### 2.1 Baker, Bloom & Davis (2016) — Economic Policy Uncertainty (BBD)

| Dimension | BBD (2016) | BENI TF-IDF |
|---|---|---|
| **Approach** | Dictionary-based keyword counting | Supervised ML classification |
| **Core logic** | Article contains *economy* + *policy* + *uncertainty* terms | Article classified as *economy* vs *non-economy* by TF-IDF + LR |
| **Label source** | Human-audited keyword audit (12K articles) | Category labels from newspaper metadata |
| **Normalization** | Frequency scaling + standardization to mean 100 | Z-score normalization to mean 100, std 10 |
| **Construct** | Economic *policy uncertainty* | Economic *narrative attention share* |
| **Language** | English (10 US newspapers) | Bangla (7 Bangladeshi newspapers) |

**Our BBD replication** follows the original protocol: article-level triple-term matching,
newspaper-level standardization, and monthly aggregation. The BENI corpus achieves a
94.77% test accuracy for the TF-IDF economic relevance classifier, validating the supervised
approach against human-assigned category labels.

### 2.2 Shiller (2017) — Narrative Economics

Shiller's AEA presidential address argues that economic narratives spread like epidemics and
drive economic fluctuations. He calls for "serious quantitative study of changing popular
narratives" to understand business cycles.

**Our contribution:** The TF-IDF index directly answers Shiller's call. It quantifies the
*attention share* devoted to economic narratives in the Bangladeshi news ecosystem. Rather
than tracking specific storylines (Shiller's "contagion" model), we measure the aggregate
salience of economic topics relative to all news — a necessary first step for any narrative
economics program.

### 2.3 Thorsrud (2020) — "Words are the New Numbers"

| Dimension | Thorsrud (2020) | BENI TF-IDF |
|---|---|---|
| **Text source** | *Dagens Næringsliv* (Norwegian business daily) | 7 Bangladeshi newspapers |
| **Corpus size** | ~80K articles | 933K articles |
| **Method** | LDA topic model (80 topics) + time-varying DFM | TF-IDF + Logistic Regression |
| **Output** | Daily business cycle index | Monthly narrative attention index |
| **Target** | GDP nowcasting | Economic narrative share measurement |
| **Accuracy** | ROC analysis: near-perfect cycle classification | 94.77% test accuracy for economic relevance |

Thorsrud's innovation is the mixed-frequency dynamic factor model that extracts a business
cycle index from daily topic series and quarterly GDP. Our approach is simpler but more
directly interpretable: the TF-IDF index measures *how much of the news is about the economy
at any given time.*

### 2.4 Bybee, Kelly, Manela & Xiu (2020) — "The Structure of Economic News"

| Dimension | Bybee et al. (2020) | BENI TF-IDF |
|---|---|---|
| **Text source** | Wall Street Journal (1984–2017) | 7 Bangla newspapers (2014–2024) |
| **Corpus size** | ~800K articles | 933K articles |
| **Method** | LDA topic model (180 topics) → hierarchical meta-topics | TF-IDF + Logistic Regression (binary) |
| **Key metric** | Topic-level news attention allocation | Binary economic attention share |
| **Validation** | Tracks GDP, employment, inflation | 94.77% accuracy, comparison with BBD |

Bybee et al. find that news attention to specific topics (e.g., "Housing Market," "Federal
Reserve") tracks corresponding economic indicators and has forecasting power beyond
standard numerical predictors. Their topic model is richer (180 topics) but the core insight
is the same: **news attention allocation contains economically meaningful signal.**

Our binary classification is less granular but more scalable and directly interpretable as a
single economic narrative intensity measure.

---

## 3. Empirical Findings Comparison

### 3.1 TF-IDF Index vs BBD Index

| Metric | Full Sample (2014–2024) | Excluding 2014 (2015–2024) |
|---|---|---|
| **Contemporaneous correlation** | r = −0.44 | r = −0.55 |
| **Peak absolute correlation** | r = −0.60 (TF-IDF leads 3–5mo) | r = −0.61 (TF-IDF leads 5mo) |
| **Direction** | Negative | Negative |

**Interpretation:** TF-IDF and BBD indices are negatively correlated across all time horizons.
This is expected given their different constructs:

- **BBD index ↑** = More articles contain economy + policy + uncertainty terms
  → Elevated economic *uncertainty*
- **TF-IDF index ↓** = Fewer articles classified as economic
  → Reduced economic *attention share*

During crises (high uncertainty), media attention shifts to non-economic topics (war,
politics, health), reducing the share of economic content. During calm periods (low
uncertainty), routine economic coverage dominates a larger share of the news.

This inverse relationship is **strongest when TF-IDF leads BBD by 3–5 months**
(r = −0.60), suggesting that declining economic narrative attention may precede
spikes in measured economic policy uncertainty.

### 3.2 Macro-Pattern Alignment

| Period | TF-IDF Index | BBD Index | Macro Context |
|---|---|---|---|
| **2015–2016** | **High** (111–112) | Moderate (84–97) | Post-election stability, 7%+ GDP growth |
| **2017–2018** | Moderate → Low (97–107) | Moderate (94–106) | Election year, political tension |
| **2019** | Moderate (102) | Elevated (106) | Post-election, pre-COVID |
| **2020 (COVID)** | Moderate (106) | **Peak** (112) | Pandemic economic disruption |
| **2021–2022** | **Lowest** (88–93) | High (104–109) | Inflation crisis, Russia-Ukraine war, FX depletion |
| **2023–2024** | Low (89–93) | High (108–111) | Macroeconomic stress, reserve crisis |

**Key insight:** The COVID-19 period (2020) is the *only* episode where both indices are
simultaneously elevated. This makes sense: the pandemic was both an economic and
non-economic story — health coverage dominated, but the economic implications were
so severe that economic uncertainty *and* economic attention both rose.

### 3.3 Comparison with Bybee et al. (2020) Findings

Bybee et al. report that WSJ attention to "Macroeconomic News & Data" topics tracks
industrial production and that "Financial Markets" topics track stock market volatility.
Their topic-level attention series show **positive co-movement with many economic
indicators** — more attention to economic topics during expansions, less during
contractions.

Our TF-IDF index shows a different pattern in Bangladesh: economic attention was
highest during the stable growth period (2015–2016) and lowest during the inflation
crisis (2021–2022). This suggests that in an emerging economy context, **economic
narrative attention may be pro-cyclical** — rising during good times, falling during
crises when other news dominates.

This contrasts with Bybee et al.'s finding for the US, where the relationship is more
nuanced (specific topics track specific indicators). The difference may reflect:
1. Different media ecosystems (Bangla mass-market vs WSJ business-focused)
2. Different economic structures (emerging vs developed)
3. Our binary measure vs their 180-topic decomposition

### 3.4 Comparison with Thorsrud (2020) Findings

Thorsrud's Newsy Coincident Index (NCI) achieves near-perfect business cycle
classification for Norway using topic-adjusted news tone. His key finding is that
**news reduces noise** — textual data improves GDP nowcasting accuracy.

Our work does not yet perform nowcasting (that is a natural next step), but the
94.77% classification accuracy for economic relevance suggests that Bangla newspaper
text contains similarly rich economic signal. The temporal patterns in our TF-IDF index
align with known Bangladeshi macroeconomic events, supporting the validity of the
approach.

### 3.5 Comparison with Developing-Country BBD Adaptations

| Study | Country | Method | Period | Key Finding |
|---|---|---|---|---|
| Belhoula (2024) | Tunisia | BBD keyword | 2012–2022 | EPU predicts GDP decline, ↑ unemployment |
| Ilori et al. (2024) | Nigeria | BBD keyword (daily) | 2010–2023 | First daily EPU for Nigeria |
| Catacutan (2023) | Philippines | BBD keyword + human audit | 2017–2022 | Monetary policy uncertainty most impactful |
| **This study** | **Bangladesh** | **BBD keyword + TF-IDF ML** | **2014–2024** | **First dual-index approach for BD** |

All developing-country adaptations use pure BBD-style keyword counting. Our work is
**the first to combine keyword-based (BBD) and ML-based (TF-IDF) indices** for a
developing country, enabling comparison of uncertainty vs attention constructs.

---

## 4. Key Contributions to the Literature

### 4.1 What We Did Differently

1. **Supervised ML for economic narrative attention**: Rather than keyword counting, we
   train a classifier to recognize economic content. This captures a broader notion of
   "economic narrative" than keyword triples.

2. **Bangla language corpus**: First large-scale (933K articles) text-based economic
   index for Bangladesh using native-language content.

3. **Dual-index approach**: We construct both a BBD-style uncertainty index and a
   TF-IDF attention index, revealing their negative correlation and complementary
   nature.

4. **Full 7-newspaper coverage**: Unlike many developing-country studies that rely on
   1–3 sources, we cover 7 major Bangla newspapers spanning the ideological spectrum.

### 4.2 Validation Evidence

- **94.77% test accuracy** for TF-IDF economic relevance classification
- **Temporal alignment** with known macro events (COVID, inflation crisis, FX pressure)
- **Negative correlation with BBD** (r ≈ −0.55) consistent with theoretical expectation
- **Cross-method consistency**: Both indices show coherent patterns across Bangladesh's
  2014–2024 economic history

### 4.3 Caveats and Limitations

1. **2014 corpus coverage**: First 7 months have <500 articles/month — index values for
   2014 are unreliable (excluded from 2015+ analysis).
2. **Binary classification**: The TF-IDF approach collapses all "economic" content into
   one category, losing topic-level granularity that topic models provide.
3. **Label source**: Training labels come from newspaper section metadata, which may
   contain misclassifications.
4. **No nowcasting validation**: Unlike Thorsrud (2020) and Bybee et al. (2020), we
   have not yet validated against GDP or other macro indicators. That is the obvious
   next step.

---

## 5. References

- Baker, S. R., Bloom, N., & Davis, S. J. (2016). "Measuring Economic Policy Uncertainty."
  *Quarterly Journal of Economics*, 131(4), 1593–1636.
- Shiller, R. J. (2017). "Narrative Economics." *American Economic Review*, 107(4), 967–1004.
- Thorsrud, L. A. (2020). "Words are the New Numbers: A Newsy Coincident Index of the
  Business Cycle." *Journal of Business & Economic Statistics*, 38(2), 393–409.
- Bybee, L., Kelly, B. T., Manela, A., & Xiu, D. (2020). "The Structure of Economic News."
  NBER Working Paper No. 26648.
- Belhoula, M. M. (2024). "Economic Policy Uncertainty (EPU) in Emerging Countries:
  The Case of Tunisia." *Journal of Accounting and Finance in Emerging Economies*, 10(2).
- Ilori, et al. (2024). "A News-Based Economic Policy Uncertainty Index for Nigeria."
  *Quality & Quantity*.
- Catacutan, D. Q. (2023). "Measuring Economic Policy Uncertainty in the Philippines."
  BSP Economic Newsletter No. 23-04.
- Azqueta-Gavaldón, A. (2023). "Sources of Economic Policy Uncertainty in the Euro Area."
  *European Economic Review*.
