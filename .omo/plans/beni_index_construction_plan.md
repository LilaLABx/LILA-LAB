# BENI Index Construction Plan

## Goal
Build the Bangla Economic Narrative Index (BENI) using 4 distinct methodologies
on the same corpus, benchmark each against real-world economic indicators, and
produce a systematic comparison.

---

## 1. Corpus and Preprocessing Variants

### Shared Cleaning (applied before all methods)
| Step | Detail |
|---|---|
| UTF-8 decoding + NFKC normalization | Merges composed/decomposed Bangla glyphs |
| Boilerplate removal | Datelines, bylines, source tags ("সংবাদ সংস্থা থেকে") |
| Deduplication | Same article across multiple newspapers on the same day |
| Whitespace normalization | Collapse multiple spaces, strip leading/trailing |

### Method-Specific Variants

```yaml
bbd:
  description: "Baker-Bloom-Davis style keyword counting"
  tokenizer: raw (whitespace split for word-boundary check)
  stopwords: false       # Economic keywords are content words
  stemming: false
  ngrams: false
  presets: [economy_terms, policy_terms, uncertainty_terms, sentiment_terms]

classical_ml:
  description: "TF-IDF + shallow models (LR, SVM, RF)"
  tokenizer: whitespace + । stripping
  stopwords: true
  stemming: false         # Bangla stemmers unreliable
  ngrams: bigrams (top 65K)
  feature: tfidf
  min_df: 5

deep_learning:
  description: "Subword embeddings + LSTM/transformer"
  tokenizer: bpe (BengaliBPE or sentencepiece, vocab 32K)
  stopwords: false        # Attention handles function words
  max_seq_length: 256
  embedding: fasttext | banglabert

llm:
  description: "LLM annotation + aggregation"
  tokenizer: whitespace (preserve full context)
  stopwords: false
  preserve_entities: true  # Underscore-join multi-word entities
  max_tokens: 4096
```

---

## 2. Method 1: BBD-Style Keyword Counting (Baseline)

### Approach
Count articles per month that contain pre-defined keywords from each category,
then normalize, standardize, and aggregate into an index.

### Categories and Seed Terms (to be expanded)

| Category | Example Bangla Terms | English |
|---|---|---|
| **Economy (E)** | অর্থনীতি, অর্থনৈতিক, বাণিজ্য, বাজার, শিল্প, ব্যবসা, মূল্যস্ফীতি, মুদ্রাস্ফীতি, জিডিপি, উৎপাদন, রপ্তানি, আমদানি, রাজস্ব, বিনিয়োগ | economy, trade, market, industry, business, inflation, GDP, production, export, import, revenue, investment |
| **Policy (P)** | নীতি, সরকার, সংসদ, আইন, বাজেট, নিয়ন্ত্রণ, কর, ভর্তুকি, সুদহার, মুদ্রানীতি | policy, government, parliament, law, budget, regulation, tax, subsidy, interest rate, monetary policy |
| **Narrative (N)** | অবস্থা, পরিস্থিতি, প্রবণতা, পরিবর্তন, সংকট, পুনরুদ্ধার, প্রবৃদ্ধি, মন্দা, স্থিতিশীল | situation, condition, trend, change, crisis, recovery, growth, recession, stable |
| **Sentiment (S)** | উন্নতি, অবনতি, বৃদ্ধি, হ্রাস, ইতিবাচক, নেতিবাচক, আশাবাদী, উদ্বেগজনক | improvement, deterioration, increase, decrease, positive, negative, optimistic, concerning |

### Index Construction

```
For each (newspaper, month):
  ratio = count(E ∩ N / total articles)  # economic narrative intensity
  ratio_sent = count(S+ / S-)            # sentiment direction
  
  # BENI narrative volume index
  std_ratio = ratio / σ_ratio(newspaper)  
  BENI_volume[t] = Σ(newspaper) w_np × std_ratio_np[t]

  # BENI sentiment index  
  BENI_sentiment[t] = Σ(newspaper) w_np × (count_positive - count_negative) / total[t]

Normalize: BENI[t] × (100 / mean(BENI over reference period))
```

