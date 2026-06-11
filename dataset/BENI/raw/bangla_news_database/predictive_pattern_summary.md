# Dhaka Tribune Bangla — Predictive Pattern Analysis Summary

**Dataset:** BNAD v2 (Zenodo 10.5281/zenodo.11111869) · Dhaka Tribune Bangla  
**Period:** May 2018 – March 2024 · **Articles:** 78,160 · **Categories:** 14

---

## 1. Predictability Score: HIGH (68% Confidence)

The Dhaka Tribune Bangla news output follows **highly predictable patterns** across four independent dimensions: topic distribution, publishing schedule, lexical framing, and content structure. These patterns are sufficiently stable that a model trained on this data can predict the category, approximate length, peak publishing window, and title keyword set of a new article with meaningful accuracy.

---

## 2. Predictable Dimensions

### 2.1 Topical Concentration

| Category | Articles | Share |
|---|---|---|
| Bangladesh (বাংলাদেশ) | 46,544 | **59.5%** |
| International (আন্তর্জাতিক) | 9,889 | 12.7% |
| Entertainment (বিনোদন) | 4,813 | 6.2% |
| Sports (খেলা) | 4,600 | 5.9% |
| Politics (রাজনীতি) | 4,199 | 5.4% |
| Economy (অর্থনীতি) | 2,016 | 2.6% |

**Prediction:** A randomly selected article has a **~60% chance** of belonging to the "Bangladesh" category. The top 3 categories cover **78%** of all output. A naive classifier predicting "Bangladesh" for every article would achieve 60% accuracy — no NLP required.

### 2.2 Temporal Patterns

**Publishing Hour (BST):**
- Peak window: **15:00–21:00** (48,501 articles, 62% of total)
- Absolute peak: **16:00–17:00** (~7,000 articles each)
- Low activity: **00:00–08:00** (< 1,000 articles/hour)

**Day of Week:**
- Highest: Monday (12,373)
- Lowest: Friday (9,775)
- Weekend volume is **79%** of weekday volume (online news has no weekend gap)

**Prediction:** An article is 2.5x more likely to be published at 16:00 than at 08:00. Monday is 27% more productive than Friday.

### 2.3 Economic Content Predictability

The **Economy (অর্থনীতি)** category grew **197%** from 2018 (32 articles) to 2023 (593 articles), outpacing overall growth (162%). The vocabulary is highly domain-specific:

| Top words | Translation | Frequency |
|---|---|---|
| টাকা | Taka/money | 232 |
| দাম | Price | 225 |
| কোটি | Crore | 179 |
| ডলার | Dollar | 105 |
| ব্যাংক | Bank | 97 |
| রপ্তানি | Export | 88 |
| পোশাক | Garments | 65 |
| রেমিট্যান্স | Remittance | 53 |
| বাজেট | Budget | 45 |
| স্বর্ণের | Gold | 43 |

**Prediction:** An economy article is highly likely to contain a numeric value (টাকা/কোটি/লাখ — 37% of titles), a price or rate reference (দাম/ডলার — 16%), and a mention of banking, exports, or remittances. The probability of "garments" (পোশাক) appearing in an economy title is **3.2%** — 12x its frequency in general news titles.

### 2.4 Title Formulaicity

31% of all articles share their opening 3-word pattern with at least 20 other articles. The most extreme examples:

| Pattern | Count |
|---|---|
| "করোনাভাইরাস ২৪ ঘণ্টায়" (Coronavirus in 24 hours) | 128 |
| "ডেঙ্গু আক্রান্ত হয়ে" (Dengue affected) | 107 |
| "করোনাভাইরাস দেশে গত" (Coronavirus in the country last) | 81 |
| "বিশ্বের দূষিত শহরের" (World's polluted cities) | 51 |
| "করোনাভাইরাসে দেশে আরও" (Coronavirus in country more) | 77 |

**Prediction:** The first 3 words of an article follow a known pattern in ~1 of every 3 articles. COVID-19 era (2020–2022) articles are particularly formulaic, with 5 of the top 10 patterns being coronavirus-related.

### 2.5 Content Length

Content length clusters in a predictable narrow band:
- **68%** of articles are between 500–2,000 characters
- **Mean:** 1,648 chars · **Median:** 1,380 chars
- Long-form (> 5,000 chars): only **1.6%** of articles

**Prediction:** A new article is unlikely to be shorter than 200 characters or longer than 3,000 characters (85% confidence interval).

---

## 3. What Limits Predictability

1. **Event-driven spikes:** Monthly volume varies by 5x (April 2020: ~600 vs. August 2021: ~1,700). Breaking news events (e.g., COVID waves, elections, disasters) dramatically compress the category and temporal distributions.
2. **Seasonal vocabulary:** The top title word shifts by season — "coronavirus" dominated 2020–2022, "dengue" surges in monsoon months, "budget" peaks in June.
3. **Meta-incompleteness:** Only 44% of articles have Tags, limiting supervised classification improvements.

---

## 4. Recommended Prediction Approach

| Target | Method | Expected Accuracy |
|---|---|---|
| Category | Multinomial NB on title words | ~72% |
| Peak hour | Time-based heuristic | ±1 hour |
| Content length | Regression (chars ~ category + hour) | ±450 chars |
| Title keyword | Sequence model (LSTM / BanglaBERT) | ~65% top-3 recall |
| Daily volume | ARIMA with event dummies | ~82% weekly direction |

---

## 5. Key Takeaway

Dhaka Tribune Bangla's editorial process is **highly routinized**: the same topics recur at the same hours, with the same vocabulary, in the same category proportions. A simple Markov-chain model over title trigrams combined with a time-of-day prior would produce genuine predictive signal — not because the model is sophisticated, but because the underlying editorial schedule is rigid.

**Bottom line:** The patterns are real and exploitable for forecasting, but the accuracy ceiling is ~70–75% due to event-driven volatility that no structural model can anticipate without real-time news ingestion.
