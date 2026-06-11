# Dataset Exploration: Three-Phase Plan

**Corpus**: Unified Bangla News (Potrika 2014–2020 + BNAD 2021–2024) — **1,467,705 articles**
**Goal**: Comprehensive corpus understanding before rebuilding narrative indexes
**Status**: 🟡 Planning Complete — Ready for Phase 1

---

## Phase 1 — Corpus Understanding (what the dataset *is*)

### 1A. Descriptive Profiling — per year, per source, per category

- [ ] **Article counts per year** — bar chart (baseline: 2014: 2.5K → 2023: 364K)
- [ ] **Articles per newspaper over time** — Jugantor, Ittefaq, Kaler Kontho, Jaijaidin, Inqilab, Somoyer Alo — detect mid-period dropouts
- [ ] **Articles per harmonised category over time** — Economy (58K), National (780K), Politics (54K), International (80K), Health, Tech, Sports, Entertainment
- [ ] **Source stability at 2020/2021 boundary** — Potrika newspapers disappearing vs BNAD sources appearing
- [ ] **Text length distribution** — article length per category/year/source; identify outliers and empty-text rows

### 1B. Vocabulary Profiling — corpus linguistics baseline

- [ ] **Type-token ratio per year** — vocabulary richness trajectory
- [ ] **Hapax legomena proportion** — words appearing once as diversity indicator
- [ ] **Most frequent words per category** — raw frequency lists for Economy, National, Politics, etc.
- [ ] **Distinctive keywords per category** — log-odds ratio or PMI to find uniquely differentiating terms
- [ ] **Most frequent bigrams/trigrams** — phrasal lexicon: *মুদ্রাস্ফীতি চাপ*, *বৈদেশিক মুদ্রা*, *সুদের হার*
- [ ] **Collocations around key economic terms** — words clustering around *অর্থনীতি*, *মুদ্রাস্ফীতি*, *বাজেট*, *রিজার্ভ* per year

### 1C. Word Clouds — framing shift visualisation

- [ ] **Per category word cloud** — Economy vs National vs Politics vs International
- [ ] **Per year word cloud (Economy only)** — how economic vocabulary shifts 2014→2020→2024
- [ ] **Per newspaper word cloud** — editorial differences across sources
- [ ] **Annotate visual patterns** — e.g., *রিজার্ভ* spiking in 2022, *মুদ্রাস্ফীতি* dominating 2023–2024

---

## Phase 2 — Linguistic Exploration (what the dataset *means*)

### 2A. Diachronic Lexical Analysis — language change over 11 years

- [ ] **Neologism tracking** — new Bangla words entering news discourse 2014→2024 (loanwords, technical terms)
- [ ] **Semantic drift check** — does *অর্থনীতি* mean the same in 2014 vs 2024?
- [ ] **Orthographic variation** — *কেন্দ্রীয়* vs *কেন্দ্রীয়* — does spelling standardise over time?
- [ ] **Anglicism tracking** — frequency of English code-mixing per year (GDP, CPI, inflation, budget as-is in Bangla text)

### 2B. Register and Genre Analysis

- [ ] **Newspaper editorial fingerprint** — which source uses the most English borrowings? Most Sanskritised vocabulary?
- [ ] **Genre markers** — how does economic reporting differ structurally from political? (SVO patterns, passive constructions, nominalisation density)
- [ ] **Headline analysis** — do headlines become more sensational over time? (exclamation frequency, superlative density)

### 2C. Source-Critical Analysis — the 2020/2021 break

- [ ] **Bridge sample comparison** — Potrika 2018–2020 vs BNAD 2021–2023 vocabulary profiles
- [ ] **Per-category vocabulary overlap** — Potrika Economy vs BNAD Economy articles
- [ ] **Source distribution diagnostic** — does the jump from 6 newspapers to many sources create structural break?
- [ ] **Merge validity assessment** — if 2018–2020 overlap matches, merge is safe; otherwise document the break

### 2D. Named Entity Analysis

- [ ] **Entity extraction** — organisations, people, places in economic news
- [ ] **Entity frequency over time** — *বাংলাদেশ ব্যাংক*, IMF, *বিশ্ব ব্যাংক*, *বিএসইসি*
- [ ] **Entity co-occurrence networks** — entities co-occurring with inflation talk vs reserve talk vs budget talk
- [ ] **Person frequency tracking** — which economists/policymakers cited most; does cast change across governments/tenures?

---

## Phase 3 — Pre-Index Modelling (what feeds the index)

### 3A. Weak Label Quality Assessment

- [ ] **Manual spot-check** — are 100–200 Economy articles actually about the economy? (precision audit)
- [ ] **Keyword density analysis** — are there economy-relevant articles mislabelled as National/Politics? (recall audit)
- [ ] **Label noise estimation** — document expected drop from current 91.7% accuracy

### 3B. Source-Balance Analysis

- [ ] **Newspaper dominance per year** — which sources dominate which periods?
- [ ] **Dropout sensitivity analysis** — does index shift meaningfully if a newspaper drops out mid-period?
- [ ] **Source-weighting strategy** — equal contribution vs proportional to article count

### 3C. The 2020/2021 Bridge Sample (make-or-break diagnostic)

- [ ] **Build Potrika-only monthly index** — 2014–2020
- [ ] **Build BNAD-only monthly index** — 2021–2024
- [ ] **Build unified monthly index** — full 2014–2024
- [ ] **Overlap comparison** — Potrika 2018–2020 vs BNAD 2018–2020
- [ ] **Merge safety verdict** — if overlap matches → proceed; if different → document structural break

---

## Bonus Analyses (post-primary)

- [ ] Multi-domain narrative indices: Health (4.6K), Education (9.4K), Tech/Science (5.5K)
- [ ] Cross-domain coherence: do economic and political narratives move together?
- [ ] Unsupervised burst detection: event timeline from term spikes (*করোনা*, *লকডাউন*, *বাজেট*, *ভোট*)
- [ ] Framing shift analysis: "growth"→"crisis" framing transition points in Economy articles
- [ ] Dictionary-based narrative force: continuous measure of economic language intensity
- [ ] Cross-source consistency: Jugantor-only vs Ittefaq-only vs Kaler Kontho-only index comparison

---

## Execution Order

| Step | Phase | What | Output |
|------|-------|------|--------|
| 1 | 1A | Load and profile deduped unified corpus | Summary stats, tables |
| 2 | 1A | Text length distribution + empty-text counts | Quality filter decisions |
| 3 | 1B | Vocabulary analysis: TTR, hapax, top N per category | Corpus linguistics baseline |
| 4 | 1C | Word clouds: per category, per year (Economy), per newspaper | Visual exploration |
| 5 | 1B | Keyword analysis: distinctive terms via log-odds | Category signal words |
| 6 | 2A | Diachronic: English borrowing frequency, neologism detection | Language change over 11 years |
| 7 | 2C | Source break diagnostic: vocabulary overlap Potrika↔BNAD | Merge validity assessment |
| 8 | 3B | Source balance: newspaper coverage over time | Weighting strategy |
| 9 | Bonus | Burst detection: unsupervised event timeline | Non-economic insights |
| 10 | 3C | Train classifier on full corpus → build index | — |

**Critical constraint**: Steps 1–8 must complete *before* training any classifier or building any index. Steps 3–6 are the linguistics value-add that most NLP pipelines skip.