### Validation
- **Benchmark correlation**: Pearson r between BENI and CPI, GDP, exchange rate, remittances
- **Event alignment**: Do spikes co-occur with known economic events (COVID, 2022 price shocks, political transitions)?
- **Baseline for comparison**: All other methods must beat this

---

## 3. Method 2: Classical ML (Feature-Based)

### Approach A — Supervised (if LLM annotations exist)
Train shallow models on LLM-annotated labels, then apply to full corpus.

### Approach B — Weakly Supervised
Use the BBD keyword articles as positive labels (distant supervision).

### Approach C — Unsupervised (Topic Model → Regression)

```python
# Pipeline
corpus → TF-IDF (unigrams + bigrams, min_df=5, max_features=50000)
       → Dimensionality reduction (SVD to 100 components)
       → Train/test split (temporal: train up to t, test on t+1...)
       → Models:
           - Elastic Net (L1/L2 regularization)
           - Random Forest (200 trees)
           - SVM (linear kernel)
           - Gradient Boosting (XGBoost/LightGBM)
       → Target variable: real economic indicator (e.g., CPI, IP)
       → Evaluation: out-of-sample R², directional accuracy
```

### Validation
| Metric | Detail |
|---|---|
| **Out-of-sample R²** | Train up to month t, predict t+1. Expand window sequentially. |
| **Directional accuracy** | % of months where predicted Δ matches actual Δ |
| **Feature importance** | Top TF-IDF terms with highest coefficients — do they make economic sense? |
| **Diebold-Mariano test** | Is ML significantly better than BBD baseline? |
| **Temporal cross-validation** | 5-fold time-series split (no random shuffling) |

### Expected Deliverable
Compare table: BBD vs LR vs SVM vs RF — R², DA, DM-statistic for each economic target.

---

## 4. Method 3: Deep Learning (Neural)

### Embedding Layer Options

| Embedding | Vocab | Why |
|---|---|---|
| **FastText (CBOW)** | 32K subword | Handles OOV; Bangla is morphologically rich |
| **BanglaBERT** | 128K BPE | Pretrained on 27.5 GB Bangla text |
| **XLM-RoBERTa** | 250K BPE | Multilingual, strong cross-lingual transfer |
| **mBERT** | 110K WordPiece | Common baseline for Indic tasks |

### Model Architectures

#### A) Document Embedding + Regression
```python
article → FastText avg → dense(128) → dropout(0.3) → linear → ΔCPI
```
- Pros: Simple, interpretable (word contributions)
- Cons: Bags-of-vectors loses word order

#### B) LSTM/GRU
```python
article → embedding → BiLSTM(128) → maxpool → dense(64) → linear
```
- Pros: Captures word order, phrase-level semantics
- Cons: Limited to ~512 tokens; 933K×512 becomes large

#### C) Fine-tuned Transformer
```python
article → BanglaBERT → [CLS] pool → dropout(0.1) → linear
```
- Train on (article → economic indicator) regression
- Use early stopping based on validation R²
- Batch size 16, AdamW lr=2e-5

### Validation
Same metrics as Classical ML, plus:
- **Ablation**: Does fine-tuning beat frozen embeddings?
- **Sequence length sensitivity**: Do longer articles improve predictions?
- **Compute cost**: Training time, inference time (for operationalization)
- **Layer analysis**: Which transformer layers encode the most economic signal?

---

## 5. Method 4: LLM-Based Annotation

### Approach

#### Phase A — Pilot (1,000 articles)
```python
for article in pilot_sample:
    prompt = f"""
    Rate this Bangla news article for economic relevance (0-5) and
    economic sentiment (-3 to +3).

    Article: {article}

    Output JSON:
    {{"relevance": int, "sentiment": int, "sector": str,
      "confidence": float, "reasoning": str}}
    """
    response = llm_api(prompt, model="claude-sonnet-4")
```
- Compute inter-annotator agreement between 2+ LLM runs (Cohen's κ)
- If κ < 0.6: refine prompt, add few-shot examples, retry

#### Phase B — Full Corpus Annotation
```python
for batch in chunks(articles, batch_size=100):
    annotated.extend(llm_batch_predict(batch))
```
- Checkpoint every 10K articles
- Track drift: does LLM behavior change over long runs?

#### Phase C — Index Construction
```python
monthly = annotated.groupby('month').agg({
    'sentiment': 'mean',
    'relevance': lambda x: (x >= 3).sum() / len(x),  # % highly relevant
    'sector': lambda x: x.mode()[0]                   # dominant sector
})
BENI_LLM = normalize(monthly['sentiment'] * monthly['relevance'])
```

### Validity Checks Specific to LLMs
| Check | What to test |
|---|---|
| **Consistency** | Annotate same article twice, compare scores. κ should be > 0.7 |
| **Order sensitivity** | Does article order in batch affect scores? |
| **Drift** | Does the LLM's scoring distribution change across months? |
| **Calibration** | Are confidence scores correlated with correctness? |
| **Prompt sensitivity** | Test 3 prompt variants: do they produce the same index? |

### LLM Candidate Models

| Model | Cost | Quality | Notes |
|---|---|---|---|
| Claude Sonnet 4 | $$$ | Highest | Best for Bengali text understanding |
| GPT-4o | $$$ | High | Comparable |
| Gemini 2.5 Pro | $$ | High | Good multilingual |
| Qwen2.5-72B | $ | Medium-High | Open source, self-hostable |

---

## 6. Benchmarks and Validation Framework

### 6.1 Target Economic Indicators for Bangladesh

| Indicator | Source | Frequency | Expected Lag | Notes |
|---|---|---|---|---|
| **CPI (Headline)** | BBS | Monthly | 0-1 month | Primary target |
| **CPI (Food)** | BBS | Monthly | 0-1 month | |
| **CPI (Non-Food)** | BBS | Monthly | 0-1 month | |
| **GDP Growth** | BBS | Quarterly | 1-3 months | Only 4 obs/year — noisy |
| **Industrial Production** | BBS | Monthly | 1-2 months | Best high-frequency real indicator |
| **Exchange Rate (BDT/USD)** | Bangladesh Bank | Daily→Monthly | 0 | Financial, reacts fast |
| **Remittances** | Bangladesh Bank | Monthly | 1 month | Key for Bangladesh economy |
| **Exports** | EPB | Monthly | 1 month | |
| **Imports** | EPB | Monthly | 1 month | |
| **Foreign Reserves** | Bangladesh Bank | Monthly | 0 | |
| **Call Money Rate** | Bangladesh Bank | Daily→Monthly | 0 | Financial |
| **Credit to Private Sector** | Bangladesh Bank | Monthly | 1-2 months | |
| **Stock Market Index (DSEX)** | DSE | Daily→Monthly | 0 | Financial, noisy |

### 6.2 Evaluation Protocol

```
For each economic indicator Y:
  For each BENI variant V in {BBD, Classical_ML, Deep_Learning, LLM}:
    For lag L in [0, 1, 2, 3]:
      r[V, L] = correlation(BENI_V[t-L], Y[t])
      dm[V, baseline] = Diebold-Mariano(BENI_V, baseline)

Report:
  - Best lag for each (variant × indicator)
  - Correlation matrix: variants × indicators × lags
  - Significance: which correlations survive Bonferroni correction?
  - DM test: which variants significantly beat BBD baseline?
```

### 6.3 Event-Based Validation

Known Bangladeshi economic events for manual validation:

| Date | Event | Expected Index Behavior |
|---|---|---|
| Mar 2020 | COVID-19 lockdown | Extreme negative sentiment, high economic narrative volume |
| 2021-2022 | Post-COVID recovery | Improving sentiment |
| Mar-Jun 2022 | Commodity price shock (Ukraine war) | Negative sentiment, inflation mentions spike |
| Jun 2022 | Fuel price hike (51.7%) | Negative sentiment, high volume |
| 2023-2024 | Forex reserve depletion | Negative narrative, exchange rate mentions |
| Jan 2024 | National election | Policy uncertainty spike |
| Jul 2024 | Quota reform protests | Political-economic uncertainty |
| Aug 2024+ | Interim government | Policy transition narrative |

### 6.4 Summary Table Template

```
┌──────────────────────┬──────┬──────┬──────┬──────┬──────────┐
│ Method               │ CPI  │ IP   │  FX  │ REM  │ Avg Rank │
├──────────────────────┼──────┼──────┼──────┼──────┼──────────┤
│ BBD (baseline)       │ 0.32 │ 0.28 │ 0.41 │ 0.35 │ 4.0      │
│ Classical ML (LR)    │ 0.45 │ 0.39 │ 0.52 │ 0.44 │ 2.5      │
│ Classical ML (RF)    │ 0.41 │ 0.37 │ 0.48 │ 0.42 │ 3.0      │
│ LSTM                 │ 0.48 │ 0.42 │ 0.55 │ 0.47 │ 2.0      │
│ BanglaBERT           │ 0.53 │ 0.44 │ 0.58 │ 0.51 │ 1.5      │
│ LLM (Claude)         │ 0.56 │ 0.47 │ 0.61 │ 0.55 │ 1.0      │
├──────────────────────┼──────┼──────┼──────┼──────┼──────────┤
│ DM: LLM vs BBD       │ 2.14*│ 1.98*│ 2.31*│ 2.05*│          │
└──────────────────────┴──────┴──────┴──────┴──────┴──────────┘
```

### 6.5 Statistical Rigor

| Concern | Mitigation |
|---|---|
| **Multiple comparisons** | Bonferroni correction on 4 indicators × 4 lags × 6 variants |
| **Look-ahead bias** | Strict temporal train/test split — no future data leaks |
| **Persistence in series** | First-difference or HP-filter all series before correlation |
| **Spurious correlation** | Granger causality test (does BENI Granger-cause the indicator?) |
| **Publication bias** | Pre-register the 4 method specifications before running |

---

## 7. Implementation Roadmap

### Phase 1 — Tooling (1 week)
- [ ] Build `PreprocessingPipeline` factory with 4 presets
- [ ] Build Bangla economic keyword dictionary (200+ terms across categories)
- [ ] Assemble economic indicator dataset (all 12 indicators, aligned monthly)
- [ ] Implement evaluation framework (correlation, DM test, event alignment)

### Phase 2 — BBD Baseline (3 days)
- [ ] Implement keyword matching + normalization pipeline
- [ ] Generate BENI_BBD time series
- [ ] Benchmark against all 12 indicators

### Phase 3 — Classical ML (1 week)
- [ ] Build TF-IDF feature matrix
- [ ] Train Elastic Net, SVM, RF with temporal CV
- [ ] Generate BENI_ML time series
- [ ] Compare against BBD

### Phase 4 — Deep Learning (2 weeks)
- [ ] Train FastText embeddings on BENI corpus
- [ ] Build LSTM regression model
- [ ] Fine-tune BanglaBERT
- [ ] Generate BENI_DL time series
- [ ] Compare against ML and BBD

### Phase 5 — LLM Annotation (2-3 weeks)
- [ ] Pilot: annotate 1,000 articles, compute agreement
- [ ] Full corpus annotation with checkpointing
- [ ] Build BENI_LLM index
- [ ] Final comparison across all 4 methods

### Phase 6 — Writeup (1 week)
- [ ] Methodology description (reproducible)
- [ ] Results table and discussion
- [ ] Which method wins? Under what conditions?
- [ ] Recommendations for future BENI iterations

---

## 8. Open Questions

1. **Economic indicator alignment**: The BBS data frequency and release lags are unknown. Need to research: when are CPI/IP numbers published relative to the measurement month?
2. **Newspaper volume shifts**: If a newspaper stops publishing or a new one starts, does the index require re-normalization?
3. **LLM cost**: 933K articles × ~500 tokens → ~467M input tokens. At Sonnet 4 pricing, that's roughly $1,500-2,000. Budget OK?
4. **Gold standard labels**: For supervised methods, we need human-annotated labels to evaluate the LLM. Is there budget/bandwidth for a human annotation exercise (even 100 articles)?
5. **Domain adaptation**: Will off-the-shelf BanglaBERT (trained on general Bangla) work for financial text, or does it need domain-specific fine-tuning?
